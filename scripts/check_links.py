#!/usr/bin/env python3
"""Fail if a relative Markdown link (file, folder or #anchor) points at something missing.

Usage:  python scripts/check_links.py [repo_root]      (default: current directory)
Standard library only. Links inside code fences / inline code are ignored.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Set

_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
_FENCE = re.compile(r"```.*?```", re.S)
_INLINE_CODE = re.compile(r"`[^`\n]*`")
_HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$", re.M)
_SKIP_DIRS = {".git", ".venv", "node_modules", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
# shortcut: GitHub-relative links cannot be resolved on disk, so they are allow-listed;
# add to this set when a new one is needed.
_GITHUB_ONLY = {"../../issues"}


def _strip_code(text: str) -> str:
    return _INLINE_CODE.sub("", _FENCE.sub("", text))


def _slug(heading: str) -> str:
    """GitHub-style heading anchor. shortcut: no '-1' suffix for duplicate headings,
    upgrade if two headings in one file ever share a name and are linked to."""
    heading = re.sub(r"[`*_]", "", heading).strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading)
    return heading.replace(" ", "-")


def _anchors(path: Path) -> Set[str]:
    return {_slug(h) for h in _HEADING.findall(_strip_code(path.read_text(encoding="utf-8")))}


def check(root: Path) -> List[str]:
    """Return one error string per broken link under root (empty list = all good)."""
    errors: List[str] = []
    for md in sorted(root.rglob("*.md")):
        if _SKIP_DIRS & set(md.relative_to(root).parts):
            continue
        for link in _LINK.findall(_strip_code(md.read_text(encoding="utf-8"))):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", link) or link in _GITHUB_ONLY:
                continue  # http(s):, mailto:, ...
            file_part, _, anchor = link.partition("#")
            target = (md.parent / file_part).resolve() if file_part else md
            where = f"{md.relative_to(root)}: ({link})"
            if not target.exists():
                errors.append(f"{where} -> missing {file_part}")
            elif anchor and target.suffix == ".md" and anchor.lower() not in _anchors(target):
                errors.append(f"{where} -> no heading #{anchor}")
    return errors


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    errors = check(root)
    for e in errors:
        print(f"Broken link: {e}")
    print(f"{len(errors)} broken link(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
