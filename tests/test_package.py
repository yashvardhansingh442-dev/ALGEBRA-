"""Tests for the package's top-level API (algebra_tools/__init__.py).

Save as: tests/test_package.py

They check the lazy re-export mechanism, not any algebra, so they pass today and
keep passing as engine modules are added.
"""

from __future__ import annotations

import pytest

import algebra_tools


def test_version_is_a_non_empty_string() -> None:
    assert isinstance(algebra_tools.__version__, str)
    assert algebra_tools.__version__


def test_all_has_no_duplicates_and_includes_version() -> None:
    assert "__version__" in algebra_tools.__all__
    assert len(algebra_tools.__all__) == len(set(algebra_tools.__all__))


def test_dir_lists_every_public_name() -> None:
    listed = dir(algebra_tools)
    for name in algebra_tools.__all__:
        assert name in listed


def test_unknown_attribute_is_an_ordinary_attribute_error() -> None:
    with pytest.raises(AttributeError, match="no attribute 'definitely_not_a_thing'"):
        _ = algebra_tools.definitely_not_a_thing  # type: ignore[attr-defined]


def test_unknown_name_cannot_be_imported() -> None:
    with pytest.raises(ImportError):
        from algebra_tools import definitely_not_a_thing  # noqa: F401


@pytest.mark.parametrize("name", sorted(set(algebra_tools.__all__) - {"__version__"}))
def test_each_public_name_resolves_or_says_it_is_not_implemented_yet(name: str) -> None:
    """Never a crash or a cryptic ImportError: either the object, or a clear message."""
    try:
        value = getattr(algebra_tools, name)
    except AttributeError as exc:
        message = str(exc)
    else:
        assert value is not None
        return
    assert "not available yet" in message
    assert not hasattr(algebra_tools, name)  # hasattr() stays False, not an error


def test_resolved_names_are_cached_on_the_module() -> None:
    for name in ("AlgebraError", "ParseError", "parse"):
        try:
            first = getattr(algebra_tools, name)
        except AttributeError:
            continue  # module not written yet
        assert name in vars(algebra_tools)  # cached by __getattr__
        assert getattr(algebra_tools, name) is first
