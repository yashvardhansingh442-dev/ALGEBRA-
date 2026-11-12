<!--
Save as: .github/PULL_REQUEST_TEMPLATE.md

Thanks for contributing! Fill in what applies and delete what doesn't.
Comments like this one are hidden in the final PR, so you don't need to remove them.
Small fix? A one-line summary and the checklist are enough.
-->

## Summary

<!-- What does this PR do, and why? One or two sentences. -->

Closes #<!-- issue number, or delete this line -->

## Type of change

<!-- Tick all that apply. -->

- [ ] 📚 Curriculum: new or updated lesson, practice, or solutions
- [ ] 🧮 Math fix: a correction to a wrong statement, step, or answer
- [ ] ⚙️ Engine: parser, simplify, expand, factor, solve, differentiate, etc.
- [ ] 🎲 Practice tools: generator, checker, difficulty
- [ ] 💻 CLI
- [ ] 📝 Documentation
- [ ] 🔧 Tooling: CI, packaging, lint, config
- [ ] 🧹 Refactor (no behavior change)

## What changed

<!--
List the main changes. For curriculum work, name the topic(s) touched.
For a math fix, say what was wrong and what it is now, so learners who studied
the old version know what to re-check.
-->

-

## How I checked it

<!-- Show your work. Paste commands, outputs, or screenshots. -->

- [ ] I ran `make check` locally (lint, format, mypy, tests, links) and it passes

## Checklist for everyone

- [ ] I read [`CONTRIBUTING.md`](../CONTRIBUTING.md) and agree to follow the [Code of Conduct](../CODE_OF_CONDUCT.md)
- [ ] This PR does one thing; unrelated changes are in separate PRs
- [ ] I added an entry under `[Unreleased]` in [`CHANGELOG.md`](../CHANGELOG.md) (math corrections go under **Fixed**)
- [ ] I did not copy copyrighted textbook text, exam questions, or solution manuals
- [ ] New or changed terms are defined in [`docs/glossary.md`](../docs/glossary.md)

## If this touches the curriculum

- [ ] The topic follows the template (`lesson.md`, `practice.md`, `solutions.md`, `notes.md`)
- [ ] I worked every problem myself and the solutions show steps, not just answers
- [ ] Problems are tagged easy / medium / hard
- [ ] Prerequisites and common mistakes are stated in the lesson
- [ ] Links to and from related code or lessons work (the link check passes)
- [ ] Filenames are lowercase-hyphen

## If this touches the engine or tools

- [ ] Every new transform emits step traces (`Step` records), not just a final answer
- [ ] No SymPy (or other CAS) is imported from `tools/algebra_tools/`
- [ ] Constants use exact arithmetic (`Fraction`), not floats, outside `numeric/`
- [ ] Added or updated tests:
  - [ ] unit tests for the new behavior
  - [ ] property test where it applies (idempotence, round trip, equivalence)
  - [ ] numeric cross-check for any new rewrite rule
- [ ] Public functions are type-annotated and `mypy --strict` passes
- [ ] The CLI still contains no algebra logic; new features live in the package and are callable as plain Python
- [ ] [`ARCHITECTURE.md`](../docs/ARCHITECTURE.md) and [`ROADMAP.md`](../docs/ROADMAP.md) status markers are updated if a phase or module changed state

## Notes for the reviewer

<!--
Anything that would help review: trade-offs you made, parts you are unsure about,
things you deliberately left out, or follow-ups you plan. Optional.
-->
