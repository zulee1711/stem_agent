#%%
from .one_d import PROBLEMS as ONE_D_PROBLEMS
from .two_d import PROBLEMS as TWO_D_PROBLEMS
from .knapsack import PROBLEMS as KNAPSACK_PROBLEMS
from .tree import PROBLEMS as TREE_PROBLEMS
from .bitmask import PROBLEMS as BITMASK_PROBLEMS
from .interval import PROBLEMS as INTERVAL_PROBLEMS

#%%
PROBLEMS = (
    ONE_D_PROBLEMS
    + TWO_D_PROBLEMS
    + KNAPSACK_PROBLEMS
    + TREE_PROBLEMS
    + BITMASK_PROBLEMS
    + INTERVAL_PROBLEMS
)

PROBLEM_BY_ID = {p["id"]: p for p in PROBLEMS}

#%%
def get_split(split: str) -> list[dict]:
    valid_splits = {"probe", "test", "eval", "all"}

    if split not in valid_splits:
        raise ValueError(f"Invalid split: {split}. Expected one of {valid_splits}")

    if split == "all":
        return PROBLEMS

    return [p for p in PROBLEMS if p["split"] == split]

#%%
def get_problem(problem_id: str) -> dict:
    if problem_id not in PROBLEM_BY_ID:
        raise ValueError(f"Problem ID not found: {problem_id}")
    return PROBLEM_BY_ID[problem_id]

#%%
def get_by_category(category:str) -> list[dict]:
    return [p for p in PROBLEMS if p["category"] == category]

#%%
def validate_problem_bank():
    required_fields = {
        "id",
        "title",
        "category",
        "difficulty",
        "split",
        "description",
        "test_cases",
    }

    valid_splits = {"probe", "test", "eval"}

    seen_ids = set()

    for p in PROBLEMS:
        missing = required_fields - set(p)
        if missing:
            problem_id = p.get("id", "<unknown>")
            raise ValueError(
                f"Problem {problem_id} missing fields: {missing}"
            )

        if p["id"] in seen_ids:
            raise ValueError(
                f"Duplicate problem ID: {p['id']}"
            )

        seen_ids.add(p["id"])

        if p["split"] not in valid_splits:
            raise ValueError(
                f"Problem {p['id']} has invalid split: {p['split']}"
            )

        if not isinstance(p["test_cases"], list) or not p["test_cases"]:
            raise ValueError(
                f"Problem {p['id']} has no test cases."
            )