"""
Dynamic Programming Problems Bank
Each problem should have:
- id, title, category
- split: which set it belongs to (probe/test/eval)
- description: what it solves
- test cases: list of (input kwargs dict, expected output)
- difficulty: easy/medium/hard

PROBLEMS template:
PROBLEMS = [
    {
        "id": "<main_problem>.<category>.<title>",
        "title": "",
        "category": "",
        "difficulty": "",
        "split": "",
        "description": (),
        "test_cases": [
            (# input, expected output),
        ]
    },
]
"""
from ..helper import make_id

PROBLEMS = [
    {
        "id": make_id("dp", "1d", "climbing_stairs"),
        "title": "Climbing Stairs",
        "category": "1d_dp",
        "difficulty": "easy",
        "split": "probe",
        "description": (
            "You are climbing a staircase with n steps. Each time you can climb 1 or 2 steps. "
            "In how many distinct ways can you climb to the top?\n"
            "Write a Python function: def solve(n: int) -> int"
        ),
        "test_cases": [
            ({"n": 0}, 1),
            ({"n": 1}, 1),
            ({"n": 2}, 2),
            ({"n": 3}, 3),
            ({"n": 5}, 8),
            ({"n": 10}, 89),
        ],
    },
    {
        "id": make_id("dp", "1d", "house_robber"),
        "title": "House Robber",
        "category": "1d_dp",
        "difficulty": "easy",
        "split": "probe",
        "description": (
            "Given an array nums of non-negative integers representing amounts of money, "
            "return the max you can rob without robbing two adjacent houses.\n"
            "Write a Python function: def solve(nums: list) -> int"
        ),
        "test_cases": [
            ({"nums": []}, 0),
            ({"nums": [5]}, 5),
            ({"nums": [1, 2, 3, 1]}, 4),
            ({"nums": [2, 7, 9, 3, 1]}, 12),
            ({"nums": [2, 1, 1, 2]}, 4),
        ],
    },
    {
        "id": make_id("dp", "1d", "maximum_subarray"),
        "title": "Maximum Subarray",
        "category": "1d_dp",
        "difficulty": "easy",
        "split": "probe",
        "description": (
            "Given an integer array nums, find the subarray with the largest sum and return its sum.\n"
            "Write a Python function: def solve(nums: list) -> int"
        ),
        "test_cases": [
            ({"nums": [-2, 1, -3, 4, -1, 2, 1, -5, 4]}, 6),
            ({"nums": [1]}, 1),
            ({"nums": [-3, -2, -5]}, -2),
            ({"nums": [5, 4, -1, 7, 8]}, 23),
        ],
    },
    {
        "id": make_id("dp", "1d", "decode_ways"),
        "title": "Decode Ways",
        "category": "1d_dp",
        "difficulty": "medium",
        "split": "eval",
        "description": (
            "A message is encoded by mapping 'A' to 1 through 'Z' to 26. "
            "Given a string s of digits, return the number of ways to decode it.\n"
            "Write a Python function: def solve(s: str) -> int"
        ),
        "test_cases": [
            ({"s": "12"}, 2),
            ({"s": "226"}, 3),
            ({"s": "06"}, 0),
            ({"s": "11106"}, 2),
            ({"s": "10"}, 1),
            ({"s": "2101"}, 1),
        ],
    },
    {
        "id": make_id("dp", "1d", "longest_increasing_subsequence"),
        "title": "Longest Increasing Subsequence",
        "category": "1d_dp",
        "difficulty": "medium",
        "split": "eval",
        "description": (
            "Given an integer array nums, return the length of the longest strictly increasing subsequence.\n"
            "Write a Python function: def solve(nums: list) -> int"
        ),
        "test_cases": [
            ({"nums": [10, 9, 2, 5, 3, 7, 101, 18]}, 4),
            ({"nums": [0, 1, 0, 3, 2, 3]}, 4),
            ({"nums": [7, 7, 7, 7, 7, 7, 7]}, 1),
        ],
    },
    {
        "id": make_id("dp", "1d", "word_break"),
        "title": "Word Break",
        "category": "1d_dp",
        "difficulty": "medium",
        "split": "test",
        "description": (
            "Given a string s and a list wordDict, return True if s can be segmented into "
            "space-separated words all from wordDict.\n"
            "Write a Python function: def solve(s: str, wordDict: list) -> bool"
        ),
        "test_cases": [
            ({"s": "leetcode", "wordDict": ["leet", "code"]}, True),
            ({"s": "applepenapple", "wordDict": ["apple", "pen"]}, True),
            ({"s": "catsandog", "wordDict": ["cats", "dog", "sand", "and", "cat"]}, False),
            ({"s": "cars", "wordDict": ["car", "ca", "rs"]}, True),
            ({"s": "a" * 30 + "b", "wordDict": ["a", "aa", "aaa", "aaaa", "aaaaa"]}, False),
        ],
    },
    {
        "id": make_id("dp", "1d", "jump_game_ii"),
        "title": "Jump Game II",
        "category": "1d_dp",
        "difficulty": "medium",
        "split": "test",
        "description": (
            "Given an array nums where nums[i] is the maximum jump length from index i, "
            "return the minimum number of jumps to reach the last index.\n"
            "Write a Python function: def solve(nums: list) -> int"
        ),
        "test_cases": [
            ({"nums": [0]}, 0),
            ({"nums": [2, 3, 1, 1, 4]}, 2),
            ({"nums": [2, 3, 0, 1, 4]}, 2),
            ({"nums": [1, 1, 1, 1]}, 3),
            ({"nums": [5, 4, 3, 2, 1, 0]}, 1),
        ],
    },
    {
        "id": make_id("dp", "1d", "arithmetic_slices"),
        "title": "Arithmetic Slices",
        "category": "1d_dp",
        "difficulty": "medium",
        "split": "test",
        "description": (
            "A subarray of length at least 3 is arithmetic if the difference between consecutive "
            "elements is constant. Given nums, return the number of arithmetic subarrays.\n"
            "Write a Python function: def solve(nums: list) -> int"
        ),
        "test_cases": [
            ({"nums": [1, 2, 3, 4]}, 3),
            ({"nums": [1]}, 0),
            ({"nums": [1, 2, 3, 8, 9, 10]}, 2),
            ({"nums": [7, 7, 7, 7]}, 3),
            ({"nums": [1, 3, 5, 7, 9]}, 6),
        ],
    },
]