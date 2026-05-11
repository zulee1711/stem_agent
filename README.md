# Stem Agent for Dynamic Programming Problem Solving

## Overview

This project implements a small stem agent that specializes into a dynamic programming problem solver.

The agent begins with only a domain label: dynamic programming problem solving. It then scouts the problem space, probes sample tasks, measures failures, mutates its internal strategy, and freezes when it reaches a performance threshold. A rollback safeguard rejects mutations that reduce validation performance.

The goal is not to build a universal coding agent. The goal is to demonstrate a bounded specialization loop for one task family.

## Repository Structure

```text
.
|-- results/
|-- src/
|   |-- problems/
|   |   |-- __init__.py
|   |   |-- helper.py
|   |   |-- dynamic_programming/
|   |   |   |-- __init__.py
|   |   |   |-- knapsack.py
|   |   |   |-- one_d.py
|   |   |   |-- registry.py
|   |   |   |-- two_d.py
|   |-- agent.py
|   |-- base.py
|   |-- executor.py
|   |-- main.py
|-- test/
|-- README.md
|-- requirements.txt
|-- Writeup.md
```

## Requirements

```text
python == 3.12
```

Python packages are listed in `requirements.txt`.

## Setup

Run these commands from the repository root.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in either the repository root or inside `src`.

```bash
cp src/.env.example src/.env
```

Edit the file so it contains your OpenAI API key.

```text
OPENAI_API_KEY=your_key_here
```

## Run the Experiment

Run the main script from the repository root.

```bash
python src/main.py
```

You can also run it from inside `src`.

```bash
cd src
python main.py
```

## Output

Each run is saved under a timestamped folder.

```text
results/yymmdd/HHMMSS/
```

For example:

```text
results/260511/190108/
```

Each run produces these files:

```text
experiment_results.json
final_system_prompt.txt
few_shot_store.json
```

`experiment_results.json` contains the baseline result, evolved-agent result, improvement value, per-problem results, and evolution history.

`final_system_prompt.txt` contains the final specialized prompt after evolution.

`few_shot_store.json` contains solved examples collected during differentiation.

## Problem Bank

Problems are stored under:

```text
src/problems/dynamic_programming/
```

Each problem has this structure:

```python
{
    "id": "dp.1d.word_break",
    "title": "Word Break",
    "category": "1d_dp",
    "difficulty": "medium",
    "split": "test",
    "description": "...",
    "test_cases": [
        ({"s": "leetcode", "wordDict": ["leet", "code"]}, True),
    ],
}
```

The split field controls how the problem is used:

```text
probe: used during differentiation
eval: used during specialization checkpoints
test: used only for the final comparison
```

The registry combines all problem files and exposes:

```python
get_split("probe")
get_split("eval")
get_split("test")
validate_problem_bank()
```