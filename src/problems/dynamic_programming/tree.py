from ..helper import make_id

PROBLEMS = [
    {
        "id": make_id("dp", "tree", "house_robber_iii"),
        "title": "House Robber III",
        "category": "tree_dp",
        "difficulty": "medium",
        "split": "test",
        "description": (
            "Houses are arranged in a binary tree. You cannot rob two directly-linked houses."
            "The tree is given as a level-order list with None for missing nodes. Return the maximum money you can rob.\n"
            "Write a Python function: def solve(root_vals: list) -> int"
        ),
        "test_cases": [
            ({"root_vals": []}, 0),
            ({"root_vals": [4]}, 4),
            ({"root_vals": [3, 2, 3, None, 3, None, 1]}, 7),
            ({"root_vals": [3, 4, 5, 1, 3, None, 1]}, 9),
            ({"root_vals": [4, 1, None, 2, None, 3]}, 7),
        ],
    },
]
