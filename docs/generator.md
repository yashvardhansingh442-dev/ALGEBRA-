# Tools

Code that powers interactive practice — not required to use the curriculum, but useful for drilling.

## What's here

- `src/algebra_tools/generator.py` — generates randomized, guaranteed-solvable practice problems for Foundations (arithmetic) and Linear Equations, and checks user answers (accepts ints, decimals, or fractions like `"3/4"`)
- `src/algebra_tools/cli.py` (run as `python -m algebra_tools`, or `algebra` once installed) — a command-line quiz runner built on top of the generator
- `scripts/check_links.py` — checks every relative Markdown link (files, folders, `#anchors`); CI runs it

## Quickstart

```bash
pip install -e ".[dev]"   # optional: adds the `algebra` command and pytest
python -m algebra_tools --topic linear-equations --difficulty medium --count 10
```

## How the generator guarantees correctness

For linear equations, the generator works **backwards**: it picks the answer `x` first, then builds an equation `ax + b = cx + d` that produces it. That means every generated problem is checked-correct by construction — no chance of accidentally generating something unsolvable. This is verified by `tests/test_generator.py`, which round-trips hundreds of random seeds across all difficulties.

## Using it as a library

```python
from algebra_tools.generator import generate, Difficulty

problem = generate("linear-equations", difficulty=Difficulty.HARD, seed=42)   # "hard" also works
print(problem.prompt)           # the equation as text
print(problem.check("10"))      # True or False (exact: "1 / 2" and "0.5" pass for 1/2, 0.33333 fails for 1/3)
print(problem.answer_display()) # "10", or a fraction like "-3/4"
print(problem.solution_text())  # step-by-step working
```

## Adding a new topic generator

1. Add a `generate_<topic>(difficulty, seed)` function in `generator.py` that returns a `Problem` with `steps`. Use a local `random.Random(seed)`, never the global `random` functions
2. Register it in `TOPIC_GENERATORS`
3. Add tests in `tests/test_generator.py` — at minimum, a round-trip correctness check across multiple seeds, like the linear equations test does
4. Wire it into `cli.py`'s `--topic` choices (this happens automatically since it reads from `TOPIC_GENERATORS`)

See `CONTRIBUTING.md` for PR guidelines.

