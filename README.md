# ALGEBRA- 🧮

A free algebra curriculum, a practice generator with exact answer checking, and (in progress) a from-scratch exact-math engine. It is the first module of a larger long-term project, and every later math topic is meant to build on it.

> **Status:** 🚧 Early stage. The curriculum (modules 01-06) and the practice generator are done and tested. The symbolic engine is **planned, not built yet**. See [Roadmap](#roadmap).

## Contents

- [At a glance](#at-a-glance)
- [Quick start](#quick-start)
- [Repo layout](#repo-layout)
- [Curriculum](#curriculum)
- [Practice tools](#practice-tools)
- [Roadmap](#roadmap)
- [Tests and CI](#tests-and-ci)
- [Contributing](#contributing)
- [License](#license)

## At a glance

| Part | What it is | Status |
|---|---|---|
| Curriculum | Six plain-language modules, five files each | 🟢 Written, being refined |
| Generator + CLI | Random problems with step-by-step working, exact answer checking | 🟢 Done, tested on Python 3.9, 3.11, 3.12 |
| Link checker | Verifies every relative Markdown link and `#anchor` | 🟢 Done, runs in CI |
| Symbolic engine | Expand, factor and solve exactly, with no SymPy | ⬜ Planned |
| Optimization example | A constrained problem solved with the engine | ⬜ Planned |

**Design rules:** Python standard library only at runtime. Exact rational arithmetic, never floats, for anything that is checked. Every feature ships with a test that proves it works and one that proves it rejects bad input.

## Quick start

Needs Python 3.9 or newer.

```bash
git clone https://github.com/<your-username>/ALGEBRA-.git
cd ALGEBRA-
pip install -r requirements.txt          # pytest only, needed just for the tests
python tools/cli.py --topic linear-equations --difficulty medium --count 5
python -m pytest tests -q
```

## Repo layout

```
ALGEBRA-/
├── curriculum/            the written course (one folder per module)
├── tools/
│   ├── algebra_tools/     importable package (generator today, symbolic engine next)
│   ├── cli.py             terminal quiz
│   ├── check_links.py     Markdown link checker
│   └── README.md          library usage, how to add a topic
├── tests/                 pytest suite
├── .github/workflows/     CI: tests on 3.9, 3.11, 3.12, plus the link check
├── CONTRIBUTING.md
├── LICENSE
└── requirements.txt
```

## Curriculum

Each module has the same five files: `README.md` (the concept), `worked-examples.md` (5 examples), `practice-problems.md` (15 problems, easy to hard), `solutions.md`, and `common-mistakes.md`. Folder names are lowercase and hyphenated.

| # | Module | You learn |
|---|---|---|
| 01 | [Foundations](curriculum/01-foundations/README.md) | Negative numbers, order of operations, what a variable is |
| 02 | [Linear Equations](curriculum/02-linear-equations/README.md) | Isolating x, variables on both sides, special cases |
| 03 | [Inequalities](curriculum/03-inequalities/README.md) | The sign-flip rule, number lines, compound inequalities |
| 04 | [Functions](curriculum/04-functions/README.md) | `f(x)` notation, domain, range, composition preview |
| 05 | [Polynomials](curriculum/05-polynomials/README.md) | Degree, adding, multiplying, FOIL |
| 06 | [Factoring](curriculum/06-factoring/README.md) | GCF, trinomials, difference of squares, a full checklist |

**How to study a module:** read the README, work the examples with a pencil, read common mistakes, do the practice problems blind, then check the solutions and drill with the CLI.

## Practice tools

**Terminal quiz**

```bash
python tools/cli.py --topic foundations --difficulty easy --count 5
```

| Flag | Values | Default |
|---|---|---|
| `--topic` | `foundations`, `linear-equations` | `foundations` |
| `--difficulty` | `easy`, `medium`, `hard` | `easy` |
| `--count` | 1 or more | `5` |

Answers can be integers, decimals or fractions (`3/4`, `1 / 2`). Checking is exact: `0.33333` is not accepted for 1/3. Type `q` to quit; the score counts only the problems you attempted.

**As a library**

```python
from algebra_tools.generator import generate, Difficulty

problem = generate("linear-equations", difficulty=Difficulty.HARD, seed=42)
print(problem.prompt)           # the equation as text
print(problem.check("15"))      # True or False
print(problem.solution_text())  # step-by-step working
```

A `seed` makes output reproducible. The generator uses its own random instance and never touches your global random state. Problems are built backwards (answer first), so every one is solvable by construction. To add a topic, see [tools/README.md](tools/README.md).

## Roadmap

- [x] Modules 01-06 written
- [x] Generator repaired, exact checking, step-by-step working
- [x] One-root repo layout, CI at the root, tested link checker
- [ ] **Symbolic engine** (`algebra_tools/symbolic/`): parser, expansion, factoring over the rationals, exact linear systems, small nonlinear systems, complex numbers
- [ ] Generator problems validated by the engine, plus CLI commands for it
- [ ] Worked optimization example (Lagrange multipliers solved exactly)
- [ ] Ruff and mypy clean in CI, `ARCHITECTURE.md`
- [ ] Modules 07-11: rational expressions, exponents and radicals, quadratics, systems, word problems

The engine is exact-math infrastructure for later topics (geometry, calculus, linear algebra, optimization). It is a teaching and tooling project, not a general-purpose CAS.

## Tests and CI

```bash
python -m pytest tests -q        # generator and link-checker tests
python tools/check_links.py      # every relative link and anchor in every .md file
```

[CI](.github/workflows/ci.yml) runs both on every push and pull request to `main`.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). Easy starts: fix a typo, verify a solution by re-solving it, add practice problems. Rules in short: accuracy over speed, plain language first, follow the template, one concept per PR.

## License

- **Code** (`tools/`, `tests/`): MIT
- **Written content** (`curriculum/`): CC-BY-SA 4.0. Credit the project and share adaptations alike.
