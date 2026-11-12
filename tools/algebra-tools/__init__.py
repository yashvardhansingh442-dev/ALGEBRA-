"""algebra-tools: a from-scratch symbolic algebra engine that shows its steps.

Save as: tools/algebra_tools/__init__.py

Quick start (a plain-Python API for everything the ``algebra`` CLI can do)::

    import algebra_tools as at

    expr = at.parse("2x + 3x - x")
    result = at.simplify(expr)          # result.value, result.steps
    print(at.to_text(result.value))
    print(at.render_steps(result.steps))

    at.is_equivalent("x^2 - 1", "(x-1)(x+1)")

Package map (see docs/ARCHITECTURE.md for the full picture)::

    algebra_tools.errors        ParseError, DomainError, NotSupportedError
    algebra_tools.steps         Step, Result, render_steps
    algebra_tools.symbolic      tokenizer -> parser -> AST -> simplify/expand/factor/
                                solve/differentiate -> printer
    algebra_tools.practice      problem generator, answer checker
    algebra_tools.numeric       Newton's method, Gaussian elimination
    algebra_tools.optimization  Lagrange multipliers
    algebra_tools.cli           the ``algebra`` command-line interface

Design notes
------------
* The most useful names are re-exported here, but **lazily** (PEP 562). Importing
  ``algebra_tools`` stays instant and never fails because one engine module is
  still unwritten; a name is only imported the first time it is used.
* A name whose module does not exist yet raises ``AttributeError`` with a clear
  "not available yet" message instead of crashing the whole package.
* Any *other* import problem (a typo or a broken dependency inside a module that
  does exist) is deliberately NOT hidden: it propagates as a normal exception.
* Runtime dependencies: none. The package uses only the standard library.
"""

from __future__ import annotations

import importlib
from importlib.metadata import PackageNotFoundError, version

# Single source of truth for the version is pyproject.toml; read it from the
# installed metadata. From a plain source checkout (not installed) fall back.
try:
    __version__ = version("algebra-tools")
except PackageNotFoundError:
    __version__ = "0.0.0+local"

# ---------------------------------------------------------------------------
# Public API: name -> module (relative to this package) that defines it.
# Add a line here when you add something worth importing from the top level.
# ---------------------------------------------------------------------------
_LAZY: dict[str, str] = {
    # errors
    "AlgebraError": "errors",
    "ParseError": "errors",
    "DomainError": "errors",
    "NotSupportedError": "errors",
    # step traces
    "Step": "steps",
    "Result": "steps",
    "render_steps": "steps",
    # expression tree
    "Expr": "symbolic.ast_nodes",
    "Num": "symbolic.ast_nodes",
    "Var": "symbolic.ast_nodes",
    "Add": "symbolic.ast_nodes",
    "Mul": "symbolic.ast_nodes",
    "Pow": "symbolic.ast_nodes",
    "Neg": "symbolic.ast_nodes",
    "Func": "symbolic.ast_nodes",
    # parsing and printing
    "tokenize": "symbolic.tokenizer",
    "parse": "symbolic.parser",
    "parse_tokens": "symbolic.parser",
    "to_text": "symbolic.printer",
    "to_latex": "symbolic.printer",
    # transforms
    "simplify": "symbolic.simplify",
    "expand": "symbolic.expand",
    "factor": "symbolic.factor",
    "differentiate": "symbolic.differentiate",
    "solve": "symbolic.solve",
    "evaluate": "symbolic.evaluate",
    # practice
    "generate": "practice.generator",
    "is_equivalent": "practice.checker",
}

# NOTE: ``from algebra_tools import *`` imports every name below, so it only
# succeeds once all of the modules above exist. Until then, import names
# explicitly (``from algebra_tools import parse``).
__all__ = ["__version__", *sorted(_LAZY)]


def __getattr__(name: str) -> object:
    """Import a re-exported name on first use (PEP 562)."""
    module_path = _LAZY.get(name)
    if module_path is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    try:
        module = importlib.import_module(f"{__name__}.{module_path}")
    except ModuleNotFoundError as exc:
        # Only translate "a module of OURS is not written yet". A missing
        # third-party package or any other error is a real problem: re-raise.
        if exc.name is not None and exc.name.startswith(f"{__name__}."):
            raise AttributeError(
                f"{name!r} is not available yet: module {exc.name!r} has not been implemented"
            ) from exc
        raise

    try:
        value = getattr(module, name)
    except AttributeError as exc:
        # The module exists but is still being written and does not define this yet.
        raise AttributeError(
            f"{name!r} is not available yet: {module.__name__!r} does not define it"
        ) from exc
    globals()[name] = value  # cache, so __getattr__ runs at most once per name
    return value


def __dir__() -> list[str]:
    return sorted([*globals(), *_LAZY])


# ---------------------------------------------------------------------------
# For IDE autocomplete and type checkers. Uncomment once the modules exist
# (before then, mypy would report them as missing imports):
#
# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from algebra_tools.errors import AlgebraError, DomainError, NotSupportedError, ParseError
#     from algebra_tools.practice.checker import is_equivalent
#     from algebra_tools.practice.generator import generate
#     from algebra_tools.steps import Result, Step, render_steps
#     from algebra_tools.symbolic.ast_nodes import Add, Expr, Func, Mul, Neg, Num, Pow, Var
#     from algebra_tools.symbolic.differentiate import differentiate
#     from algebra_tools.symbolic.evaluate import evaluate
#     from algebra_tools.symbolic.expand import expand
#     from algebra_tools.symbolic.factor import factor
#     from algebra_tools.symbolic.parser import parse, parse_tokens
#     from algebra_tools.symbolic.printer import to_latex, to_text
#     from algebra_tools.symbolic.simplify import simplify
#     from algebra_tools.symbolic.solve import solve
#     from algebra_tools.symbolic.tokenizer import tokenize
