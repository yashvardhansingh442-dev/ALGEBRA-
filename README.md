# Algebra Mastery 🧮

An open-source, community-built curriculum for learning algebra from the ground up — free, plain-language, and built by learners for learners.

> **Status:** 🚧 Early stage — Foundations, Linear Equations, Inequalities, and Functions modules in progress. Contributions welcome!

## Why this exists

Most algebra resources are either locked behind paywalls, written in dense textbook-speak, or scattered across a hundred different YouTube channels with no clear path. This repo aims to be:

- **Free and open** — MIT/CC-BY-SA licensed, fork it, use it, teach with it
- **Plain-language first** — intuition before notation
- **Structured** — a clear path from "what is a variable" to solving systems of equations
- **Honest about mistakes** — every topic includes a "common mistakes" section, because that's usually where people actually get stuck
- **Community-verified** — every problem and solution is reviewed before merging
- **Backed by code, not just text** — a practice-problem generator with a real test suite, so "correct" is enforced by CI, not just eyeballed

## Learning path

| # | Topic | Status |
|---|-------|--------|
| 01 | [Foundations](curriculum/01-foundations) (integers, order of operations, variables) | 🟢 In progress |
| 02 | [Linear Equations](curriculum/02-linear-equations) | 🟢 In progress |
| 03 | [Inequalities](curriculum/03-inequalities) | 🟢 In progress |
| 04 | [Functions](curriculum/04-functions) | 🟢 In progress |
| 05 | Polynomials | ⬜ Not started |
| 06 | Factoring | ⬜ Not started |
| 07 | Rational Expressions | ⬜ Not started |
| 08 | Exponents & Radicals | ⬜ Not started |
| 09 | Quadratics | ⬜ Not started |
| 10 | Systems of Equations | ⬜ Not started |
| 11 | Word Problems | ⬜ Not started |

Each topic folder follows the same layout — **always lowercase, hyphenated** (e.g. `02-linear-equations`, never `02-Linear-Equations`), to avoid case-collision issues on case-sensitive systems like GitHub/Linux:

```
0X-topic-name/
├── README.md              ← concept explained in plain language
├── worked-examples.md     ← fully worked, step-by-step problems
├── practice-problems.md   ← tiered by difficulty (easy/medium/hard)
├── solutions.md           ← solutions kept separate so problems can be used "blind"
└── common-mistakes.md     ← misconceptions people actually run into
```

## Tools

Beyond the written curriculum, [`tools`](tools) has a Python-based practice problem generator and CLI quiz runner:

```bash
pip install -r requirements.txt
python tools/cli.py --topic linear-equations --difficulty medium --count 10
```

It generates randomized, guaranteed-solvable problems (works backwards from a chosen answer, so nothing is ever unsolvable), grades your input, and shows a real step-by-step solution when you get it wrong. See [`tools/README.md`](tools/README.md) for details on extending it with new topic generators.

## How to use this repo

- **Learning solo?** Start at `curriculum/01-foundations/README.md` and work through in order.
- **Studying for a test?** Jump to the topic you need — each is self-contained.
- **Teaching?** Fork it, remix it, use the practice problems as-is or as templates.
- **Want drills instead of reading?** Use the CLI tool above.

## How to contribute

New here and want to help? Read [CONTRIBUTING.md](CONTRIBUTING.md) — there are `good-first-issue` labeled tasks for newcomers, including "add practice problems" and "improve an explanation," which don't require deep math background to start on.

All code changes run through CI ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) — the test suite and a markdown link-checker run automatically on every PR.

## Roadmap

- [ ] Finish Foundations module (v0.1)
- [ ] Finish Linear Equations module (v0.1)
- [ ] Finish Inequalities module (v0.1)
- [ ] Finish Functions module (v0.1)
- [ ] Polynomials module
- [ ] Add visual/geometric explainer diagrams
- [ ] Extend `tools/` generator to cover more topics (inequalities, quadratics, ...)

## License

Code: MIT. Written content (explanations, problems, solutions): CC-BY-SA 4.0 — free to reuse and adapt, just credit the project and share alike.
