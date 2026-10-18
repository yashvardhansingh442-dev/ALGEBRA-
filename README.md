# Algebra Mastery 🧮

An open-source, community-built algebra curriculum: free, plain-language, and structured so you always know what to learn next. It comes with a practice-problem generator and a terminal quiz, so you can read a concept and drill it straight away.

> **Status:** 🚧 Early stage. Modules 01 to 06 (Foundations through Factoring) are written and being refined. Modules 07 to 11 are planned. Contributions welcome!

## Table of contents

- [Why this exists](#why-this-exists)
- [Who this is for](#who-this-is-for)
- [What's inside](#whats-inside)
- [The learning path](#the-learning-path)
- [How to study a module](#how-to-study-a-module)
- [Practice from the terminal](#practice-from-the-terminal)
- [Using the generator as a library](#using-the-generator-as-a-library)
- [Tests and CI](#tests-and-ci)
- [FAQ](#faq)
- [How to contribute](#how-to-contribute)
- [Roadmap](#roadmap)
- [License](#license)

## Why this exists

Most algebra resources are locked behind paywalls, written in dense textbook-speak, or scattered across dozens of YouTube channels with no clear path. This repo aims to be:

- **Free and open.** Fork it, use it, teach with it (see [License](#license)).
- **Plain-language first.** Intuition before notation. Every concept starts with *why* before *how*.
- **Structured.** A single path from "what is a variable" toward systems of equations, with each module building on the last.
- **Honest about mistakes.** Every topic has a "common mistakes" page, because that is usually where people actually get stuck.
- **Reviewed for accuracy.** Contributions are checked for correctness before merging (see [CONTRIBUTING.md](CONTRIBUTING.md)).
- **Backed by code.** The practice generator builds every problem from a known answer, and its test suite runs on every PR, so "correct" is checked by machine and not just eyeballed.

## Who this is for

| You are... | Start here |
|---|---|
| Learning algebra from scratch | [Module 01: Foundations](curriculum/01-foundations/README.md), then go in order |
| Studying for a test on one topic | Jump straight to that module. Each is self-contained, with a "what's next" pointer at the end |
| Rusty and want a refresher | Skim a module's `README.md`, then try its `practice-problems.md` blind. Only read on if you get stuck |
| A teacher or tutor | Fork it. Use the problems as-is or as templates, and use the CLI for quick in-class drills |
| A developer who wants to help | The generator in [`tools/`](tools/README.md) is small and easy to extend with new topics |

## What's inside

```
ALGEBRA--main/
├── curriculum/                  ← the written course
│   ├── 01-foundations/
│   ├── 02-linear-equations/
│   ├── 03-inequalities/
│   ├── 04-functions/
│   ├── 05-polynomials/
│   └── 06-factoring/
├── tools/                       ← practice tooling (Python, standard library only)
│   ├── cli.py                   ← terminal quiz runner
│   ├── algebra_tools/
│   │   └── generator.py         ← problem generator + answer checker
│   └── README.md                ← library usage, adding new topics
├── tests/
│   └── test_generator.py        ← test suite for the generator
├── .github/workflows/ci.yml     ← runs tests + link check on every PR
├── CONTRIBUTING.md
├── requirements.txt             ← pytest (only needed to run the tests)
└── README.md
```

Every topic folder inside `curriculum/` uses the same five files. Folder names are **lowercase and hyphenated** (`02-linear-equations`, never `02-Linear-Equations`) so they don't collide on case-sensitive systems like Linux and GitHub.

```
0X-topic-name/
├── README.md             ← the concept, explained in plain language
├── worked-examples.md    ← fully worked, step-by-step problems (5 per module)
├── practice-problems.md  ← 15 problems per module, tiered easy / medium / hard
├── solutions.md          ← kept separate so problems can be used "blind"
└── common-mistakes.md    ← misconceptions people actually run into
```

## The learning path

| # | Module | What you learn | Status |
|---|--------|----------------|--------|
| 01 | [Foundations](curriculum/01-foundations) | Integers and negative-number arithmetic, order of operations (PEMDAS), what a variable is | 🟢 In progress |
| 02 | [Linear Equations](curriculum/02-linear-equations) | What makes an equation linear, isolating x, variables on both sides, equations with fractions, special cases | 🟢 In progress |
| 03 | [Inequalities](curriculum/03-inequalities) | The flip-the-sign rule for negatives, solving like equations, graphing on a number line, compound inequalities | 🟢 In progress |
| 04 | [Functions](curriculum/04-functions) | What a function is, `f(x)` notation, evaluating, domain, range, a preview of composition | 🟢 In progress |
| 05 | [Polynomials](curriculum/05-polynomials) | Terms and degree, classifying polynomials, adding/subtracting, multiplying by a monomial, FOIL | 🟢 In progress |
| 06 | [Factoring](curriculum/06-factoring) | GCF, `x² + bx + c`, difference of squares, perfect square trinomials, `ax² + bx + c`, a full factoring checklist | 🟢 In progress |
| 07 | Rational Expressions | | ⬜ Not started |
| 08 | Exponents & Radicals | | ⬜ Not started |
| 09 | Quadratics | | ⬜ Not started |
| 10 | Systems of Equations | | ⬜ Not started |
| 11 | Word Problems | | ⬜ Not started |

**How the modules connect:** 01 gives you the arithmetic and notation habits everything else relies on. 02 and 03 are the core equation-solving skill (03 is 02 plus one new rule). 04 introduces the language of functions. 05 and 06 are two sides of the same coin: multiplying polynomials out, then factoring them back apart.

## How to study a module

A routine that works for most people:

1. **Read the module `README.md`.** Short sections, each with an inline example. Don't skip the "what's next" note at the end.
2. **Work through `worked-examples.md` with a pencil.** Cover the solution, try each step yourself, then compare.
3. **Read `common-mistakes.md` before you practice, not after.** Most lost marks come from a handful of repeated errors.
4. **Do `practice-problems.md` blind.** Start with Easy, then Medium, then Hard. Don't open the solutions yet.
5. **Check against `solutions.md`.** For any wrong answer, find the exact line where your working diverged.
6. **Drill with the CLI** (below) until the module feels automatic, then move on.

## Practice from the terminal

Needs Python 3.9+ and nothing else. The CLI uses only the standard library, so there is nothing to install.

```bash
python tools/cli.py --topic linear-equations --difficulty medium --count 10
```

| Flag | Values | Default |
|---|---|---|
| `--topic` | `foundations`, `linear-equations` | `foundations` |
| `--difficulty` | `easy`, `medium`, `hard` | `easy` |
| `--count` | any number of problems, at least 1 | `5` |

Type your answer and press Enter, or type `q` to quit. Integers, decimals, and fractions (`3/4`, `1 / 2`) are all accepted. The final score counts only the problems you actually attempted.

**What a session looks like:**

```
Q1. Solve: 8x - 1 = 5x - 4
Your answer (or 'q' to quit): 3
❌ Not quite. Correct answer: -1
   Working:
     Start with: 8x - 1 = 5x - 4
     Move the x terms to the left (subtract 5x on both sides): 3x - 1 = -4
     Move the constant to the right (add 1 on both sides): 3x = -3
     Divide both sides by 3: x = -1

Score: 0/1
```

**How the problems are generated.** For linear equations, the generator picks the answer `x` first, then builds `ax + b = cx + d` around it (solving for `d`). Every problem therefore has a clean, checkable answer by construction, and the step-by-step working is generated from the same numbers. Easy uses positive coefficients, while medium and hard include negatives and larger ranges.

## Using the generator as a library

```python
from algebra_tools.generator import generate, Difficulty

problem = generate("linear-equations", difficulty=Difficulty.HARD, seed=42)
print(problem.prompt)           # the equation as text
print(problem.check("10"))      # True or False
print(problem.answer_display()) # "10", or a fraction like "-3/4"
print(problem.solution_text())  # step-by-step working
```

Passing a `seed` makes output reproducible, which is useful for worksheets and tests. The generator uses its own random instance, so it never disturbs your program's global random state. To add a new topic, see [`tools/README.md`](tools/README.md).

## Tests and CI

```bash
pip install -r requirements.txt   # just pytest
python -m pytest tests/ -v
```

The test suite covers answer checking (ints, decimals, fractions, garbage input), difficulty validation, reproducibility with seeds, formatting edge cases, and a round-trip correctness check across many seeds for every difficulty.

[CI](.github/workflows/ci.yml) runs on every push and pull request to `main`. It runs the tests on Python 3.9, 3.11, and 3.12, and checks the relative links in `curriculum/` for breakage.

## FAQ

**Do I need to install anything to read the curriculum?**
No. It is plain Markdown, so you can read it on GitHub or in any editor.

**Why are solutions in a separate file?**
So you can use the problems "blind" for self-testing, or hand them out without answers.

**Can I use this in my class or tutoring?**
Yes. Content is CC-BY-SA 4.0: credit the project and share your adaptations under the same license.

**I found a wrong answer. What do I do?**
Open an issue, or fix it and send a PR. Accuracy matters more than anything else here, and a report helps even if you don't want to fix it yourself.

**Can I add a topic?**
Yes. Follow the five-file template for the written module, and see [`tools/README.md`](tools/README.md) if you also want a generator for it.

## How to contribute

Read [CONTRIBUTING.md](CONTRIBUTING.md). Good ways to start, from easiest up:

| Contribution | Difficulty |
|---|---|
| Fix a typo or an unclear sentence | 🟢 Easy |
| Add practice problems to an existing module | 🟢 Easy to medium |
| Write a "common mistakes" entry | 🟡 Medium |
| Add a generator for a new topic, with tests | 🔴 Involved |
| Write a full new module from the template | 🔴 Involved |

Check the Issues tab for anything labeled `good-first-issue`. Rules in short: accuracy over speed, plain language first, follow the template, one concept per PR.

## Roadmap

- [ ] Finish and review modules 01 to 06 (v0.1)
- [ ] Module 07: Rational Expressions
- [ ] Module 08: Exponents & Radicals
- [ ] Module 09: Quadratics
- [ ] Module 10: Systems of Equations
- [ ] Module 11: Word Problems
- [ ] Visual and geometric explainer diagrams
- [ ] Generators for more topics (inequalities, quadratics, and so on)

## License

- **Code** (`tools/`, `tests/`): MIT
- **Written content** (`curriculum/`: explanations, problems, solutions): CC-BY-SA 4.0. Free to reuse and adapt; credit the project and share alike.
