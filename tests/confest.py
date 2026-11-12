"""Shared pytest configuration for ALGEBRA-.

Save as: tests/conftest.py

What lives here
---------------
1. Hypothesis profiles (``dev``, ``ci``, ``thorough``) so property tests run
   fast locally and hard in CI.
2. An automatic ``property`` marker for everything under ``tests/property/``.
3. Reusable fixtures for the numeric cross-check described in
   ARCHITECTURE.md section 7:
       - ``rng``                a seeded random generator (reproducible failures)
       - ``sample_points``      a factory for random rational test points
       - ``assert_equivalent``  "do these two expressions mean the same thing?"

Choosing a Hypothesis profile
-----------------------------
    pytest                                  # "dev": fast, for everyday work
    pytest --hypothesis-profile=ci          # what GitHub Actions runs
    pytest --hypothesis-profile=thorough    # deep local fuzzing before a release
    HYPOTHESIS_PROFILE=ci pytest            # same thing via an environment variable
"""

from __future__ import annotations

import os
import random
from collections.abc import Callable, Sequence
from fractions import Fraction

import pytest
from hypothesis import HealthCheck, settings

# ---------------------------------------------------------------------------
# Hypothesis profiles
# ---------------------------------------------------------------------------

# Everyday local runs: quick feedback.
settings.register_profile(
    "dev",
    max_examples=25,
    deadline=1000,  # milliseconds; a slow example is usually a real performance bug
)

# GitHub Actions: more examples, and *deterministic* so a failure in CI can be
# reproduced locally with the same profile. No deadline, because shared CI
# machines have noisy timing and a flaky deadline failure teaches nothing.
settings.register_profile(
    "ci",
    max_examples=200,
    derandomize=True,
    deadline=None,
    print_blob=True,
    suppress_health_check=[HealthCheck.too_slow],
)

# Slow, deep fuzzing: run before a release or after changing a rewrite rule.
settings.register_profile(
    "thorough",
    max_examples=2000,
    deadline=None,
    suppress_health_check=[HealthCheck.too_slow],
)

# Default to "dev". A --hypothesis-profile=... flag on the command line is
# applied later by Hypothesis' pytest plugin and overrides this.
settings.load_profile(os.environ.get("HYPOTHESIS_PROFILE", "dev"))


# ---------------------------------------------------------------------------
# Markers
# ---------------------------------------------------------------------------


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Mark every test under tests/property/ as ``property``.

    Lets you run (``pytest -m property``) or skip (``pytest -m "not property"``)
    the slower property-based tests without decorating each one by hand.
    """
    for item in items:
        path = str(item.path).replace(os.sep, "/")
        if "/tests/property/" in path:
            item.add_marker(pytest.mark.property)


# ---------------------------------------------------------------------------
# Randomness
# ---------------------------------------------------------------------------

# Fixed seed: a numeric cross-check that fails must fail the same way every time.
RNG_SEED = 20240601


@pytest.fixture
def rng() -> random.Random:
    """A fresh, seeded random generator for each test."""
    return random.Random(RNG_SEED)


# Small, "nice" rationals that avoid zero and one so that expressions such as
# 1/x or x^2 - 1 don't land on a singularity or a coincidental root.
_POINT_POOL: tuple[Fraction, ...] = (
    Fraction(-7, 3),
    Fraction(-2),
    Fraction(-1, 2),
    Fraction(1, 3),
    Fraction(3, 2),
    Fraction(5, 2),
    Fraction(4),
    Fraction(7, 5),
)


@pytest.fixture
def sample_points(rng: random.Random) -> Callable[..., list[dict[str, Fraction]]]:
    """Factory: ``sample_points(("x", "y"), n=8)`` -> list of {name: Fraction}."""

    def make(variables: Sequence[str] = ("x",), n: int = 8) -> list[dict[str, Fraction]]:
        return [{name: rng.choice(_POINT_POOL) for name in variables} for _ in range(n)]

    return make


# ---------------------------------------------------------------------------
# Numeric cross-check
# ---------------------------------------------------------------------------


@pytest.fixture
def assert_equivalent(
    sample_points: Callable[..., list[dict[str, Fraction]]],
) -> Callable[..., None]:
    """Assert two expressions agree at many random points.

    Usage::

        def test_expand_is_correct(assert_equivalent):
            assert_equivalent("(x+1)^2", "x^2 + 2x + 1")

        def test_two_variables(assert_equivalent):
            assert_equivalent("(x+y)^2", "x^2 + 2xy + y^2", variables=("x", "y"))

    This tests *meaning*, not shape, so it catches a wrong rewrite rule that a
    string comparison would miss. Points where either side is undefined
    (division by zero, ln of a non-positive number) are skipped, but at least
    ``minimum`` points must be usable or the check fails.

    The test is skipped, not failed, until the engine modules exist.
    """
    parser = pytest.importorskip("algebra_tools.symbolic.parser")
    evaluator = pytest.importorskip("algebra_tools.symbolic.evaluate")
    errors = pytest.importorskip("algebra_tools.errors")

    def check(
        left: str,
        right: str,
        variables: Sequence[str] = ("x",),
        n: int = 8,
        minimum: int = 3,
    ) -> None:
        left_expr = parser.parse(left)
        right_expr = parser.parse(right)

        usable = 0
        for point in sample_points(variables, n):
            try:
                a = evaluator.evaluate(left_expr, point)
                b = evaluator.evaluate(right_expr, point)
            except errors.DomainError:
                continue  # undefined here; try another point
            usable += 1
            assert a == b, f"{left!r} and {right!r} differ at {point}: {a} != {b}"

        assert usable >= minimum, (
            f"only {usable} of {n} sample points were defined for {left!r} / {right!r}; "
            "cannot confirm equivalence"
        )

    return check


# ---------------------------------------------------------------------------
# Isolation helpers
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _plain_output(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep CLI output free of ANSI color codes so assertions stay simple."""
    monkeypatch.setenv("NO_COLOR", "1")
