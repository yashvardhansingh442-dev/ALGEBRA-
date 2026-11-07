"""Command-line interface for algebra-tools.

Save as: tools/algebra_tools/cli.py  (matches [project.scripts] in pyproject.toml)

This module is deliberately THIN: it parses arguments, calls into the package,
and prints results. It contains no algebra logic (see ARCHITECTURE.md section 5).
Anything the CLI can do must also be callable as a plain Python function.

Usage:
    algebra practice --topic quadratics --count 5 --seed 42
    algebra simplify "2x + 3x - x" --steps
    algebra solve "x^2 - 5x + 6 = 0" --steps
    algebra check "x^2-1" --answer "(x-1)(x+1)"

Tip: quote expressions. In most shells ^, (, ) and * have special meaning.

Exit codes:
    0  success
    1  bad input or a math error (ParseError, DomainError, NotSupportedError)
    2  command-line usage error (handled by argparse)
    3  feature not implemented yet (engine modules still being built)

Assumed engine API (adjust the imports in the _cmd_* functions to match what
you actually build in Phase 3):
    symbolic.parser.parse(text) -> Expr
    symbolic.simplify.simplify(expr) -> Result            # .value, .steps
    symbolic.solve.solve(text) -> Result                  # .value, .steps
    symbolic.printer.to_text(expr) -> str
    steps.render_steps(steps) -> str
    practice.generator.generate(topic, count, seed) -> list[str]
    practice.checker.is_equivalent(reference, answer) -> bool
    errors.AlgebraError  (base class of ParseError, DomainError, NotSupportedError)
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from importlib.metadata import PackageNotFoundError, version

EXIT_OK = 0
EXIT_USER_ERROR = 1
EXIT_NOT_IMPLEMENTED = 3

# Keep in sync with the curriculum topic folders.
TOPICS: tuple[str, ...] = (
    "linear",
    "inequalities",
    "exponents",
    "polynomials",
    "factoring",
    "quadratics",
    "systems",
    "rational",
)


class NotImplementedYet(Exception):
    """Raised when a command depends on an engine module that does not exist yet."""


def _package_version() -> str:
    try:
        return version("algebra-tools")
    except PackageNotFoundError:  # running from a source checkout, not installed
        return "0.0.0+local"


# ---------------------------------------------------------------------------
# Command handlers. Imports are lazy so `algebra --help` always works, even
# while parts of the engine are still unwritten.
# ---------------------------------------------------------------------------


def _cmd_practice(args: argparse.Namespace) -> int:
    try:
        from algebra_tools.practice.generator import generate
    except ImportError as exc:
        raise NotImplementedYet("practice generator") from exc

    problems = generate(args.topic, args.count, args.seed)
    for number, problem in enumerate(problems, start=1):
        print(f"{number}. {problem}")
    return EXIT_OK


def _cmd_simplify(args: argparse.Namespace) -> int:
    try:
        from algebra_tools.steps import render_steps
        from algebra_tools.symbolic.parser import parse
        from algebra_tools.symbolic.printer import to_text
        from algebra_tools.symbolic.simplify import simplify
    except ImportError as exc:
        raise NotImplementedYet("simplify") from exc

    result = simplify(parse(args.expression))
    if args.steps:
        print(render_steps(result.steps))
    print(to_text(result.value))
    return EXIT_OK


def _cmd_solve(args: argparse.Namespace) -> int:
    try:
        from algebra_tools.steps import render_steps
        from algebra_tools.symbolic.solve import solve
    except ImportError as exc:
        raise NotImplementedYet("solve") from exc

    result = solve(args.equation)
    if args.steps:
        print(render_steps(result.steps))
    print(result.value)
    return EXIT_OK


def _cmd_check(args: argparse.Namespace) -> int:
    try:
        from algebra_tools.practice.checker import is_equivalent
    except ImportError as exc:
        raise NotImplementedYet("answer checker") from exc

    if is_equivalent(args.reference, args.answer):
        print("Equivalent")
        return EXIT_OK
    print("Not equivalent")
    return EXIT_USER_ERROR


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="algebra",
        description="Practice, simplify, and solve algebra with step-by-step explanations.",
        epilog="Quote expressions, e.g. algebra simplify \"2x + 3x\".",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {_package_version()}")
    sub = parser.add_subparsers(dest="command", required=True, metavar="<command>")

    p = sub.add_parser("practice", help="generate practice problems")
    p.add_argument("--topic", required=True, choices=TOPICS, help="topic to practice")
    p.add_argument("--count", type=_positive_int, default=10, help="number of problems (default 10)")
    p.add_argument("--seed", type=int, default=None, help="seed for reproducible problem sets")
    p.set_defaults(func=_cmd_practice)

    p = sub.add_parser("simplify", help="simplify an expression")
    p.add_argument("expression", help='expression, e.g. "2x + 3x - x"')
    p.add_argument("--steps", action="store_true", help="show each rewrite step")
    p.set_defaults(func=_cmd_simplify)

    p = sub.add_parser("solve", help="solve an equation")
    p.add_argument("equation", help='equation, e.g. "x^2 - 5x + 6 = 0"')
    p.add_argument("--steps", action="store_true", help="show each solving step")
    p.set_defaults(func=_cmd_solve)

    p = sub.add_parser("check", help="check whether an answer is equivalent to a reference")
    p.add_argument("reference", help="the reference expression")
    p.add_argument("--answer", required=True, help="the answer to check")
    p.set_defaults(func=_cmd_check)

    return parser


def _positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    args = build_parser().parse_args(argv)

    try:
        return int(args.func(args))
    except NotImplementedYet as exc:
        print(f"algebra {args.command}: not implemented yet ({exc}).", file=sys.stderr)
        return EXIT_NOT_IMPLEMENTED
    except Exception as exc:  # noqa: BLE001 - see below
        # Engine errors (ParseError, DomainError, NotSupportedError) all derive
        # from AlgebraError, which may not exist yet, so match by lineage lazily.
        if _is_algebra_error(exc):
            print(f"error: {exc}", file=sys.stderr)
            return EXIT_USER_ERROR
        raise


def _is_algebra_error(exc: Exception) -> bool:
    try:
        from algebra_tools.errors import AlgebraError
    except ImportError:
        return False
    return isinstance(exc, AlgebraError)


if __name__ == "__main__":
    raise SystemExit(main())
