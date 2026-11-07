"""Command-line interface for algebra-tools.

Save as: tools/algebra_tools/cli.py  (matches [project.scripts] in pyproject.toml)

This module is deliberately THIN: it parses arguments, calls into the package,
formats output, and reports errors. It contains no algebra logic (see
ARCHITECTURE.md section 5). Anything the CLI can do must also be callable as a
plain Python function.

Commands
--------
    algebra simplify  "2x + 3x - x"          [--steps] [--format latex] [--json]
    algebra expand    "(x+1)^2"              [--steps] [--format latex] [--json]
    algebra factor    "x^2 - 5x + 6"         [--steps] [--format latex] [--json]
    algebra diff      "x^3 + 2x" --var x     [--steps] [--format latex] [--json]
    algebra solve     "x^2 - 5x + 6 = 0"     [--steps] [--format latex] [--json]
    algebra eval      "x^2 + 1" --set x=3
    algebra check     "x^2-1" --answer "(x-1)(x+1)"
    algebra practice  --topic quadratics --count 5 --seed 42 [--answers] [--markdown]
    algebra topics
    algebra repl

Input conveniences
------------------
    * Pass several expressions at once; each is processed independently.
    * Use "-" as an expression to read one expression per line from stdin
      (blank lines and lines starting with "#" are ignored).
    * Quote expressions: in most shells ^, (, ) and * have special meaning.

Output conveniences
-------------------
    * --steps shows each rewrite rule that was applied.
    * --format latex renders results (and steps) as LaTeX.
    * --json prints one JSON object per input, for scripts and tests.
    * Color is used only on a terminal, and is disabled by --no-color or by
      setting the NO_COLOR environment variable.

Exit codes
----------
    0    success
    1    bad input, a math error, or a failed `check`
    2    command-line usage error (handled by argparse)
    3    feature not implemented yet (engine modules still being built)
    130  interrupted (Ctrl-C)

Assumed engine API
------------------
Adjust the lazy imports in the ``_t_*`` / ``_cmd_*`` functions to match what you
actually build in Phase 3:

    symbolic.parser.parse(text) -> Expr
    symbolic.simplify.simplify(expr) -> Result        # Result.value, Result.steps
    symbolic.expand.expand(expr) -> Result
    symbolic.factor.factor(expr) -> Result
    symbolic.differentiate.differentiate(expr, var) -> Result
    symbolic.solve.solve(text) -> Result
    symbolic.evaluate.evaluate(expr, env) -> Fraction  # env: dict[str, Fraction]
    symbolic.printer.to_text(value) -> str             # handles Expr and solutions
    symbolic.printer.to_latex(value) -> str
    steps.render_steps(steps, latex=False) -> str      # Step.rule/.before/.after
    practice.generator.generate(topic, count, seed, difficulty) -> list[Problem]
                                                       # Problem.prompt / .answer
    practice.checker.is_equivalent(reference, answer) -> bool
    errors.AlgebraError   # base of ParseError, DomainError, NotSupportedError;
                          # ParseError may expose .position (index into the input)
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import secrets
import sys
import traceback
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from fractions import Fraction
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import TYPE_CHECKING, TextIO

if TYPE_CHECKING:
    from algebra_tools.steps import Result, Step

EXIT_OK = 0
EXIT_USER_ERROR = 1
EXIT_NOT_IMPLEMENTED = 3
EXIT_INTERRUPTED = 130

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
DIFFICULTIES: tuple[str, ...] = ("easy", "medium", "hard")
FORMATS: tuple[str, ...] = ("text", "latex")


class NotImplementedYetError(Exception):
    """Raised when a command depends on an engine module that does not exist yet."""


def _not_implemented(feature: str, exc: ImportError) -> NotImplementedYetError:
    """Turn a *missing engine module* into NotImplementedYetError.

    Any other ImportError (a typo, a broken dependency inside an existing
    module) is a real bug, so it is re-raised instead of being hidden.
    """
    if isinstance(exc, ModuleNotFoundError) and (exc.name or "").startswith("algebra_tools"):
        return NotImplementedYetError(feature)
    raise exc


# ---------------------------------------------------------------------------
# Output styling and options
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Style:
    """Tiny ANSI helper. When disabled, every method returns its text unchanged."""

    enabled: bool = False

    def _wrap(self, code: str, text: str) -> str:
        return f"\033[{code}m{text}\033[0m" if self.enabled else text

    def bold(self, text: str) -> str:
        return self._wrap("1", text)

    def dim(self, text: str) -> str:
        return self._wrap("2", text)

    def red(self, text: str) -> str:
        return self._wrap("31", text)

    def green(self, text: str) -> str:
        return self._wrap("32", text)


@dataclass
class Options:
    """Settings shared by every command. Mutable so the REPL can toggle them."""

    steps: bool = False
    fmt: str = "text"
    as_json: bool = False
    quiet: bool = False
    debug: bool = False
    var: str = "x"
    style: Style = field(default_factory=Style)


def _color_supported(stream: TextIO) -> bool:
    """Color only on a real terminal, honoring https://no-color.org/."""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return stream.isatty()


def _options_from(args: argparse.Namespace) -> Options:
    color = not getattr(args, "no_color", False) and _color_supported(sys.stdout)
    return Options(
        steps=getattr(args, "steps", False),
        fmt=getattr(args, "format", "text"),
        as_json=getattr(args, "json", False),
        quiet=getattr(args, "quiet", False),
        debug=getattr(args, "debug", False),
        var=getattr(args, "var", "x"),
        style=Style(color),
    )


def _package_version() -> str:
    try:
        return version("algebra-tools")
    except PackageNotFoundError:  # running from a source checkout, not installed
        return "0.0.0+local"


# ---------------------------------------------------------------------------
# Rendering helpers (lazy imports so `algebra --help` always works)
# ---------------------------------------------------------------------------


def _render(value: object, fmt: str) -> str:
    try:
        from algebra_tools.symbolic import printer
    except ImportError as exc:
        raise _not_implemented("printer", exc) from exc
    return printer.to_latex(value) if fmt == "latex" else printer.to_text(value)


def _steps_text(steps: Sequence[Step], fmt: str) -> str:
    try:
        from algebra_tools.steps import render_steps
    except ImportError as exc:
        raise _not_implemented("step rendering", exc) from exc
    return str(render_steps(steps, latex=(fmt == "latex")))


def _steps_json(steps: Sequence[Step], fmt: str) -> list[dict[str, str]]:
    return [
        {
            "rule": step.rule,
            "before": _render(step.before, fmt),
            "after": _render(step.after, fmt),
        }
        for step in steps
    ]


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


def _is_algebra_error(exc: Exception) -> bool:
    try:
        from algebra_tools.errors import AlgebraError
    except ImportError:
        return False
    return isinstance(exc, AlgebraError)


def _report(exc: Exception, text: str, opts: Options) -> None:
    """Print a friendly error, with a caret under the problem if the position is known."""
    print(opts.style.red(f"error: {exc}"), file=sys.stderr)
    position = getattr(exc, "position", None)
    if isinstance(position, int) and 0 <= position <= len(text):
        print(f"  {text}", file=sys.stderr)
        print("  " + " " * position + "^", file=sys.stderr)
    if opts.debug:
        traceback.print_exception(exc)


def _attempt(text: str, opts: Options, action: Callable[[], int]) -> int:
    """Run one unit of work; report engine errors and keep going, re-raise real bugs."""
    try:
        return action()
    except NotImplementedYetError:
        raise
    except Exception as exc:
        if _is_algebra_error(exc):
            _report(exc, text, opts)
            return EXIT_USER_ERROR
        raise


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------


def _expand_inputs(items: Sequence[str]) -> list[str]:
    """Replace "-" with the non-empty, non-comment lines of stdin."""
    expressions: list[str] = []
    for item in items:
        if item == "-":
            for line in sys.stdin:
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    expressions.append(stripped)
        else:
            expressions.append(item)
    return expressions


def _positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value!r} is not an integer") from None
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def _assignment(value: str) -> tuple[str, Fraction]:
    """Parse NAME=VALUE for `eval --set`, e.g. x=3 or y=1/2 or z=0.25."""
    name, sep, raw = value.partition("=")
    if not sep or not name.isidentifier():
        raise argparse.ArgumentTypeError(f"expected NAME=VALUE, got {value!r}")
    try:
        return name, Fraction(raw)
    except (ValueError, ZeroDivisionError):
        raise argparse.ArgumentTypeError(f"{raw!r} is not a number") from None


# ---------------------------------------------------------------------------
# Transform commands: simplify / expand / factor / diff / solve
# Each loader returns a Result; formatting and error handling are shared.
# ---------------------------------------------------------------------------

Transform = Callable[[str, Options], "Result"]


def _t_simplify(text: str, opts: Options) -> Result:
    try:
        from algebra_tools.symbolic.parser import parse
        from algebra_tools.symbolic.simplify import simplify
    except ImportError as exc:
        raise _not_implemented("simplify", exc) from exc
    return simplify(parse(text))


def _t_expand(text: str, opts: Options) -> Result:
    try:
        from algebra_tools.symbolic.expand import expand
        from algebra_tools.symbolic.parser import parse
    except ImportError as exc:
        raise _not_implemented("expand", exc) from exc
    return expand(parse(text))


def _t_factor(text: str, opts: Options) -> Result:
    try:
        from algebra_tools.symbolic.factor import factor
        from algebra_tools.symbolic.parser import parse
    except ImportError as exc:
        raise _not_implemented("factor", exc) from exc
    return factor(parse(text))


def _t_diff(text: str, opts: Options) -> Result:
    try:
        from algebra_tools.symbolic.differentiate import differentiate
        from algebra_tools.symbolic.parser import parse
    except ImportError as exc:
        raise _not_implemented("diff", exc) from exc
    return differentiate(parse(text), opts.var)


def _t_solve(text: str, opts: Options) -> Result:
    try:
        from algebra_tools.symbolic.solve import solve
    except ImportError as exc:
        raise _not_implemented("solve", exc) from exc
    return solve(text)


TRANSFORMS: dict[str, Transform] = {
    "simplify": _t_simplify,
    "expand": _t_expand,
    "factor": _t_factor,
    "diff": _t_diff,
    "solve": _t_solve,
}


def _run_transform(name: str, text: str, opts: Options, show_input: bool = False) -> int:
    """Run one transform on one input and print the result."""

    def action() -> int:
        result = TRANSFORMS[name](text, opts)
        rendered = _render(result.value, opts.fmt)

        if opts.as_json:
            payload: dict[str, object] = {"command": name, "input": text, "result": rendered}
            if opts.steps:
                payload["steps"] = _steps_json(result.steps, opts.fmt)
            print(json.dumps(payload, ensure_ascii=False))
            return EXIT_OK

        if show_input and not opts.quiet:
            print(opts.style.dim(f"> {text}"))
        if opts.steps and result.steps:
            print(_steps_text(result.steps, opts.fmt))
            print()
        print(opts.style.bold(rendered))
        return EXIT_OK

    return _attempt(text, opts, action)


def _cmd_transform(args: argparse.Namespace, opts: Options) -> int:
    expressions = _expand_inputs(args.expressions)
    show_input = len(expressions) > 1
    worst = EXIT_OK
    for text in expressions:
        worst = max(worst, _run_transform(args.command, text, opts, show_input))
    return worst


# ---------------------------------------------------------------------------
# eval
# ---------------------------------------------------------------------------


def _cmd_eval(args: argparse.Namespace, opts: Options) -> int:
    try:
        from algebra_tools.symbolic.evaluate import evaluate
        from algebra_tools.symbolic.parser import parse
    except ImportError as exc:
        raise _not_implemented("eval", exc) from exc

    env = dict(args.set)
    worst = EXIT_OK
    for text in _expand_inputs(args.expressions):

        def action(text: str = text) -> int:
            value = evaluate(parse(text), env)
            if opts.as_json:
                print(json.dumps({"command": "eval", "input": text, "result": str(value)}))
            else:
                print(opts.style.bold(str(value)))
            return EXIT_OK

        worst = max(worst, _attempt(text, opts, action))
    return worst


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------


def _cmd_check(args: argparse.Namespace, opts: Options) -> int:
    try:
        from algebra_tools.practice.checker import is_equivalent
    except ImportError as exc:
        raise _not_implemented("answer checker", exc) from exc

    def action() -> int:
        equivalent = is_equivalent(args.reference, args.answer)
        if opts.as_json:
            print(json.dumps({"command": "check", "equivalent": equivalent}))
        elif not opts.quiet:
            print(
                opts.style.green("Equivalent") if equivalent else opts.style.red("Not equivalent")
            )
        return EXIT_OK if equivalent else EXIT_USER_ERROR

    return _attempt(args.answer, opts, action)


# ---------------------------------------------------------------------------
# practice and topics
# ---------------------------------------------------------------------------


def _cmd_practice(args: argparse.Namespace, opts: Options) -> int:
    try:
        from algebra_tools.practice.generator import generate
    except ImportError as exc:
        raise _not_implemented("practice generator", exc) from exc

    # Always know the seed, so any worksheet can be reproduced exactly.
    seed: int = args.seed if args.seed is not None else secrets.randbelow(2**31)
    problems = generate(args.topic, args.count, seed, args.difficulty)

    lines: list[str] = []
    if args.markdown:
        lines += [
            f"# Practice: {args.topic.capitalize()}",
            "",
            f"*Difficulty: {args.difficulty} · seed: {seed} · "
            f"reproduce with `algebra practice --topic {args.topic} "
            f"--count {args.count} --difficulty {args.difficulty} --seed {seed}`*",
            "",
        ]
    elif not opts.quiet:
        lines += [f"{args.topic} / {args.difficulty} / seed {seed}", ""]

    lines += [f"{number}. {problem.prompt}" for number, problem in enumerate(problems, start=1)]

    if args.answers:
        lines += ["", "## Answers" if args.markdown else "Answers:"]
        lines += [f"{number}. {problem.answer}" for number, problem in enumerate(problems, start=1)]

    text = "\n".join(lines) + "\n"
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        if not opts.quiet:
            print(f"Wrote {len(problems)} problems to {args.output} (seed {seed})")
    else:
        sys.stdout.write(text)
    return EXIT_OK


def _cmd_topics(args: argparse.Namespace, opts: Options) -> int:
    for topic in TOPICS:
        print(topic)
    return EXIT_OK


# ---------------------------------------------------------------------------
# repl
# ---------------------------------------------------------------------------

REPL_HELP = """\
Type an expression to simplify it, or start with a command:
  simplify|expand|factor|diff|solve <expression>
Settings:
  :steps on|off     show or hide step-by-step traces
  :latex on|off     switch between text and LaTeX output
  :var <name>       variable used by diff (default x)
  :help             show this help
  :quit             leave (Ctrl-D also works)
"""


def _repl_meta(line: str, opts: Options) -> bool:
    """Handle ':' commands. Returns False when the REPL should exit."""
    parts = line[1:].split()
    command = parts[0] if parts else ""
    argument = parts[1] if len(parts) > 1 else ""

    if command in {"q", "quit", "exit"}:
        return False
    if command == "help":
        print(REPL_HELP)
    elif command == "steps" and argument in {"on", "off"}:
        opts.steps = argument == "on"
        print(f"steps {argument}")
    elif command == "latex" and argument in {"on", "off"}:
        opts.fmt = "latex" if argument == "on" else "text"
        print(f"format {opts.fmt}")
    elif command == "var" and argument.isidentifier():
        opts.var = argument
        print(f"variable {argument}")
    else:
        print("unknown command; type :help", file=sys.stderr)
    return True


def _cmd_repl(args: argparse.Namespace, opts: Options) -> int:
    with contextlib.suppress(ImportError):
        import readline  # noqa: F401  (enables arrow-key history where available)

    if not opts.quiet:
        print(f"algebra-tools {_package_version()}  ·  :help for commands, :quit to leave")

    while True:
        try:
            line = input(opts.style.bold("algebra> ")).strip()
        except EOFError:
            print()
            return EXIT_OK
        except KeyboardInterrupt:
            print()
            continue

        if not line:
            continue
        if line.startswith(":"):
            if not _repl_meta(line, opts):
                return EXIT_OK
            continue

        first, _, rest = line.partition(" ")
        name, text = (first, rest.strip()) if first in TRANSFORMS else ("simplify", line)
        if not text:
            print(f"usage: {name} <expression>", file=sys.stderr)
            continue
        try:
            _run_transform(name, text, opts)
        except NotImplementedYetError as exc:
            print(f"{name}: not implemented yet ({exc}).", file=sys.stderr)


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

Handler = Callable[[argparse.Namespace, Options], int]


def _common_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    group = parser.add_argument_group("global options")
    group.add_argument("-q", "--quiet", action="store_true", help="suppress decorative output")
    group.add_argument("--no-color", action="store_true", help="disable ANSI colors")
    group.add_argument("--debug", action="store_true", help="show tracebacks for engine errors")
    return parser


def _render_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    group = parser.add_argument_group("output options")
    group.add_argument("--steps", action="store_true", help="show each rewrite step")
    group.add_argument("--format", choices=FORMATS, default="text", help="output format")
    group.add_argument("--json", action="store_true", help="print one JSON object per input")
    return parser


def build_parser() -> argparse.ArgumentParser:
    common = _common_parser()
    render = _render_parser()

    parser = argparse.ArgumentParser(
        prog="algebra",
        description="Practice, simplify, and solve algebra with step-by-step explanations.",
        epilog='Quote expressions, e.g. algebra simplify "2x + 3x". Use "-" to read from stdin.',
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {_package_version()}")
    sub = parser.add_subparsers(dest="command", required=True, metavar="<command>")

    def add(
        name: str, help_text: str, handler: Handler, *parents: argparse.ArgumentParser
    ) -> argparse.ArgumentParser:
        p = sub.add_parser(name, help=help_text, parents=[common, *parents])
        p.set_defaults(func=handler)
        return p

    transforms = {
        "simplify": ("simplify expressions", '"2x + 3x - x"'),
        "expand": ("expand products and powers", '"(x+1)^2"'),
        "factor": ("factor polynomials", '"x^2 - 5x + 6"'),
        "diff": ("differentiate with respect to a variable", '"x^3 + 2x"'),
        "solve": ("solve equations", '"x^2 - 5x + 6 = 0"'),
    }
    for name, (help_text, example) in transforms.items():
        p = add(name, help_text, _cmd_transform, render)
        p.add_argument(
            "expressions", nargs="+", metavar="EXPR", help=f"e.g. {example}; - for stdin"
        )
        if name == "diff":
            p.add_argument("--var", default="x", help="variable to differentiate by (default x)")

    p = add("eval", "evaluate expressions at given values", _cmd_eval)
    p.add_argument("expressions", nargs="+", metavar="EXPR", help='e.g. "x^2 + 1"; - for stdin')
    p.add_argument(
        "--set",
        action="append",
        default=[],
        type=_assignment,
        metavar="NAME=VALUE",
        help="assign a value (repeatable), e.g. --set x=3 --set y=1/2",
    )
    p.add_argument("--json", action="store_true", help="print one JSON object per input")

    p = add("check", "check an answer against a reference by equivalence", _cmd_check)
    p.add_argument("reference", help="the reference expression")
    p.add_argument("--answer", required=True, help="the answer to check")
    p.add_argument("--json", action="store_true", help="print a JSON object")

    p = add("practice", "generate practice problems", _cmd_practice)
    p.add_argument("--topic", required=True, choices=TOPICS, help="topic to practice")
    p.add_argument(
        "--count", type=_positive_int, default=10, help="number of problems (default 10)"
    )
    p.add_argument("--difficulty", choices=DIFFICULTIES, default="medium", help="default medium")
    p.add_argument("--seed", type=int, default=None, help="seed for reproducible problem sets")
    p.add_argument("--answers", action="store_true", help="append an answer key")
    p.add_argument("--markdown", action="store_true", help="format as a markdown worksheet")
    p.add_argument("--output", metavar="FILE", help="write to FILE instead of stdout")

    add("topics", "list practice topics", _cmd_topics)
    add("repl", "interactive session", _cmd_repl)

    return parser


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    args = build_parser().parse_args(argv)
    opts = _options_from(args)

    try:
        return int(args.func(args, opts))
    except NotImplementedYetError as exc:
        print(f"algebra {args.command}: not implemented yet ({exc}).", file=sys.stderr)
        return EXIT_NOT_IMPLEMENTED
    except KeyboardInterrupt:
        print(file=sys.stderr)
        return EXIT_INTERRUPTED


if __name__ == "__main__":
    raise SystemExit(main())
