# backend/tools/code_sandbox.py
"""Safe Python code execution sandbox."""

import logging
import subprocess
import tempfile
import os

from backend.config import settings

logger = logging.getLogger(__name__)


def execute_python(code: str) -> dict:
    """Execute Python code in a subprocess with timeout."""
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            f.write(code)
            temp_path = f.name

        try:
            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                timeout=settings.SANDBOX_TIMEOUT,
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout[:2000],
                "stderr": result.stderr[:2000],
                "exit_code": result.returncode,
            }
        finally:
            os.unlink(temp_path)
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "Execution timed out", "exit_code": -1}
    except Exception as e:
        logger.error(f"Sandbox execution failed: {e}")
        return {"success": False, "stdout": "", "stderr": str(e), "exit_code": -1}
