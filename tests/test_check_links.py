"""Tests for tools/check_links.py: it must pass good links and reject every kind of bad one."""
from pathlib import Path

from check_links import check


def _write(root: Path, name: str, text: str) -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_valid_file_folder_and_anchor_links_pass(tmp_path):
    _write(tmp_path, "README.md", "# Title\n## What's inside\n[a](docs/a.md) [d](docs) [s](#whats-inside)\n")
    _write(tmp_path, "docs/a.md", "# A\n[back](../README.md#title)\n")
    assert check(tmp_path) == []


def test_missing_file_is_reported(tmp_path):
    _write(tmp_path, "README.md", "[x](nope.md)\n")
    errors = check(tmp_path)
    assert len(errors) == 1 and "nope.md" in errors[0]


def test_missing_folder_is_reported(tmp_path):
    _write(tmp_path, "README.md", "[x](curriculum/07-missing)\n")
    assert len(check(tmp_path)) == 1


def test_broken_anchor_same_file_and_other_file(tmp_path):
    _write(tmp_path, "README.md", "# Real\n[bad](#fake) [bad2](a.md#fake) [ok](a.md#real-a)\n")
    _write(tmp_path, "a.md", "# Real A\n")
    errors = check(tmp_path)
    assert len(errors) == 2 and all("fake" in e for e in errors)


def test_links_inside_code_are_ignored(tmp_path):
    _write(tmp_path, "README.md", "```\n[x](nope.md)\n```\nand `[y](nope2.md)` inline\n")
    assert check(tmp_path) == []


def test_external_and_github_relative_links_are_not_checked(tmp_path):
    _write(tmp_path, "README.md", "[w](https://example.com/x) [m](mailto:a@b.c) [i](../../issues)\n")
    assert check(tmp_path) == []


def test_real_repo_has_no_broken_links():
    repo_root = Path(__file__).resolve().parent.parent
    assert check(repo_root) == []
