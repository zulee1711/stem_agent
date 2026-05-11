from ..helper import make_id

PROBLEMS = [
    {
        "id": make_id("dp", "knapsack", "zero_one_knapsack"),
        "title": "0-1 Knapsack",
        "category": "knapsack",
        "difficulty": "medium",
        "split": "probe",
        "description": (
            "Given weights and values of n items and a capacity W, find the maximum "
            "value you can fit in the knapsack. Each item may be used at most once.\n"
            "Write a Python function: def solve(weights: list, values: list, W: int) -> int"
        ),
        "test_cases": [
            ({"weights": [1, 3, 4, 5], "values": [1, 4, 5, 7], "W": 7}, 9),
            ({"weights": [2, 3, 4, 5], "values": [3, 4, 5, 6], "W": 5}, 7),
            ({"weights": [1, 2, 3], "values": [6, 10, 12], "W": 5}, 22),
        ],
    },
    {
        "id": make_id("dp", "knapsack", "partition_equal_subset_sum"),
        "title": "Partition Equal Subset Sum",
        "category": "knapsack",
        "difficulty": "medium",
        "split": "eval",
        "description": (
            "Given an integer array nums, return True if it can be partitioned into two "
            "subsets with equal sum, else False.\n"
            "Write a Python function: def solve(nums: list) -> bool"
        ),
        "test_cases": [
            ({"nums": [1, 5, 11, 5]}, True),
            ({"nums": [1, 2, 3, 5]}, False),
            ({"nums": [3, 3, 3, 4, 5]}, True),
        ],
    },
    {
        "id": make_id("dp", "knapsack", "coin_change"),
        "title": "Coin Change",
        "category": "knapsack",
        "difficulty": "medium",
        "split": "test",
        "description": (
            "Given coins of different denominations and a total amount, find the fewest "
            "number of coins needed to make up that amount. Return -1 if impossible.\n"
            "Write a Python function: def solve(coins: list, amount: int) -> int"
        ),
        "test_cases": [
            ({"coins": [1, 5, 11], "amount": 15}, 3),
            ({"coins": [2], "amount": 3}, -1),
            ({"coins": [1, 2, 5], "amount": 11}, 3),
        ],
    },
]