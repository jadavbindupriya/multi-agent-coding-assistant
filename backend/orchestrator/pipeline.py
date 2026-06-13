# backend/orchestrator/pipeline.py
"""Multi-agent orchestration pipeline with RAG, tools, testing, and metrics."""

import logging
import time
import uuid

from backend.agents.planner import planner
from backend.agents.coder import coder
from backend.agents.reviewer import reviewer
from backend.agents.tester import tester
from backend.rag.retriever import retriever
from backend.testing.runner import test_runner
from backend.testing.coverage import coverage_analyzer
from backend.storage.tasks import task_store
from backend.storage.metrics import metrics_store
from backend.config import settings

logger = logging.getLogger(__name__)


class AgentPipeline:
    """Orchestrates Planner → Coder → Reviewer → Tester with all Phase 5-9 features."""

    def run(self, task: str, language: str = "python", context: str = None, use_knowledge: bool = True) -> dict:
        task_id = str(uuid.uuid4())
        start_time = time.perf_counter()
        task_store.create(task_id, task)

        knowledge = ""
        if use_knowledge and retriever.has_knowledge():
            knowledge = retriever.retrieve(task)
            if knowledge:
                task_store.add_message(task_id, "Retrieved knowledge from documentation")

        agent_outputs = []
        total_tokens = 0

        # Planner
        task_store.update(task_id, current_agent="Planner", progress_percent=10)
        t0 = time.perf_counter()
        planner_result = planner.plan(task, language, knowledge=knowledge, context=context)
        planner_time = time.perf_counter() - t0
        if planner_result["status"] == "error":
            task_store.fail(task_id, planner_result["error"])
            metrics_store.record_error("Planner", planner_result["error"], task_id)
            return {"status": "error", "error": planner_result["error"], "task_id": task_id}

        plan = planner_result["plan"]
        total_tokens += planner_result["tokens_used"]
        agent_outputs.append(self._agent_output("Planner", plan, planner_result["tokens_used"], planner_time))
        task_store.add_message(task_id, "Planner completed")

        # Coder (with tool calling)
        task_store.update(task_id, current_agent="Coder", progress_percent=35)
        t0 = time.perf_counter()
        coder_result = coder.code(task, plan, language, knowledge=knowledge, context=context)
        coder_time = time.perf_counter() - t0
        if coder_result["status"] == "error":
            task_store.fail(task_id, coder_result["error"])
            metrics_store.record_error("Coder", coder_result["error"], task_id)
            return {"status": "error", "error": coder_result["error"], "task_id": task_id}

        solution = coder_result["code"]
        total_tokens += coder_result["tokens_used"]
        coder_output = solution
        if coder_result.get("tool_calls"):
            tool_summary = "\n".join(f"🔧 {tc['tool']}: {tc['result'][:100]}" for tc in coder_result["tool_calls"])
            coder_output = f"{solution}\n\n--- Tools Used ---\n{tool_summary}"
        agent_outputs.append(self._agent_output("Coder", coder_output, coder_result["tokens_used"], coder_time, coder_result.get("tool_calls")))
        task_store.add_message(task_id, "Coder completed")

        # Reviewer
        task_store.update(task_id, current_agent="Reviewer", progress_percent=60)
        t0 = time.perf_counter()
        reviewer_result = reviewer.review(solution, task, knowledge=knowledge)
        reviewer_time = time.perf_counter() - t0
        if reviewer_result["status"] == "error":
            task_store.fail(task_id, reviewer_result["error"])
            return {"status": "error", "error": reviewer_result["error"], "task_id": task_id}

        review = reviewer_result["review"]
        total_tokens += reviewer_result["tokens_used"]
        agent_outputs.append(self._agent_output("Reviewer", review, reviewer_result["tokens_used"], reviewer_time))
        task_store.add_message(task_id, "Reviewer completed")

        # Tester (enhanced with property-based testing)
        task_store.update(task_id, current_agent="Tester", progress_percent=80)
        t0 = time.perf_counter()
        tester_result = tester.test(solution, task)
        tester_time = time.perf_counter() - t0
        if tester_result["status"] == "error":
            task_store.fail(task_id, tester_result["error"])
            return {"status": "error", "error": tester_result["error"], "task_id": task_id}

        tests = tester_result["tests"]
        total_tokens += tester_result["tokens_used"]

        test_execution = None
        coverage = None
        if settings.ENABLE_TEST_EXECUTION:
            test_execution = test_runner.run_tests(solution, tests)
            coverage = coverage_analyzer.analyze(solution, tests)

        tester_output = tests
        if test_execution:
            status = "✅ PASSED" if test_execution["passed"] else "❌ FAILED"
            tester_output += f"\n\n--- Test Execution ---\n{status}: {test_execution['passed_count']}/{test_execution['total']} passed"
            if test_execution.get("edge_cases_found"):
                tester_output += f"\nEdge cases: {', '.join(test_execution['edge_cases_found'])}"
        if coverage:
            tester_output += f"\nCoverage: {coverage['coverage_percent']*100:.0f}%"

        agent_outputs.append(self._agent_output("Tester", tester_output, tester_result["tokens_used"], tester_time))
        task_store.add_message(task_id, "Tester completed")

        execution_time = time.perf_counter() - start_time
        confidence = self._compute_confidence(review, test_execution, coverage)

        result = {
            "status": "success",
            "task_id": task_id,
            "original_task": task,
            "solution": solution,
            "tests": tests,
            "explanation": (
                "Solved using 4 specialized agents with RAG, tool calling, "
                "test execution, and coverage analysis."
            ),
            "agent_outputs": agent_outputs,
            "total_tokens_used": total_tokens,
            "execution_time": round(execution_time, 2),
            "confidence_score": confidence,
            "knowledge_used": bool(knowledge),
            "test_execution": test_execution,
            "coverage": coverage,
            "estimated_cost_usd": round((total_tokens / 1000) * settings.TOKEN_COST_PER_1K, 4),
        }

        task_store.complete(task_id, {
            "total_tokens": total_tokens,
            "execution_time": execution_time,
            "agent_outputs": [{"agent_name": a["agent_name"], "tokens_used": a["tokens_used"]} for a in agent_outputs],
        })
        metrics_store.record_task(task_id, agent_outputs, total_tokens, execution_time)

        return result

    def _agent_output(self, name, output, tokens, exec_time, tool_calls=None):
        return {
            "agent_name": name,
            "output": output,
            "tokens_used": tokens,
            "execution_time": round(exec_time, 2),
            "success": True,
            "tool_calls": tool_calls or [],
        }

    def _compute_confidence(self, review, test_execution, coverage):
        score = 0.75
        if "excellent" in review.lower() or "good" in review.lower():
            score += 0.1
        if test_execution and test_execution.get("passed"):
            score += 0.1
        if coverage and coverage.get("meets_threshold"):
            score += 0.05
        return min(round(score, 2), 1.0)


pipeline = AgentPipeline()
