# backend/testing/coverage.py
"""Test coverage analysis for generated solutions."""

import logging
import os
import re
import subprocess
import tempfile

from backend.config import settings

logger = logging.getLogger(__name__)


def _extract_code_block(text: str) -> str:
    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


class CoverageAnalyzer:
    """Measures line coverage of solution code via pytest-cov."""

    def analyze(self, solution_code: str, test_code: str) -> dict:
        solution = _extract_code_block(solution_code)
        tests = _extract_code_block(test_code)

        if not solution or not tests:
            return {"coverage_percent": 0.0, "lines_covered": 0, "lines_total": 0, "meets_threshold": False}

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
                    [
                        "python", "-m", "pytest", test_path,
                        f"--cov=solution", "--cov-report=term-missing", "-q",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=tmpdir,
                )
                output = result.stdout + result.stderr
                match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", output)
                coverage = float(match.group(1)) / 100.0 if match else 0.0

                lines_match = re.search(r"TOTAL\s+(\d+)\s+(\d+)", output)
                lines_total = int(lines_match.group(1)) if lines_match else 0
                lines_missed = int(lines_match.group(2)) if lines_match else 0
                lines_covered = lines_total - lines_missed

                return {
                    "coverage_percent": coverage,
                    "lines_covered": lines_covered,
                    "lines_total": lines_total,
                    "meets_threshold": coverage >= settings.COVERAGE_THRESHOLD,
                    "report": output[:2000],
                }
            except Exception as e:
                logger.error(f"Coverage analysis failed: {e}")
                return {
                    "coverage_percent": 0.0,
                    "lines_covered": 0,
                    "lines_total": 0,
                    "meets_threshold": False,
                    "report": str(e),
                }


coverage_analyzer = CoverageAnalyzer()
