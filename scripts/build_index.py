#!/usr/bin/env python3
"""Generate the curriculum table of contents from the folder structure.

Save as: scripts/build_index.py     (standard library only, Python 3.10+)

The folders under ``curriculum/`` are the single source of truth. This script
reads them and regenerates, between marker comments:

  1. the full table of contents in ``curriculum/00-start-here.md``, and
  2. the "Curriculum progress" table in ``docs/ROADMAP.md`` (optional).

Expected layout
---------------
    curriculum/
    ├── 00-start-here.md
    ├── level-1-foundations/
    │   ├── 01-number-systems/
    │   │   ├── lesson.md
    │   │   ├── practice.md
    │   │   ├── solutions.md
    │   │   └── notes.md
    │   └── 02-linear-equations/ ...
    ├── level-2-core-algebra/ ...
    └── _templates/                 (folders starting with "_" or "." are ignored)

Status of each file
-------------------
    ✅  exists and has content
    🚧  exists, but contains the marker  <!-- draft -->
    📋  missing or empty

A topic counts as *complete* when its lesson, practice, and solutions are all ✅.
``notes.md`` is shown but does not affect completeness.

Topic titles come from the first ``# Heading`` of ``lesson.md``; if there is no
lesson yet, they are derived from the folder name.

Markers
-------
Add these lines once, around the place the generated content should go:

    <!-- BEGIN: curriculum-index -->
    <!-- END: curriculum-index -->           in curriculum/00-start-here.md

    <!-- BEGIN: curriculum-progress -->
    <!-- END: curriculum-progress -->        in docs/ROADMAP.md  (optional)

Everything between a pair of markers is overwritten. Nothing outside is touched.

Usage
-----
    python scripts/build_index.py             update the files in place
    python scripts/build_index.py --check     exit 1 if anything is out of date
                                              (for CI and pre-commit; changes nothing)
    python scripts/build_index.py --stdout    print the generated blocks, change nothing
    python scripts/build_index.py --init      create 00-start-here.md if it is missing
    python scripts/build_index.py --strict    treat layout warnings as failures
    python scripts/build_index.py --no-roadmap

Exit codes
----------
    0  success (or, with --check, everything is up to date)
    1  --check found stale files, or --strict found layout warnings
    2  setup problem (missing curriculum folder, file, or markers)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

DONE, DRAFT, MISSING = "✅", "🚧", "📋"
DRAFT_MARKER = "<!-- draft -->"

LESSON_FILES: tuple[str, ...] = ("lesson", "practice", "solutions", "notes")
REQUIRED_FILES: tuple[str, ...] = ("lesson", "practice", "solutions")

_SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
LEVEL_RE = re.compile(rf"^level-(?P<num>\d+)-(?P<slug>{_SLUG})$")
TOPIC_RE = re.compile(rf"^(?P<num>\d+)-(?P<slug>{_SLUG})$")

INDEX_BLOCK = "curriculum-index"
PROGRESS_BLOCK = "curriculum-progress"

EXIT_OK, EXIT_STALE, EXIT_SETUP = 0, 1, 2

START_HERE_SKELETON = f"""\
# Start here

Welcome! This curriculum takes you from the basics of algebra to more advanced
topics, one numbered topic at a time. Work through the levels in order, or jump
to a topic you need.

Every topic has the same four files:

- `lesson.md`: the concept, with worked examples
- `practice.md`: problems, tagged easy / medium / hard
- `solutions.md`: step-by-step answers and common mistakes
- `notes.md`: what tripped me up while learning it

## Curriculum

<!-- BEGIN: {INDEX_BLOCK} -->
<!-- END: {INDEX_BLOCK} -->
"""


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Topic:
    number: int
    title: str
    path: Path
    status: dict[str, str]

    @property
    def complete(self) -> bool:
        return all(self.status[name] == DONE for name in REQUIRED_FILES)


@dataclass
class Level:
    number: int
    title: str
    path: Path
    topics: list[Topic] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Scanning the curriculum folder
# ---------------------------------------------------------------------------


def _humanize(slug: str) -> str:
    return slug.replace("-", " ").capitalize()


def _file_status(path: Path) -> str:
    if not path.is_file():
        return MISSING
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return MISSING  # an empty placeholder counts as not started
    return DRAFT if DRAFT_MARKER in text else DONE


def _topic_title(topic_dir: Path, slug: str) -> str:
    lesson = topic_dir / "lesson.md"
    if lesson.is_file():
        for line in lesson.read_text(encoding="utf-8").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
    return _humanize(slug)


def _subdirs(path: Path) -> list[Path]:
    """Visible subdirectories, sorted by name. Folders starting with _ or . are skipped."""
    return sorted(
        entry
        for entry in path.iterdir()
        if entry.is_dir() and not entry.name.startswith(("_", "."))
    )


def scan(curriculum: Path, root: Path) -> tuple[list[Level], list[str]]:
    """Read the folder tree. Returns the levels and a list of layout warnings."""
    warnings: list[str] = []
    levels: list[Level] = []

    def rel(path: Path) -> str:
        return path.relative_to(root).as_posix()

    for level_dir in _subdirs(curriculum):
        level_match = LEVEL_RE.match(level_dir.name)
        if not level_match:
            warnings.append(f"ignored {rel(level_dir)}/ (expected a name like level-1-foundations)")
            continue

        level = Level(
            number=int(level_match["num"]),
            title=_humanize(level_match["slug"]),
            path=level_dir,
        )
        for topic_dir in _subdirs(level_dir):
            topic_match = TOPIC_RE.match(topic_dir.name)
            if not topic_match:
                warnings.append(
                    f"ignored {rel(topic_dir)}/ (expected a name like 01-number-systems)"
                )
                continue
            level.topics.append(
                Topic(
                    number=int(topic_match["num"]),
                    title=_topic_title(topic_dir, topic_match["slug"]),
                    path=topic_dir,
                    status={name: _file_status(topic_dir / f"{name}.md") for name in LESSON_FILES},
                )
            )
        level.topics.sort(key=lambda topic: (topic.number, topic.path.name))
        levels.append(level)

    levels.sort(key=lambda level: (level.number, level.path.name))
    warnings += _numbering_warnings(levels)
    return levels, warnings


def _numbering_warnings(levels: list[Level]) -> list[str]:
    """Flag duplicate level numbers and duplicate topic numbers."""
    warnings: list[str] = []
    seen_levels: set[int] = set()
    seen_topics: dict[int, str] = {}
    for level in levels:
        if level.number in seen_levels:
            warnings.append(f"duplicate level number {level.number}: {level.path.name}")
        seen_levels.add(level.number)
        for topic in level.topics:
            if topic.number in seen_topics:
                warnings.append(
                    f"duplicate topic number {topic.number:02d}: "
                    f"{seen_topics[topic.number]} and {topic.path.name}"
                )
            else:
                seen_topics[topic.number] = topic.path.name
    return warnings


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _escape(text: str) -> str:
    return text.replace("|", "\\|")


def _link(target: Path, base: Path) -> str:
    return Path(os.path.relpath(target, base)).as_posix()


def _counts(levels: list[Level]) -> tuple[int, int]:
    topics = [topic for level in levels for topic in level.topics]
    return sum(topic.complete for topic in topics), len(topics)


def render_index(levels: list[Level], base: Path) -> str:
    """Table of contents with links. ``base`` is the folder of the file it goes into."""
    done, total = _counts(levels)
    lines = [
        "<!-- Generated by scripts/build_index.py. Edit the topic files, not this block. -->",
        "",
    ]
    if total == 0:
        lines.append("No topics yet.")
        return "\n".join(lines)

    percent = round(100 * done / total)
    lines += [
        f"**Progress:** {done} of {total} topics complete ({percent}%).  ",
        f"{DONE} done · {DRAFT} draft · {MISSING} not started",
    ]

    for level in levels:
        lines += [
            "",
            f"### Level {level.number}: {level.title}",
            "",
            "| # | Topic | Lesson | Practice | Solutions | Notes |",
            "|---|-------|:------:|:--------:|:---------:|:-----:|",
        ]
        for topic in level.topics:
            cells = []
            for name in LESSON_FILES:
                status = topic.status[name]
                if status == MISSING:
                    cells.append(status)
                else:
                    cells.append(f"[{status}]({_link(topic.path / f'{name}.md', base)})")
            title = f"[{_escape(topic.title)}]({_link(topic.path, base)}/)"
            lines.append(f"| {topic.number:02d} | {title} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def render_progress(levels: list[Level]) -> str:
    """Plain status table for docs/ROADMAP.md (no links, same columns as the roadmap)."""
    lines = [
        "| Level | Topic | Lesson | Practice | Solutions | Notes |",
        "|-------|-------|:------:|:--------:|:---------:|:-----:|",
    ]
    for level in levels:
        for topic in level.topics:
            cells = " | ".join(topic.status[name] for name in LESSON_FILES)
            lines.append(f"| {level.number} | {_escape(topic.title)} | {cells} |")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Updating files between markers
# ---------------------------------------------------------------------------


def _block_pattern(name: str) -> re.Pattern[str]:
    return re.compile(
        rf"(<!-- BEGIN: {re.escape(name)} -->\n)(.*?)(<!-- END: {re.escape(name)} -->)",
        re.DOTALL,
    )


def replace_block(text: str, name: str, body: str) -> str | None:
    """Return ``text`` with the named block's contents replaced, or None if no markers."""
    match = _block_pattern(name).search(text)
    if match is None:
        return None
    return text[: match.start(2)] + body + "\n" + text[match.start(3) :]


def _wrap(name: str, body: str) -> str:
    return f"<!-- BEGIN: {name} -->\n{body}\n<!-- END: {name} -->"


@dataclass
class Target:
    path: Path
    block: str
    body: str
    required: bool


def _setup_problem(target: Target, root: Path) -> str | None:
    """Describe why a *required* target cannot be updated, or None if it is fine."""
    label = target.path.relative_to(root).as_posix()
    if not target.path.is_file():
        return f"{label} not found (use --init to create it)"
    text = target.path.read_text(encoding="utf-8")
    if replace_block(text, target.block, "") is None:
        markers = f"<!-- BEGIN: {target.block} --> / <!-- END: {target.block} -->"
        return f"{label} has no markers; add {markers}"
    return None


def _process(target: Target, root: Path, *, check: bool) -> int:
    """Update (or check) one file. Returns an exit code."""
    label = target.path.relative_to(root).as_posix()

    if not target.path.is_file():
        if target.required:
            print(f"error: {label} not found (use --init to create it)", file=sys.stderr)
            return EXIT_SETUP
        print(f"{label}: skipped (file not found)")
        return EXIT_OK

    original = target.path.read_text(encoding="utf-8")
    updated = replace_block(original, target.block, target.body)
    if updated is None:
        markers = f"<!-- BEGIN: {target.block} --> / <!-- END: {target.block} -->"
        if target.required:
            print(f"error: {label} has no markers; add {markers}", file=sys.stderr)
            return EXIT_SETUP
        print(f"{label}: skipped (no {target.block} markers)")
        return EXIT_OK

    if updated == original:
        print(f"{label}: up to date")
        return EXIT_OK
    if check:
        print(f"{label}: OUT OF DATE (run: python scripts/build_index.py)", file=sys.stderr)
        return EXIT_STALE

    target.path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"{label}: updated")
    return EXIT_OK


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate the curriculum table of contents from the folder structure."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root (default: the folder above scripts/)",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="exit 1 if files are out of date")
    mode.add_argument("--stdout", action="store_true", help="print the blocks, change nothing")
    parser.add_argument("--init", action="store_true", help="create 00-start-here.md if missing")
    parser.add_argument("--strict", action="store_true", help="fail on layout warnings")
    parser.add_argument("--no-roadmap", action="store_true", help="do not touch docs/ROADMAP.md")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root: Path = args.root.resolve()
    curriculum = root / "curriculum"

    if not curriculum.is_dir():
        print(f"error: {curriculum} not found", file=sys.stderr)
        return EXIT_SETUP

    levels, warnings = scan(curriculum, root)
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)

    start_here = curriculum / "00-start-here.md"
    index_body = render_index(levels, curriculum)
    progress_body = render_progress(levels)

    if args.stdout:
        print(_wrap(INDEX_BLOCK, index_body))
        print()
        print(_wrap(PROGRESS_BLOCK, progress_body))
        return EXIT_STALE if (args.strict and warnings) else EXIT_OK

    if args.init and not start_here.exists() and not args.check:
        start_here.write_text(START_HERE_SKELETON, encoding="utf-8", newline="\n")
        print(f"{start_here.relative_to(root).as_posix()}: created")

    targets = [Target(start_here, INDEX_BLOCK, index_body, required=True)]
    if not args.no_roadmap:
        targets.append(
            Target(root / "docs" / "ROADMAP.md", PROGRESS_BLOCK, progress_body, required=False)
        )

    problems = [
        problem
        for target in targets
        if target.required and (problem := _setup_problem(target, root)) is not None
    ]
    if problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
        return EXIT_SETUP  # nothing has been written

    code = EXIT_OK
    for target in targets:
        code = max(code, _process(target, root, check=args.check))

    if code == EXIT_OK:
        done, total = _counts(levels)
        print(f"{total} topics across {len(levels)} levels, {done} complete")
    if code == EXIT_OK and args.strict and warnings:
        print("error: layout warnings found (--strict)", file=sys.stderr)
        return EXIT_STALE
    return code


if __name__ == "__main__":
    raise SystemExit(main())
