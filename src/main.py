#%%
import json
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

#%% add src to path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name == "src" else SCRIPT_DIR

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

load_dotenv(SCRIPT_DIR / ".env")
load_dotenv(PROJECT_ROOT / ".env")

#%%
from base import base_solve
from agent import Agent
from executor import run_solution, extract_code

from problems.dynamic_programming import get_split, validate_problem_bank

#%%
def make_run_dir() -> Path:
    now = datetime.now()
    run_dir = PROJECT_ROOT / "results" / now.strftime("%y%m%d") / now.strftime("%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir

#%%
def evaluate_solver(name: str, solver_fn, problems: list) -> dict:
    total_passed = 0
    total_tests = 0
    rows = []
    print(f"\nEvaluating: {name}")

    for prob in problems:
        try:
            raw = solver_fn(prob["description"], category=prob["category"])
        except TypeError:
            raw = solver_fn(prob["description"])

        code = extract_code(raw)
        if not code.strip().startswith("def") and "def solve" in raw:
            code = raw

        result = run_solution(code, prob["test_cases"])
        total_passed += result["passed"]
        total_tests += result["total"]

        if result["pass_rate"] == 1.0:
            status = "PASS"
        elif result["pass_rate"] > 0:
            status = "PARTIAL"
        else:
            status = "FAIL"

        error_text = ""
        if result["errors"]:
            error_text = " error: " + result["errors"][0][:80].replace("\n", " ")

        print(
            f"  {status} {prob['id']} ({prob['category']}) "
            f"{result['passed']}/{result['total']}{error_text}"
        )

        rows.append(
            {
                "id": prob["id"],
                "title": prob["title"],
                "category": prob["category"],
                "difficulty": prob["difficulty"],
                "passed": result["passed"],
                "total": result["total"],
                "pass_rate": result["pass_rate"],
                "runtime_ms": result["runtime_ms"],
                "errors": result["errors"][:2],
            }
        )

    overall = total_passed / total_tests if total_tests else 0.0
    print(f"\n{name}: {total_passed}/{total_tests} = {overall:.1%}")
    return {
        "name": name,
        "passed": total_passed,
        "total": total_tests,
        "pass_rate": overall,
        "problems": rows,
    }

#%%
def main() -> None:
    print("Starting experiment")

    validate_problem_bank()

    run_dir = make_run_dir()

    probe = get_split("probe")  # agent trains on these
    eval_s = get_split("eval")  # agent self-evals during evolution
    test = get_split("test")  # final held-out benchmark

    print(f"Project root: {PROJECT_ROOT}")
    print(f"Results directory: {run_dir}")
    print(f"Dataset: probe={len(probe)}, eval={len(eval_s)}, test={len(test)}")

    # BEFORE — gpt-4o-mini with no scaffolding
    baseline_result = evaluate_solver(
        "baseline (gpt-4o-mini, no scaffolding)",
        base_solve,
        test,
    )

    # EVOLVE — stem agent uses probe + eval, never sees test
    agent = Agent()
    history = agent.evolve(probe_problems=probe, eval_problems=eval_s)

    # AFTER — evolved agent (gpt-4o + full scaffolding + few-shots) on test set
    evolved_result = evaluate_solver(
        "evolved stem agent (gpt-4o, scaffolding, few shots)",
        agent.solve,
        test,
    )

    improvement = evolved_result["pass_rate"] - baseline_result["pass_rate"]

    experiment = {
        "run_dir": str(run_dir),
        "baseline": baseline_result,
        "evolved": evolved_result,
        "improvement": improvement,
        "history": history,
    }

    experiment_path = run_dir / "experiment_results.json"
    prompt_path = run_dir / "final_system_prompt.txt"
    few_shot_path = run_dir / "few_shot_store.json"

    with experiment_path.open("w", encoding="utf-8") as f:
        json.dump(experiment, f, indent=2)

    with prompt_path.open("w", encoding="utf-8") as f:
        f.write(agent.state.system_prompt)

    with few_shot_path.open("w", encoding="utf-8") as f:
        json.dump(agent.state.few_shot_store, f, indent=2)

    print("")
    print("Final comparison")
    print(f"Baseline: {baseline_result['pass_rate']:.1%}")
    print(f"Evolved: {evolved_result['pass_rate']:.1%}")
    print(f"Delta: {improvement:+.1%}")
    print("")
    print(f"Saved experiment results to: {experiment_path}")
    print(f"Saved final system prompt to: {prompt_path}")
    print(f"Saved few shot store to: {few_shot_path}")


if __name__ == "__main__":
    main()