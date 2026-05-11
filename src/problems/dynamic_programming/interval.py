from ..helper import make_id


PROBLEMS = [
    {
        "id": make_id("dp", "interval", "burst_balloons"),
        "title": "Burst Balloons",
        "category": "interval_dp",
        "difficulty": "hard",
        "split": "test",
        "description": (
            "Given balloons with values nums, burst them in any order. Bursting i gives "
            "nums[i-1] * nums[i] * nums[i+1] coins, using 1 outside the array. "
            "Return the maximum coins.\n"
            "Write a Python function: def solve(nums: list) -> int"
        ),
        "test_cases": [
            ({"nums": [3, 1, 5, 8]}, 167),
            ({"nums": [1, 5]}, 10),
            ({"nums": [1]}, 1),
            ({"nums": []}, 0),
            ({"nums": [7, 9, 8, 0, 7, 1, 3, 5, 5, 2, 3]}, 1654),
        ],
    },
    {
        "id": make_id("dp", "interval", "palindrome_partitioning_ii"),
        "title": "Palindrome Partitioning II",
        "category": "interval_dp",
        "difficulty": "hard",
        "split": "test",
        "description": (
            "Given a string s, return the minimum number of cuts needed to partition it so every substring is a palindrome.\n"
            "Write a Python function: def solve(s: str) -> int"
        ),
        "test_cases": [
            ({"s": "aab"}, 1),
            ({"s": "a"}, 0),
            ({"s": "ab"}, 1),
            ({"s": "aaabaa"}, 1),
            ({"s": "cabababcbc"}, 3),
        ],
    },
]