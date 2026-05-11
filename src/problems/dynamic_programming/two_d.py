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
        "id": make_id("dp", "2d", "unique_paths"),
        "title": "Unique Paths",
        "category": "2d_dp",
        "difficulty": "easy",
        "split": "probe",
        "description": (
            "A robot starts at the top-left corner of an m x n grid and wants to reach "
            "bottom-right. It can only move right or down. How many unique paths are there?\n"
            "Write a Python function: def solve(m: int, n: int) -> int"
        ),
        "test_cases": [
            ({"m": 3, "n": 7}, 28),
            ({"m": 3, "n": 2}, 3),
            ({"m": 7, "n": 3}, 28),
        ],
    },
    {
        "id": make_id("dp", "2d", "minimum_path_sum"),
        "title": "Minimum Path Sum",
        "category": "2d_dp",
        "difficulty": "medium",
        "split": "probe",
        "description": (
            "Given an m x n grid filled with non-negative numbers, find a path from "
            "top-left to bottom-right that minimizes the sum. You can only move right or down.\n"
            "Write a Python function: def solve(grid: list) -> int"
        ),
        "test_cases": [
            ({"grid": [[1, 3, 1], [1, 5, 1], [4, 2, 1]]}, 7),
            ({"grid": [[1, 2, 3], [4, 5, 6]]}, 12),
        ],
    },
    {
        "id": make_id("dp", "2d", "edit_distance"),
        "title": "Edit Distance",
        "category": "2d_dp",
        "difficulty": "hard",
        "split": "eval",
        "description": (
            "Given two strings word1 and word2, return the minimum number of operations "
            "(insert, delete, replace) to convert word1 to word2.\n"
            "Write a Python function: def solve(word1: str, word2: str) -> int"
        ),
        "test_cases": [
            ({"word1": "horse", "word2": "ros"}, 3),
            ({"word1": "intention", "word2": "execution"}, 5),
            ({"word1": "", "word2": "a"}, 1),
        ],
    },
    {
        "id": make_id("dp", "2d", "longest_common_subsequence"),
        "title": "Longest Common Subsequence",
        "category": "2d_dp",
        "difficulty": "medium",
        "split": "eval",
        "description": (
            "Given two strings text1 and text2, return the length of their longest "
            "common subsequence.\n"
            "Write a Python function: def solve(text1: str, text2: str) -> int"
        ),
        "test_cases": [
            ({"text1": "abcde", "text2": "ace"}, 3),
            ({"text1": "abc", "text2": "abc"}, 3),
            ({"text1": "abc", "text2": "def"}, 0),
        ],
    },
    {
        "id": make_id("dp", "2d", "maximal_square"),
        "title": "Maximal Square",
        "category": "2d_dp",
        "difficulty": "medium",
        "split": "test",
        "description": (
            "Given an m x n binary matrix of '0' and '1' strings, find the largest "
            "square containing only 1s and return its area.\n"
            "Write a Python function: def solve(matrix: list) -> int"
        ),
        "test_cases": [
            ({"matrix": [["1","0","1","0","0"],["1","0","1","1","1"],
                          ["1","1","1","1","1"],["1","0","0","1","0"]]}, 4),
            ({"matrix": [["0","1"],["1","0"]]}, 1),
            ({"matrix": [["1"]]}, 1),
        ],
    },
    {
        "id": make_id("dp", "2d", "interleaving_string"),
        "title": "Interleaving String",
        "category": "2d_dp",
        "difficulty": "hard",
        "split": "test",
        "description": (
            "Given s1, s2, and s3, return True if s3 is formed by interleaving s1 and s2.\n"
            "Write a Python function: def solve(s1: str, s2: str, s3: str) -> bool"
        ),
        "test_cases": [
            ({"s1": "aabcc", "s2": "dbbca", "s3": "aadbbcbcac"}, True),
            ({"s1": "aabcc", "s2": "dbbca", "s3": "aadbbbaccc"}, False),
            ({"s1": "", "s2": "", "s3": ""}, True),
        ],
    },
]