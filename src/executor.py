#%%
import ast
import subprocess
import sys
import json
import textwrap
import time
import re
import base64
from typing import Any


TIMEOUT_SECONDS = 10

#%%
def run_solution(code: str, test_cases: list[tuple[dict, Any]]) -> dict:
    results = {"passed": 0, "total": len(test_cases), "errors": [], "runtime_ms": 0.0}

    for kwargs, expected in test_cases:
        harness = _build_harness(code, kwargs, expected)
        t0 = time.perf_counter()
        try:
            proc = subprocess.run(
                [sys.executable, "-c", harness],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )
            elapsed = (time.perf_counter() - t0) * 1000
            results["runtime_ms"] += elapsed

            if proc.returncode == 0:
                output = proc.stdout.strip()
                if output == "PASS":
                    results["passed"] += 1
                else:
                    results["errors"].append(output or proc.stderr.strip())
            else:
                err = (proc.stderr or proc.stdout or "unknown error").strip()
                results["errors"].append(err[:300])
        except subprocess.TimeoutExpired:
            results["errors"].append(f"TimeoutExpired after {TIMEOUT_SECONDS}s")

    results["pass_rate"] = results["passed"] / results["total"] if results["total"] else 0.0
    return results

#%%
def _build_harness(code: str, kwargs: dict, expected: Any) -> str:
    """
    Build a Python test harness.

    Important: generated code is placed at column zero.
    Do not indent the inserted code inside a triple-quoted string,
    because textwrap.dedent can remove the indentation from function bodies and cause IndentationError.
    """
    cleaned_code = extract_code(code).strip()
    kwargs_b64 = base64.b64encode(json.dumps(kwargs).encode("utf-8")).decode("utf-8")
    expected_repr = repr(expected)

    prefix = "import base64\nimport json\nimport sys\n\n"
    suffix = f"""
    raw = base64.b64decode("{kwargs_b64}").decode("utf-8")
    kwargs = json.loads(raw)
    expected = {expected_repr}
    try:
        result = solve(**kwargs)
        if result == expected:
            print("PASS")
        else:
            print(f"FAIL: got {{result!r}}, expected {{expected!r}}")
    except Exception as e:
        import traceback
        print(f"ERROR: {{type(e).__name__}}: {{e}}")
        traceback.print_exc(file=sys.stdout)
    """
    return prefix + cleaned_code + "\n\n" + textwrap.dedent(suffix).lstrip()

#%%
def extract_code(text: str) -> str:
    """
    Extract Python code from a markdown code block or raw text
    """
    text = text.strip()

    fenced_python = re.search(r"```python\s*(.*?)```", text, re.DOTALL)
    if fenced_python:
        return fenced_python.group(1).strip()

    fenced = re.search(r"```\s*(.*?)```", text, re.DOTALL)
    if fenced:
        return fenced.group(1).strip()

    def_match = re.search(r"(^def\s+solve\s*\(.*)", text, re.DOTALL | re.MULTILINE)
    if def_match:
        return def_match.group(1).strip()

    return text

#%%
def extract_json(text: str) -> dict:
    """
    Extract JSON from model output.
    """
    text = text.strip()
    for pattern in [r"```json\s*(.*?)```", r"```\s*(.*?)```"]:
        m = re.search(pattern, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1).strip())
            except json.JSONDecodeError:
                pass
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start:end+1])
        except json.JSONDecodeError:
            pass
    return {}


def check_syntax(code: str) -> tuple[bool, str]:
    try:
        ast.parse(extract_code(code))
        return True, ""
    except SyntaxError as exc:
        return False, str(exc)
