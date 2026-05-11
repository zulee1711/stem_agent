from ..helper import make_id


PROBLEMS = [
    {
        "id": make_id("dp", "bitmask", "traveling_salesman_small"),
        "title": "Traveling Salesman Small",
        "category": "bitmask_dp",
        "difficulty": "hard",
        "split": "test",
        "description": (
            "Given a distance matrix dist where dist[i][j] is the cost from city i to city j, "
            "return the minimum cost to visit all cities exactly once and return to city 0.\n"
            "Write a Python function: def solve(dist: list) -> int"
        ),
        "test_cases": [
            ({"dist": [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]}, 80),
            ({"dist": [[0, 20, 42, 25], [20, 0, 30, 34], [42, 30, 0, 10], [25, 34, 10, 0]]}, 85),
            ({"dist": [[0, 5], [5, 0]]}, 10),
        ],
    },
    {
        "id": make_id("dp", "bitmask", "minimum_cost_connect_points"),
        "title": "Minimum Cost to Connect All Points",
        "category": "bitmask_dp",
        "difficulty": "hard",
        "split": "test",
        "description": (
            "Given points on a 2D plane, the cost to connect two points is Manhattan distance. "
            "Return the minimum cost to connect all points.\n"
            "Write a Python function: def solve(points: list) -> int"
        ),
        "test_cases": [
            ({"points": [[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]}, 20),
            ({"points": [[3, 12], [-2, 5], [-4, 1]]}, 18),
            ({"points": [[0, 0]]}, 0),
        ],
    },
]
