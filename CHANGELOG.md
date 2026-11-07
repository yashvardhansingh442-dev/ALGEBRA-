# Changelog

All notable changes to **ALGEBRA-** are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) once it reaches `1.0.0`. Before that, minor versions (`0.x.0`) may include breaking changes, and they will be listed under **Changed** or **Removed**.

## How to use this file

- Add an entry in the **same commit or PR** as the change, under `[Unreleased]`.
- Write for a *user or learner*, not for yourself. "Added a quadratics lesson" beats "update stuff".
- Use these headings, and only the ones you need:
  - **Added**: new features, lessons, or files
  - **Changed**: changes to existing behavior or content
  - **Deprecated**: things that will be removed soon
  - **Removed**: things taken out
  - **Fixed**: bug fixes and corrected math
  - **Security**: vulnerability fixes
- Mark **math corrections** clearly under **Fixed**, since learners may have studied the wrong version. Example: "Fixed sign error in worked example 3 of `quadratics/lesson.md`."
- When releasing, rename `[Unreleased]` to the new version with the date (`YYYY-MM-DD`), add a fresh empty `[Unreleased]` above it, and update the comparison links at the bottom.

---

## [Unreleased]

> **Note:** the entries below are a starting point based on the planned work. Edit them to match what actually lands in your commits, and delete any that do not apply.

### Added

- Project documentation: `ARCHITECTURE.md`, `ROADMAP.md`, `docs/glossary.md`, and this changelog.
- `pyproject.toml` with packaging, Ruff, Mypy (strict), Pytest, and coverage configuration.
- Curriculum structure under `curriculum/` with level folders, numbered topic folders, and lesson/problem templates.
- Python package skeleton `tools/algebra_tools/` with a command-line interface.
- Continuous integration workflow running tests, linting, and type checks.

### Changed

- Reorganized existing content into the `curriculum/` and `tools/` layout.
- Renamed files to lowercase-hyphen style and updated internal links.

### Fixed

- Rewrote the README so it accurately describes the repository.

---

## Planned releases

These are targets from [`ROADMAP.md`](docs/ROADMAP.md), not promises. They are kept here so the version history has a clear direction. Move items into real release sections as they ship.

### 0.1.0 (target: end of Phase 5)

First tagged release. Expected to include:

- Symbolic engine without SymPy: tokenizer, parser, AST, simplify, expand, factor, solve, differentiate
- Step traces for every transform
- Practice generator and answer checker
- Lagrange-multiplier optimization example
- Strict typing, lint, coverage floor, and link checking enforced in CI

---

<!--
Comparison links. Replace the placeholders when you publish the first tag.

[Unreleased]: https://github.com/yashvardhansingh442-dev/ALGEBRA-/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yashvardhansingh442-dev/ALGEBRA-/releases/tag/v0.1.0
-->

[Unreleased]: https://github.com/yashvardhansingh442-dev/ALGEBRA-/commits/main
