# Contributing to Algebra Mastery

Thanks for wanting to help build this. This guide covers everything from fixing a typo to adding a whole new module, so use the table of contents to jump to what you need.

## Table of contents

- [Ground rules](#ground-rules)
- [Ways to contribute](#ways-to-contribute)
- [Getting set up](#getting-set-up)
- [Repo layout and file formats](#repo-layout-and-file-formats)
- [Adding a practice problem](#adding-a-practice-problem)
- [Adding a worked example](#adding-a-worked-example)
- [Adding a common-mistakes entry](#adding-a-common-mistakes-entry)
- [Writing or improving an explanation](#writing-or-improving-an-explanation)
- [Adding a new module](#adding-a-new-module)
- [Code contributions](#code-contributions)
- [Style guide](#style-guide)
- [Before you open a PR](#before-you-open-a-pr)
- [Submitting a pull request](#submitting-a-pull-request)
- [What happens in review](#what-happens-in-review)
- [Reporting an error](#reporting-an-error)
- [License of your contributions](#license-of-your-contributions)
- [Code of Conduct](#code-of-conduct)

## Ground rules

1. **Accuracy over speed.** A wrong solution merged in silently hurts every learner who trusts this repo. Double-check your math before opening a PR.
2. **Plain language first.** Explain the *why* before the formal notation. Assume the reader has never seen this concept.
3. **Follow the existing template.** Every topic folder has the same five files. Match the style of what's already there.
4. **One concept per PR.** Easier to review, easier to merge.
5. **Keep it original.** Don't copy problems, explanations, or images verbatim from textbooks, paid courses, or other websites.

## Ways to contribute

Pick your comfort level:

| Contribution | Difficulty | Good for |
|---|---|---|
| Fix a typo or unclear sentence | 🟢 Easy | First-time contributors |
| Verify a solution by re-solving it, and report any error | 🟢 Easy | Anyone comfortable with the topic |
| Add practice problems to an existing module | 🟢 Easy to medium | Anyone who knows the topic |
| Add a worked example | 🟡 Medium | People who can explain steps clearly |
| Write a "common mistakes" entry | 🟡 Medium | People who've tutored or been confused themselves |
| Improve a module's explanation | 🟡 Medium | Teachers, tutors, strong learners |
| Add a generator for a new topic, with tests | 🔴 Involved | Python developers |
| Write a full new module from the template | 🔴 Involved | Confident with the topic, has time |

Check the [Issues tab](../../issues) for tasks labeled `good-first-issue`.

## Getting set up

**For written content (Markdown only):** you need nothing but a text editor and Git. Fork the repo, clone it, and edit.

**For code (the generator and tests):** you need Python 3.9 or newer.

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -r requirements.txt     # just pytest
python -m pytest tests/ -q          # should all pass before you change anything
python tools/cli.py --count 3       # try the quiz
```

If the tests fail on a fresh clone, that's worth an issue by itself.

## Repo layout and file formats

```
curriculum/0X-topic-name/    ← lowercase, hyphenated folder names
├── README.md
├── worked-examples.md
├── practice-problems.md
├── solutions.md
└── common-mistakes.md
tools/                        ← practice generator + CLI (see tools/README.md)
tests/                        ← pytest suite for the generator
```

Folder names are **always lowercase and hyphenated** (`02-linear-equations`, never `02-Linear-Equations`). Case-sensitive systems like Linux treat those as two different folders, which breaks links and causes duplicates.

Each file has an established format. Open an existing module and copy its shape.

| File | Format |
|---|---|
| `README.md` | `# 0X — Topic`, then numbered sections (`## 1. ...`), each with a short explanation and an inline example, ending with `## What's next` |
| `worked-examples.md` | `### Example N: short title`, then `**Problem:**`, numbered `**Step N:**` lines, a `**Check:**` line, and `**Answer: ...**` |
| `practice-problems.md` | `## Easy`, `## Medium`, `## Hard`, with problems as `**P1.** Solve for x: ...` |
| `solutions.md` | Same tiers, with solutions as `**S1.** ...`, using the **same number** as the problem |
| `common-mistakes.md` | `## N. Short name of the mistake`, then a Wrong line (❌), a Right line (✓), and a sentence on *why* people make it |

## Adding a practice problem

1. Open `curriculum/0X-topic/practice-problems.md`.
2. Add your problem under the correct tier heading (`## Easy`, `## Medium`, or `## Hard`). Use the **next unused number** in the file (if the last problem is `P15`, yours is `P16`, even if it sits in the Easy section). Numbers don't have to be in order within the file, but they must be unique.
3. Add the matching, fully worked solution to `solutions.md` under the same tier, with the **same number** (`S16`).
4. **Verify it yourself.** Solve it from scratch without looking at your solution, then substitute your answer back into the original problem. If the problem has no single answer ("no solution" or "infinite solutions"), say so explicitly in the solution.
5. Keep difficulty honest. Easy is one or two steps, Medium needs distributing or variables on both sides, and Hard combines several ideas or has a trap.

Example. In `practice-problems.md`, under `## Medium`:

```markdown
**P16.** Solve for x: `4(x - 3) = 2x + 6`
```

And in `solutions.md`, under `## Medium`:

```markdown
**S16.** `4(x - 3) = 2x + 6`
- Distribute: `4x - 12 = 2x + 6`
- Subtract 2x: `2x - 12 = 6`
- Add 12: `2x = 18`
- Divide by 2: `x = 9`
```

Check: `4(9 - 3) = 24` and `2(9) + 6 = 24` ✓

Show every step in the solution, even obvious ones. Learners use solutions to find where their own working went wrong.

## Adding a worked example

Worked examples teach a *pattern*, so each one should show something the others don't (a new move, a trap, a special case).

1. Add it to `worked-examples.md` as the next `### Example N: ...`, using the format in the table above.
2. Always include a **Check** line that substitutes the answer back in.
3. Say in the title what the example is *about* ("Distributing first", "Recognizing no solution"), not just "Example 6".
4. Don't reuse a problem that's already in `practice-problems.md`.

## Adding a common-mistakes entry

The best entries come from real confusion: something you got wrong, or saw a student get wrong.

- Show the mistake (❌) next to the correct version (✓) so the difference is visible at a glance.
- Explain **why** the mistake is tempting. "People forget the negative" is weak. "People distribute the 3 to the x but not the 2 because the 2 feels separate" is useful.
- Link back to the earlier module where the underlying idea first appears, if there is one.

## Writing or improving an explanation

- Start with a real-world or intuitive framing before introducing notation.
- Include at least one fully worked example inline.
- Keep paragraphs short. This is a reference people scan, not a novel.
- Introduce one new idea per section. If a section needs a previous module's idea, link to it.
- Define a term the first time it appears, in bold.
- End with a `## What's next` pointer so the path through the curriculum stays clear.

If you're improving an existing explanation, say in the PR description what was confusing and why your version is clearer.

## Adding a new module

1. Create `curriculum/0X-topic-name/` (lowercase, hyphenated) with all five files in the formats above.
2. Aim for the same depth as existing modules: about 5 sections in the README, 5 worked examples, and 15 practice problems (5 per tier) with full solutions.
3. Update the learning path table in the root `README.md`: link the module, add what it covers, and set its status.
4. Add a `## What's next` link from the previous module to yours.
5. Open an issue first if the module is big, so nobody duplicates your effort.

## Code contributions

The generator lives in `tools/algebra_tools/generator.py`, the CLI in `tools/cli.py`, and tests in `tests/`. For how the generator works and how to register a new topic, read [`tools/README.md`](tools/README.md).

Rules for code:

- **Standard library only** in `tools/`. The CLI should run with no `pip install`.
- **Python 3.9 compatible.** CI tests 3.9, 3.11, and 3.12. Keep `from __future__ import annotations` at the top of modules, and don't use `match` statements.
- **Use a local `random.Random(seed)`**, never `random.seed()` or the global `random` functions. Tests enforce this.
- **Generate backwards.** Pick the answer first, then build the problem around it, so every problem is solvable by construction.
- **Every new generator needs tests.** At minimum: a round-trip correctness check across many seeds and all three difficulties, a reproducibility check (same seed gives the same problem), and an invalid-input check.
- Add type hints and a short docstring to public functions.

Run `python -m pytest tests/ -q` before pushing. CI runs the same command.

## Style guide

**Math notation**

- Put math in backticks: `3x + 7 = 22`.
- Use `×` for multiplication between numbers (`3 × 4`), and write `3x` (not `3*x`) for a coefficient times a variable.
- Use `^` for exponents (`x^2`) or `²` for squares. Be consistent within a file.
- Write fractions inline as `(x - 2)/3`, with parentheses around any numerator that has more than one term.
- Wrap negative numbers in parentheses after an operator: `5 + (-3)`, not `5 + -3`.
- State final answers as `x = 4`, in bold in worked examples.

**Language**

- Short sentences. Active voice. Say "subtract 3 from both sides", not "3 is subtracted".
- Avoid "obviously", "simply", "just", and "clearly". If it were obvious, the learner wouldn't be reading it.
- Spell out abbreviations on first use (GCF is "greatest common factor").

**Formatting**

- Use the exact file names in the table above (lowercase, hyphenated).
- One blank line between sections. Keep lines readable, with no hard wrapping required.
- Use relative links between files (`../02-linear-equations/README.md`) so they work on GitHub and locally.

## Before you open a PR

Run through this list:

- [ ] I solved every new problem from scratch and checked my answer by substituting it back.
- [ ] Every new problem has a solution with the **same number** in `solutions.md`.
- [ ] I matched the format of the existing files.
- [ ] Relative links I added point at files that exist.
- [ ] My content is original, not copied from a book, course, or website.
- [ ] For code changes: `python -m pytest tests/ -q` passes, and I added tests for new behavior.
- [ ] The PR covers one concept or one fix.

## Submitting a pull request

1. Fork the repo and create a branch with a descriptive name, such as `add-linear-equations-practice-problems` or `fix-s12-sign-error`.
2. Make your changes following the formats above.
3. Commit with a short, specific message: `Add 5 medium problems to inequalities` is good, `update` is not.
4. Open a PR against `main`. In the description, say what you added or changed and why, and tick the checklist.
5. Wait for CI. It runs the test suite and a link check, and the PR can't merge while it's red.

## What happens in review

A maintainer or experienced contributor will review your PR for:

1. **Accuracy.** Every solution gets re-solved. This is the most important check.
2. **Clarity.** Would a beginner follow this without extra help?
3. **Consistency.** Does it match the template, notation, and tone of the rest of the repo?
4. **Scope.** Is it one concept, or should it be split?

Expect requests for changes. That's normal, and it isn't a judgement on you. If a review comment is unclear, ask. If you disagree, explain your reasoning. Good arguments change minds here.

## Reporting an error

Found a wrong answer or a confusing explanation? You don't have to fix it yourself. Open an issue using one of the templates:

- **Fix error in solution**: a wrong answer, a skipped or incorrect step, or a mismatched problem and solution number.
- **Improve explanation clarity**: something that was hard to follow, a missing example, or unclear wording.

Say which file and which problem or section, what you think is wrong, and what you think is right. Flagging it helps a lot.

## License of your contributions

By submitting a contribution, you agree that:

- **code** (`tools/`, `tests/`) is released under the MIT license, and
- **written content** (`curriculum/`: explanations, problems, solutions) is released under CC-BY-SA 4.0,

matching the License section of the root `README.md`. Only submit work that is yours to share.

## Code of Conduct

Be kind, be patient, assume good faith. This project exists to help people learn, and that includes contributors who are still learning too.

- Critique the work, not the person.
- Explain *why* when you request a change, and say what was good about the original.
- Never mock a question or a mistake. Everyone here was a beginner once.
- Harassment, personal attacks, and discriminatory language aren't welcome. Maintainers may remove comments, close issues, or block users that break these rules.
