# backend/testing/runner.py
"""Execute generated tests and report results."""

import logging
import os
import re
import subprocess
import tempfile
from typing import List

logger = logging.getLogger(__name__)


def _extract_code_block(text: str) -> str:
    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def _detect_edge_cases(test_code: str) -> List[str]:
    edge_patterns = [
        (r"empty|None|null|zero|0\b", "empty/null input"),
        (r"negative|-\d", "negative values"),
        (r"large|max|overflow|9999", "large input"),
        (r"unicode|special.?char", "special characters"),
        (r"raises|pytest\.raises|Exception", "error handling"),
        (r"@given|hypothesis|st\.", "property-based"),
    ]
    found = []
    lower = test_code.lower()
    for pattern, label in edge_patterns:
        if re.search(pattern, lower):
            found.append(label)
    return found


class TestRunner:
    """Runs generated pytest tests against solution code."""

    def run_tests(self, solution_code: str, test_code: str) -> dict:
        solution = _extract_code_block(solution_code)
        tests = _extract_code_block(test_code)

        if not solution or not tests:
            return {
                "passed": False,
                "total": 0,
                "passed_count": 0,
                "failed_count": 0,
                "output": "Could not extract code from solution or tests",
                "edge_cases_found": [],
            }

        edge_cases = _detect_edge_cases(tests)
        has_property_tests = any("property" in e for e in edge_cases)

        with tempfile.TemporaryDirectory() as tmpdir:
            solution_path = os.path.join(tmpdir, "solution.py")
            test_path = os.path.join(tmpdir, "test_solution.py")

            with open(solution_path, "w", encoding="utf-8") as f:
                f.write(solution)
            with open(test_path, "w", encoding="utf-8") as f:
                if "from solution" not in tests and "import solution" not in tests:
                    tests = f"import sys\nsys.path.insert(0, '{tmpdir}')\nfrom solution import *\n\n{tests}"
                f.write(tests)

            try:
                result = subprocess.run(
                    ["python", "-m", "pytest", test_path, "-v", "--tb=short", "-q"],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=tmpdir,
                )
                output = (result.stdout + result.stderr)[:3000]
                passed_match = re.search(r"(\d+) passed", output)
                failed_match = re.search(r"(\d+) failed", output)
                passed_count = int(passed_match.group(1)) if passed_match else 0
                failed_count = int(failed_match.group(1)) if failed_match else 0
                total = passed_count + failed_count

                return {
                    "passed": result.returncode == 0 and total > 0,
                    "total": total,
                    "passed_count": passed_count,
                    "failed_count": failed_count,
                    "output": output,
                    "edge_cases_found": edge_cases,
                    "has_property_tests": has_property_tests,
                }
            except subprocess.TimeoutExpired:
                return {
                    "passed": False,
                    "total": 0,
                    "passed_count": 0,
                    "failed_count": 0,
                    "output": "Test execution timed out",
                    "edge_cases_found": edge_cases,
                    "has_property_tests": has_property_tests,
                }
            except Exception as e:
                logger.error(f"Test runner error: {e}")
                return {
                    "passed": False,
                    "total": 0,
                    "passed_count": 0,
                    "failed_count": 0,
                    "output": str(e),
                    "edge_cases_found": edge_cases,
                    "has_property_tests": has_property_tests,
                }


test_runner = TestRunner()
