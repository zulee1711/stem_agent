"""
Stem Agent - DP Problem Solver

Lifecycle:
1. Scout - gather domain knowledge about dynamic programming categories via LLM
2. Differentiate - probe sammple problems, identify failure patterns, mutate strategy
3. Specialize - self-evaluate on evaluation set, freeze if threshold met, else iterate

Safeguard:
- Each mutation is validated before committed
"""

import os
import json
import copy
import re
import logging
from dataclasses import dataclass, field

from openai import OpenAI

from executor import run_solution, extract_code, extract_json

#%%
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

#%%
@dataclass
class AgentState:
    """
    Mutable identity of the agent, what it knows and how it thinks
    """
    system_prompt: str = ""
    known_patterns: list[str] = field(default_factory=list)
    strategy_notes: str = ""
    generation: int = 0
    eval_score: float = 0.0
    probe_score: float = 0.0
    few_shot_store: dict = field(default_factory=dict)

    def snapshot(self) -> "AgentState":
        return copy.deepcopy(self)


#%%
class Agent:
    """
    A stem agent for the domain "dynamic programming problem solving"
    Starts undifferentiated, evolves through scout -> differentiate -> specialize
    """

    # Stopping criteria
    PASS_THRESHOLD = 0.8  # freeze if eval >= this rate
    MAX_GENERATIONS = 3  # never evolve more than this many times
    SAFEGUARD_MIN_DELTA = -0.10  # rollback
    MAX_REPAIR_ATTEMPTS = 2  # syntax-repair retries inside solve()

    def __init__(
            self,
            task_class: str = "dynamic programming problem solving",
                 ):
        self.task_class = task_class
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.state = AgentState()
        self.history: list[dict] = []  # evolution log

    def evolve(
            self,
            probe_problems: list,
            eval_problems: list,
               ) -> dict:
        """
        Run the full lifecycle from stem to specialized
        probe_problems : problems used during differentiation (agent can see these)
        eval_problems : problems used for self-evaluation (held out from probing)
        Return evolution log
        """
        logger.info(f"Starting STEM AGENT task class: {self.task_class}")

        # Phase 1: Scout
        self._phase_scout()

        # Iterative differentiation loop
        for gen in range(1, self.MAX_GENERATIONS + 1):
            self.state.generation = gen

            logger.info(f"Generation: {gen}")

            # Phase 2: Differentiate
            self._phase_differentiate(probe_problems)

            # Phase 3: Specialize check
            done = self._phase_specialize(eval_problems)

            self._log_generation()

            if done:
                logger.info(f"Threshold reached at generation: {gen}")
                break
        else:
            logger.info("Max generations reached, use best accumulated state.")

        return self.history

    def solve(self, problem_description: str, category: str = "unknown") -> str:
        """
        Solve one problem with the current specialized state.

        Steps:
          1. Inject category-matched few-shot examples into the system prompt.
          2. Force a chain-of-thought scratchpad before the code.
          3. Run a syntax-repair loop if the returned code has parse errors.

        Returns a raw Python code string (solve() function).
        """
        few_shots = self._get_few_shots(category)
        system = self._build_solve_system(few_shots)

        # Step 1: forced chain-of-thought
        cot_prompt = (
            f"{problem_description}\n\n"
            "First write a SCRATCHPAD section:\n"
            "  - Pattern: which DP type is this?\n"
            "  - State: what does dp[i] (or dp[i][j]) represent?\n"
            "  - Recurrence: write it mathematically\n"
            "  - Base cases: list them\n"
            "  - Edge cases: empty input, n=0, etc.\n\n"
            "Then write the Python solve() function."
        )

        raw = self._call_llm(system=system, user=cot_prompt, temperature=0.15, max_tokens=1200)
        code = extract_code(raw)

        # Step 2: self-repair loop
        for attempt in range(self.MAX_REPAIR_ATTEMPTS):
            syntax_ok, syntax_err = self._check_syntax(code)
            if not syntax_ok:
                logger.debug("repair attempt %d: %s", attempt + 1, syntax_err[:80])

                repair_prompt = (
                    f"Your previous solution had a syntax error:\n{syntax_err}\n\n"
                    f"Original problem:\n{problem_description}\n\n"
                    "Fix it and return ONLY the corrected Python solve() function."
                )
                raw = self._call_llm(system=system, user=repair_prompt,
                                     temperature=0.2, max_tokens=800)
                code = extract_code(raw)
            else:
                break

        return code

    ## Phase 1: Scout
    def _phase_scout(self):
        """
        Gathering domain knowledge about dynamic programming problem categories, common patterns, and solution strategies via LLM exploration.
        """
        logger.info("Phase 1: Scout - Gathering domain knowledge")

        taxonomy_prompt = (
            f"You are a senior programmer and CS educator.\n"
            f"Your job is to map out the full landscape of '{self.task_class}' problems.\n"
            "Return a JSON object with this exact structure (raw JSON only, no markdown fences):\n"
            "{\n"
            '  "categories": [\n'
            "    {\n"
            '      "name": "<name>",\n'
            '      "key_insight": "<the core recurrence idea in one sentence>",\n'
            '      "common_pitfalls": ["<pitfall>"],\n'
            '      "template": "<3-5 line Python pseudocode template for this pattern>"\n'
            "    }\n"
            "  ],\n"
            '  "general_strategy": "<how to approach ANY DP problem: 3-4 sentences>"\n'
            "}\n"
            "Include at minimum: 1D DP, 2D DP, knapsack, interval DP, sequence DP, "
            "state-machine DP, bitmask DP, tree DP."
        )

        raw = self._call_llm(
            system="You are a CS curriculum expert.",
            user=taxonomy_prompt,
            temperature=0.3,
            max_tokens=2500,
        )
        taxonomy = extract_json(raw)

        categories = taxonomy.get("categories", [])
        if not categories:
            logger.warning("Scout got empty taxonomy - using fallback")
            categories = self._fallback_taxonomy()

        self.state.known_patterns = [c["name"] for c in categories]
        general_strategy = taxonomy.get("general_strategy", "")

        logger.info(
            "Discovered %d categories: %s",
            len(categories),
            ", ".join(self.state.known_patterns),
        )

        pattern_block = "\n".join(
            f"{c['name']}: {c['key_insight']}\n"
            f"Template:\n{self._indent(c.get('template', ''), 4)}"
            for c in categories
        )

        self.state.system_prompt = (
            "You are a specialized dynamic programming solver.\n"
            "Your task: read a DP problem, reason step by step, then write correct Python.\n\n"
            "## DP Pattern Library\n"
            f"{pattern_block}\n\n"
            "## General strategy\n"
            f"{general_strategy}\n\n"
            "## Solving protocol\n"
            "1. IDENTIFY: label the DP pattern (1D / 2D / knapsack / interval / sequence / "
            "state-machine / bitmask / tree)\n"
            "2. STATE: define dp[i] or dp[i][j] precisely as a comment in your code\n"
            "3. RECURRENCE: write it as a comment before the loop\n"
            "4. BASE CASES: initialize explicitly\n"
            "5. EDGE CASES: handle empty input, n=0, single-element arrays\n"
            "6. BOUNDS: never access dp[i-1] without checking i > 0\n\n"
            "## Output format\n"
            "Return ONLY valid Python code. The function must be named solve().\n"
            "No markdown fences. No explanations outside the code."
        )

        self.state.strategy_notes = general_strategy
        logger.info("System prompt built (%d chars).", len(self.state.system_prompt))

    ## Phase 2: Differentiate
    def _phase_differentiate(self, probe_problems: list):
        """
        Run the agent on probe problems. Collect per-category pass rates,
        store solved examples as few-shot memory, then ask the LLM to
        diagnose failures and propose a targeted prompt mutation.
        """
        logger.info("Phase 2: Differentiate - Probing %d problems", len(probe_problems))

        results_by_category: dict[str, list[float]] = {}
        raw_errors: list[str] = []
        solved_examples: list[dict] = []

        for prob in probe_problems:
            code = self.solve(prob["description"], category=prob["category"])
            result = run_solution(code, prob["test_cases"])
            cat = prob["category"]
            results_by_category.setdefault(cat, []).append(result["pass_rate"])

            if result["pass_rate"] == 1.0:
                solved_examples.append({
                    "category": cat,
                    "problem": prob["description"][:400],
                    "solution": code[:600],
                })
            else:
                raw_errors.extend(result["errors"][:2])

        # Store few-shot examples after processing all problems (not inside the loop)
        for ex in solved_examples:
            cat = ex["category"]
            self.state.few_shot_store.setdefault(cat, [])
            if len(self.state.few_shot_store[cat]) < 2:
                self.state.few_shot_store[cat].append(ex)

        cat_scores = {
            cat: sum(rates) / len(rates)
            for cat, rates in results_by_category.items()
        }
        overall = sum(cat_scores.values()) / len(cat_scores) if cat_scores else 0.0
        self.state.probe_score = overall

        weak_cats = [cat for cat, score in cat_scores.items() if score < 0.6]

        logger.info(
            "Probe pass-rate: %.1f%% | Weak categories: %s",
            overall * 100,
            weak_cats or "none",
        )
        logger.info(
            "Few-shot store: %d categories with examples",
            len(self.state.few_shot_store),
        )

        if weak_cats or raw_errors:
            mutation = self._ask_for_mutation(weak_cats, raw_errors, cat_scores)
            if mutation:
                self._apply_mutation(mutation)

    def _ask_for_mutation(self, weak_cats: list, errors: list, cat_scores: dict) -> dict:
        """
        Ask the LLM to diagnose failures in the current system prompt
        and return a targeted mutation as a JSON object.
        """
        scores_str = "\n".join(f"  {c}: {s:.0%}" for c, s in cat_scores.items())
        error_sample = "\n".join(errors[:5]) or "none"

        prompt = (
            "You are improving a DP-solving AI agent.\n\n"
            "Current system prompt:\n"
            "---\n"
            f"{self.state.system_prompt[:1500]}\n"
            "---\n\n"
            f"Category scores:\n{scores_str}\n\n"
            f"Weak categories: {weak_cats}\n\n"
            f"Error samples:\n{error_sample}\n\n"
            "Return a JSON object (raw JSON, no markdown fences):\n"
            "{\n"
            '  "diagnosis": "<why is the agent failing>",\n'
            '  "targeted_additions": "<concrete rules for the weak categories>",\n'
            '  "revised_protocol": "<full replacement for the ## Solving protocol section>"\n'
            "}"
        )

        raw = self._call_llm(
            system="You are an AI systems engineer improving an agent.",
            user=prompt,
            temperature=0.4,
            max_tokens=1500,
        )
        result = extract_json(raw)
        if not result:
            logger.warning("Mutation JSON parse failed -- skipping mutation.")
        return result

    def _apply_mutation(self, mutation: dict):
        """Apply a validated mutation dict to the current system prompt."""
        diagnosis = mutation.get("diagnosis", "")
        additions = mutation.get("targeted_additions", "")
        new_protocol = mutation.get("revised_protocol", "")

        logger.info("Mutation diagnosis: %s", diagnosis[:120])

        if additions:
            tag = f"## Pattern-specific rules (gen {self.state.generation})"
            if tag not in self.state.system_prompt:
                self.state.system_prompt = self.state.system_prompt.replace(
                    "## Output format",
                    f"{tag}\n{additions}\n\n## Output format",
                )

        if new_protocol and "## Solving protocol" in self.state.system_prompt:
            self.state.system_prompt = re.sub(
                r"## Solving protocol.*?(?=## )",
                f"{new_protocol}\n\n",
                self.state.system_prompt,
                flags=re.DOTALL,
            )


    ## Phase 3: Specialize
    def _phase_specialize(self, eval_problems: list) -> bool:
        """
        Evaluate the current agent state on the held-out eval set.
        Freeze (return True) if pass-rate meets PASS_THRESHOLD.
        Roll back and return False if pass-rate regressed beyond SAFEGUARD_MIN_DELTA.
        """
        logger.info("Phase 3: Specialize - Evaluating on %d problems", len(eval_problems))

        prev_score = self.state.eval_score

        passed = total = 0
        for prob in eval_problems:
            code = self.solve(prob["description"], category=prob["category"])
            result = run_solution(code, prob["test_cases"])
            passed += result["passed"]
            total += result["total"]

        new_score = passed / total if total else 0.0
        logger.info("Eval: %.1f%% (%d/%d)", new_score * 100, passed, total)

        delta = new_score - prev_score
        if self.state.generation > 1 and delta < self.SAFEGUARD_MIN_DELTA:
            logger.warning(
                "ROLLBACK - score dropped %.1f%% which exceeds safeguard threshold.",
                abs(delta) * 100,
            )
            if self.history:
                self.state.system_prompt = self.history[-1]["system_prompt_snapshot"]
            self.state.eval_score = prev_score
            return False

        self.state.eval_score = new_score
        return new_score >= self.PASS_THRESHOLD

    ## Helper
    def _build_solve_system(self, few_shots: list[dict]) -> str:
        """Append few-shot examples to the base system prompt."""
        system = self.state.system_prompt
        if few_shots:
            examples = "\n\n".join(
                f"Example ({ex['category']}):\n"
                f"Problem: {ex['problem'][:300]}\n"
                f"Solution:\n```python\n{ex['solution']}\n```"
                for ex in few_shots
            )
            system = system + f"\n\n## Solved examples (use as reference)\n{examples}"
        return system

    def _get_few_shots(self, category: str) -> list[dict]:
        """Retrieve up to 2 solved examples for this category."""
        return self.state.few_shot_store.get(category, [])[:2]

    def _check_syntax(self, code: str) -> tuple[bool, str]:
        """Quick syntax check without executing."""
        import ast
        try:
            ast.parse(code)
            return True, ""
        except SyntaxError as e:
            return False, str(e)

    def _call_llm(
        self,
        system: str,
        user: str,
        temperature: float = 0.2,
        max_tokens: int = 1000,
    ) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def _log_generation(self):
        self.history.append({
            "generation": self.state.generation,
            "probe_score": self.state.probe_score,
            "eval_score": self.state.eval_score,
            "system_prompt_snapshot": self.state.system_prompt,
            "few_shot_categories": list(self.state.few_shot_store.keys()),
            "known_patterns": list(self.state.known_patterns),
        })

    def _indent(self, text: str, spaces: int) -> str:
        prefix = " " * spaces
        return "\n".join(prefix + line for line in text.splitlines())

    def _fallback_taxonomy(self) -> list[dict]:
        return [
            {
                "name": "1D DP",
                "key_insight": "dp[i] depends on a fixed number of prior states such as dp[i-1] or dp[i-2]",
                "common_pitfalls": ["off-by-one on array size", "forgetting base case for i=0"],
                "template": "dp = [0] * (n + 1)\nfor i in range(1, n + 1):\n    dp[i] = ...\nreturn dp[n]",
            },
            {
                "name": "2D DP",
                "key_insight": "dp[i][j] is derived from dp[i-1][j] and dp[i][j-1] or dp[i-1][j-1]",
                "common_pitfalls": ["wrong initialization of first row/column"],
                "template": (
                    "dp = [[0] * (n + 1) for _ in range(m + 1)]\n"
                    "for i in range(1, m + 1):\n"
                    "    for j in range(1, n + 1):\n"
                    "        dp[i][j] = ..."
                ),
            },
            {
                "name": "knapsack",
                "key_insight": "dp[w] = max value achievable at capacity w; iterate capacity in reverse for 0-1 variant",
                "common_pitfalls": ["iterating capacity forward allows item reuse in 0-1 knapsack"],
                "template": (
                    "dp = [0] * (W + 1)\n"
                    "for w, v in zip(weights, values):\n"
                    "    for cap in range(W, w - 1, -1):\n"
                    "        dp[cap] = max(dp[cap], dp[cap - w] + v)"
                ),
            },
        ]