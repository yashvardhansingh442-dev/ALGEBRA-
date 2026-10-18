# Tools

Code that powers interactive practice — not required to use the curriculum, but useful for drilling.

## What's here

- `algebra_tools/generator.py` — generates randomized, guaranteed-solvable practice problems for Foundations (arithmetic) and Linear Equations, and checks user answers (accepts ints, decimals, or fractions like `"3/4"`)
- `cli.py` — a command-line quiz runner built on top of the generator

## Quickstart

```bash
pip install -r ../requirements.txt
python tools/cli.py --topic linear-equations --difficulty medium --count 10
```

## How the generator guarantees correctness

For linear equations, the generator works **backwards**: it picks the answer `x` first, then builds an equation `ax + b = cx + d` that produces it. That means every generated problem is checked-correct by construction — no chance of accidentally generating something unsolvable. This is verified by `tests/test_generator.py`, which round-trips hundreds of random seeds across all difficulties.

## Using it as a library

```python
from algebra_tools.generator import generate

problem = generate("linear-equations", difficulty="hard")
print(problem.prompt)           # e.g. "9x + 6 = 4x + 56"
print(problem.check("10"))      # True or False
print(problem.answer_display()) # "10"
```

## Adding a new topic generator

1. Add a `generate_<topic>(difficulty, seed)` function in `generator.py` that returns a `Problem`
2. Register it in `TOPIC_GENERATORS`
3. Add tests in `tests/test_generator.py` — at minimum, a round-trip correctness check across multiple seeds, like the linear equations test does
4. Wire it into `cli.py`'s `--topic` choices (this happens automatically since it reads from `TOPIC_GENERATORS`)

See `CONTRIBUTING.md` for PR guidelines.
