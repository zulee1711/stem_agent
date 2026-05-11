# Stem Agent for Dynamic Programming Problem Solving

## Summary

This project implements a small stem agent that specializes itself into a dynamic programming problem solver. The agent begins as a minimal executor that only knows a domain label: dynamic programming problem solving. It then scouts the problem space, probes sample tasks, measures its own failures, mutates its internal strategy, and freezes when it reaches a performance threshold. A safeguard rolls back mutations that regress performance.

The goal is not to build a universal agent. The goal is to show a bounded self-specialization loop where an agent becomes useful for one technical task family through its own evaluation process.

## Scope

The scope of this project is intentionally narrow. I focus on dynamic programming coding problems rather than general software engineering. This keeps the task family small enough to run end to end while still requiring algorithmic reasoning, code generation, execution, and evaluation.

The stem agent does not train model weights. Instead, it evolves its prompt-level architecture and execution strategy. Its mutable state includes a system prompt, known dynamic programming patterns, strategy notes, probe score, evaluation score, generation number, and a few-shot memory store.

The project evaluates whether a minimal agent can become more specialized through a controlled loop:

1. Scout the domain.
2. Probe representative problems.
3. Measure failures.
4. Mutate the solving strategy.
5. Validate the mutation.
6. Freeze when performance is good enough.

This makes the project a prototype of agent specialization rather than a production coding assistant.

## Task Domain

The task domain is dynamic programming problem solving. Each task is a coding problem with a natural language description, a required Python function signature, a problem category, a difficulty label, a split label, and unit tests.

The current problem bank is organized under the dynamic programming domain. Problem categories can include:

1. One dimensional dynamic programming.
2. Two dimensional dynamic programming.
3. Knapsack and subset dynamic programming.
4. Interval dynamic programming.
5. Sequence dynamic programming.
6. State machine dynamic programming.
7. Tree dynamic programming.
8. Bitmask dynamic programming.

I chose this domain because dynamic programming sits between applied mathematics and computer science. Solving these problems requires identifying state, recurrence, base cases, constraints, and edge cases. This makes the domain a good fit for a stem agent because the agent has to learn a repeatable problem-solving structure rather than only generate code directly.

The problem bank is split into three groups:

1. Probe problems: used during differentiation.
2. Evaluation problems: used for self-evaluation and specialization checkpoints.
3. Test problems: held out until the final before and after comparison.

The final test split is not used during evolution.

## Architecture

The agent architecture has three main phases: Scout, Differentiate, and Specialize.

### Phase 1: Scout

The agent starts with the domain label dynamic programming problem solving. It asks the language model to produce a taxonomy of dynamic programming patterns, including key recurrence ideas, common pitfalls, and pseudocode templates.

From this scouting step, the agent builds its initial internal state. This state acts like the agent genome. It contains:

1. A system prompt.
2. A list of known patterns.
3. A general solving strategy.
4. A generation counter.
5. Probe and evaluation scores.
6. A few-shot store for solved examples.

The output of this phase is not a final solver. It is an initial strategy that the agent can test and improve.

### Phase 2: Differentiate

The agent runs on probe problems. For each problem, it generates a Python solve function, extracts the code, executes it against unit tests, and records the pass rate.

The executor runs generated code in a subprocess with a timeout. This provides a simple safety boundary and a measurable signal. The result includes the number of passed tests, total tests, pass rate, runtime, and error messages.

The agent groups results by category. If a category performs poorly, it asks the language model to diagnose the failure and propose a strategy mutation. A mutation can add category-specific rules, revise the solving protocol, or add more explicit instructions about base cases, bounds, recurrence, or iteration order.

The agent also stores successful probe solutions in a few-shot memory store. Later, when solving a new problem in the same category, it can inject relevant solved examples into the prompt.

### Phase 3: Specialize

After differentiation, the agent evaluates itself on the evaluation set. If its pass rate reaches the threshold, it freezes and becomes the specialized solver. If it does not reach the threshold, it continues evolving until the generation limit is reached.

The safeguard is a rollback rule. If a mutation causes the evaluation score to drop more than the allowed threshold, the agent restores the previous system prompt and rejects the mutation. This mirrors the biological checkpoint idea: the agent can transform, but harmful transformations should not become permanent.

### Final Test

After the agent freezes, it is evaluated on the held-out test set. This result is compared against a baseline agent that uses a weaker model with no dynamic programming-specific scaffolding.

## Evaluation Method

The main evaluation is a before and after comparison.

The before system is the baseline agent. It receives the same problem descriptions but does not scout the domain, store few-shot examples, mutate its strategy, or use a dynamic programming-specific solving protocol.

The after system is the evolved stem agent. It has gone through the Scout, Differentiate, and Specialize phases before being tested.

The primary metric is unit-test pass rate:

```text
pass rate = passed test cases / total test cases
```

For each generated solution, the system runs the solve function against all test cases for the problem. The experiment records:

1. Overall pass rate.
2. Per-problem pass rate.
3. Per-problem errors.
4. Runtime in milliseconds.
5. Evolution history.
6. Final system prompt.
7. Few-shot examples stored by the agent.

Each run saves its results under a timestamped folder:

```text
results/yymmdd/HHMMSS/
```

This keeps experiment outputs separated and reproducible.

## What the System Produces

Each run produces three main output files:

```text
experiment_results.json
final_system_prompt.txt
few_shot_store.json
```

The experiment results file stores the baseline score, evolved score, improvement, per-problem outcomes, and evolution history. The final system prompt file stores the agent state after specialization. The few-shot store file stores successful examples collected during differentiation.

These files make it possible to inspect not only the final score, but also how the agent changed along the way.

## What Failed or Surprised Me

The first version of the project did not show improvement because the baseline model already solved all held-out test cases. This was a useful failure. It showed that a stem agent needs meaningful environmental pressure in order to demonstrate specialization. If the baseline already saturates the benchmark, there is no visible reason for the agent to evolve.

To address this, I changed the setup so that the baseline uses a weaker model with no scaffolding, while the stem agent uses a richer specialization loop. I also structured the problem bank so it can grow by category and added split labels directly into each problem. This makes it easier to add harder hidden tests later.

Another limitation is that the current mutations are prompt-level mutations. The agent changes its solving protocol and few-shot context, but it does not yet generate new Python tools or rewrite its runtime architecture. This is a useful first step, but it is not full autonomous agent design.

## What I Would Do With More Time

With more time, I would extend the project in four directions.

First, I would add more problems and harder hidden test cases. The current framework supports more categories, but the benchmark should be larger to make results more meaningful.

Second, I would add runtime repair using actual failed test cases during evaluation. The current repair loop checks syntax, but it does not fully repair semantic failures at solve time.

Third, I would let the agent mutate more than the prompt. For example, it could add or remove modules such as a complexity checker, a recurrence verifier, or a test generator.

Fourth, I would repeat the same framework on a second task family, such as graph algorithms or probability word problems. That would test whether the stem-agent loop is reusable beyond dynamic programming.
