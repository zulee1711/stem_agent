#%%
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
    Use base64-encoded kwargs to avoid any quote/escape conflicts in the f-string
    """
    kwargs_b64 = base64.b64encode(json.dumps(kwargs).encode()).decode()
    expected_repr = repr(expected)

    harness = textwrap.dedent(f"""
    import json, sys, base64
    
    {code}
    
    raw = base64.b64decode("{kwargs_b64}").decode()
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
    """)
    return harness

#%%
def extract_code(text: str) -> str:
    """
    Extract Python code from a markdown code block or raw text
    """
    if "```python" in text:
        start = text.index("```python") + 9
        end = text.index("```", start)
        return text[start:end].strip()
    if "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        return text[start:end].strip()
    return text.strip()

#%%
def extract_json(text: str) -> dict:
    """
    Robustly extract JSON from LLM output.
    GPT often wraps JSON in ```json ... ``` fences.
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