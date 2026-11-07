# Roadmap

This roadmap lays out where **ALGEBRA-** is going and in what order. For *how* the pieces fit together, see [`ARCHITECTURE.md`](ARCHITECTURE.md).

**Status legend:** ✅ done · 🚧 in progress · 📋 planned · 💡 idea (not committed)

Each phase has **tasks** and **exit criteria**. A phase is finished only when every exit criterion is true, not when the tasks merely look done.

---

## Overview

| Phase | Theme | Outcome | Status |
|-------|-------|---------|--------|
| 1 | Repair | Existing content is correct and the README is accurate | 📋 |
| 2 | Restructure | Repo follows the target layout with CI running | 📋 |
| 3 | Symbolic engine | Parse, simplify, expand, factor, and solve with step traces, no SymPy | 📋 |
| 4 | Optimization | Lagrange-multiplier example built on the engine | 📋 |
| 5 | Hardening | Full tests, lint, strict typing, finished docs | 📋 |
| 6+ | Growth | Curriculum expansion, richer practice tools | 💡 |

Phases are sequential: each one depends on the one before it. Phase 3 is the largest.

---

## Phase 1: Repair 📋

**Goal:** make what already exists trustworthy before building on it.

**Tasks**

- [ ] Rewrite `README.md` first: what the repo is, who it is for, and a two-minute quickstart
- [ ] Audit existing curriculum files for math errors, broken links, and inconsistent formatting
- [ ] Verify that every code snippet and script in the repo actually runs
- [ ] Fix or remove dead files, duplicates, and leftover scratch work
- [ ] Add a `LICENSE` and a proper `.gitignore`
- [ ] Record everything found but not fixed in `docs/ROADMAP.md` under *Known issues*

**Exit criteria**

- A stranger can read the README and know what to do in under two minutes
- No known math errors remain in the curriculum
- Every existing script runs without edits

---

## Phase 2: Restructure 📋

**Goal:** move to the target layout so later phases have a home.

**Tasks**

- [ ] Create `curriculum/` with level folders and numbered topic folders
- [ ] Add `curriculum/_templates/` (lesson and problem templates)
- [ ] Move existing lessons into the template shape: `lesson.md`, `practice.md`, `solutions.md`, `notes.md`
- [ ] Create `tools/algebra_tools/` package with `__init__.py` and `py.typed`
- [ ] Move the existing practice generator into `practice/generator.py`
- [ ] Add `tools/cli.py` as a thin wrapper
- [ ] Create `tests/`, `examples/`, and `docs/`
- [ ] Rename files to lowercase-hyphen style and fix every internal link
- [ ] Add `pyproject.toml`, `requirements.txt`, and `requirements-dev.txt`
- [ ] Add `.github/workflows/ci.yml` running pytest and ruff
- [ ] Add `CONTRIBUTING.md`

**Exit criteria**

- Repo layout matches `ARCHITECTURE.md` section 2
- CI is green on the default branch
- `scripts/check_links.py` (or a manual pass) finds zero broken links
- The CLI runs the practice generator end to end

---

## Phase 3: Symbolic engine 📋

**Goal:** a from-scratch engine (standard library only) that manipulates algebra and **explains its steps**.

This is the biggest phase, so it is broken into milestones. Each milestone is shippable on its own.

### 3.1 Foundations

- [ ] `ast_nodes.py`: immutable nodes `Num`, `Var`, `Add`, `Mul`, `Pow`, `Neg`, `Func`
- [ ] `tokenizer.py`: numbers, variables, operators, parentheses, functions
- [ ] `parser.py`: precedence climbing, implicit multiplication, right-associative `^`
- [ ] `printer.py`: AST to readable text (LaTeX comes later)
- [ ] `errors.py`: `ParseError`, `DomainError`, `NotSupportedError`
- [ ] Tests: unit tests plus the round-trip property `parse(print(e)) == e`

**Done when:** any valid expression string parses to an AST and prints back identically.

### 3.2 Simplify and expand

- [ ] Write `docs/design/002-simplification-strategy.md` (normal form) **before** coding
- [ ] `simplify.py`: flatten, fold constants, combine like terms, sort, remove identities
- [ ] `expand.py`: distribution and binomial expansion
- [ ] `steps.py`: `Step` and `Result` types, text rendering of traces
- [ ] Tests: unit tests, idempotence property, numeric cross-check at random points

**Done when:** `simplify("2x + 3x - x")` returns `4x` with a readable step trace, and idempotence holds across generated expressions.

### 3.3 Factor and solve

- [ ] `polynomial.py`: canonical polynomial representation
- [ ] `factor.py`: GCF, grouping, quadratics, difference of squares
- [ ] `solve.py`: linear equations, quadratics (including complex roots), 2x2 and 3x3 systems
- [ ] `numeric/linear_system.py`: Gaussian elimination
- [ ] `practice/checker.py`: answer checking by equivalence
- [ ] Tests for each module, plus `expand(factor(e))` equivalent to `e`

**Done when:** the CLI solves linear and quadratic equations with `--steps`, and the checker accepts equivalent answers (`x^2-1` and `(x-1)(x+1)`).

### 3.4 Differentiate

- [ ] `differentiate.py`: power rule, sum, product, chain rule, basic functions
- [ ] Tests, including a numeric derivative cross-check

**Done when:** symbolic derivatives agree with finite-difference estimates on random inputs.

**Phase 3 exit criteria**

- No imports of SymPy anywhere in `tools/algebra_tools/`
- Every transform emits step traces
- Property and numeric cross-check tests pass in CI
- CLI supports `solve`, `simplify`, and `check`

---

## Phase 4: Optimization example 📋

**Goal:** show the engine doing something real with a constrained-optimization worked example.

**Tasks**

- [ ] `optimization/lagrange.py`: build the Lagrangian, differentiate, solve the resulting system
- [ ] `examples/03-lagrange-box-problem.py`: a worked example (for instance, maximize box volume under a surface-area constraint)
- [ ] Curriculum lesson `16-optimization/` with intuition, worked example, and practice
- [ ] Verify results numerically against a brute-force search
- [ ] Tests for the Lagrange module

**Exit criteria**

- The example runs end to end and prints the steps
- The lesson links to the code and the code links back to the lesson
- Numeric verification agrees with the symbolic answer

---

## Phase 5: Hardening 📋

**Goal:** make the repo something other people can trust and contribute to.

**Tasks**

- [ ] Turn on `mypy --strict` for `tools/algebra_tools/` and fix everything it finds
- [ ] Enforce `ruff check` and `ruff format --check` in CI
- [ ] Add a pre-commit config
- [ ] Add a coverage floor in CI (start at 80%, raise over time)
- [ ] Add the link checker to CI
- [ ] Finalize `ARCHITECTURE.md` and flip every status marker to match reality
- [ ] Add issue and PR templates
- [ ] Write `CHANGELOG.md` and tag a first release (`v0.1.0`)

**Exit criteria**

- CI enforces lint, types, tests, coverage, and links
- A new contributor can add a topic or a rewrite rule using only the docs
- `ARCHITECTURE.md` matches the code

---

## Phase 6+: Growth 💡

These ideas are **not committed**. Promote one into a numbered phase only when it has tasks and exit criteria.

- LaTeX output for the printer and step traces
- Inequalities (`Lt`, `Gt`) and systems of inequalities
- Rational expressions and partial fractions
- Matrices and determinants in the engine (ties into the linear algebra material)
- Difficulty-adaptive practice sessions
- Jupyter notebook walkthroughs for each curriculum level
- A static site generated from `curriculum/`
- Spaced-repetition export of practice problems

---

## Curriculum progress

Track topic status here. Update it when a topic gets all four files.

| Level | Topic | Lesson | Practice | Solutions | Notes |
|-------|-------|:------:|:--------:|:---------:|:-----:|
| 1 | Number systems | 📋 | 📋 | 📋 | 📋 |
| 1 | Linear equations | 📋 | 📋 | 📋 | 📋 |
| 1 | Inequalities | 📋 | 📋 | 📋 | 📋 |
| 1 | Exponents and radicals | 📋 | 📋 | 📋 | 📋 |
| 2 | Polynomials | 📋 | 📋 | 📋 | 📋 |
| 2 | Factoring | 📋 | 📋 | 📋 | 📋 |
| 2 | Quadratics | 📋 | 📋 | 📋 | 📋 |
| 2 | Systems of equations | 📋 | 📋 | 📋 | 📋 |
| 2 | Rational expressions | 📋 | 📋 | 📋 | 📋 |
| 3 | Functions and graphs | 📋 | 📋 | 📋 | 📋 |
| 3 | Exponentials and logs | 📋 | 📋 | 📋 | 📋 |
| 3 | Sequences and series | 📋 | 📋 | 📋 | 📋 |
| 4 | Complex numbers | 📋 | 📋 | 📋 | 📋 |
| 4 | Polynomial theory | 📋 | 📋 | 📋 | 📋 |
| 4 | Matrices intro | 📋 | 📋 | 📋 | 📋 |
| 4 | Optimization | 📋 | 📋 | 📋 | 📋 |

Replace the markers with the real current state before publishing. Several of these may already be partly done.

---

## Risks and mitigations

| Risk | Why it matters | Mitigation |
|------|----------------|------------|
| Simplification has no canonical form | Equality checks and tests become unreliable | Write the normal-form design doc *before* any simplify code |
| Implicit multiplication breaks the parser | `2x`, `3(x+1)`, and `x(y)` are ambiguous | Isolate it in one place; give it a dedicated test section |
| Scope creep in the engine | Turns into a half-finished CAS | Ship each Phase 3 milestone on its own; defer extras to Phase 6+ |
| Curriculum drifts from the code | Learners hit stale or broken links | Link checker in CI; every lesson links to code and back |
| Wrong rewrite rule goes unnoticed | Teaches incorrect algebra | Numeric cross-check on every transform |

---

## How to use this document

- Move a task to ✅ in the same commit that completes it.
- Add new ideas under **Phase 6+** first; promote them when they have exit criteria.
- If a phase's scope changes, edit the phase rather than quietly working around it.
- Log anything found but not fixed in a **Known issues** section so it is not lost.
