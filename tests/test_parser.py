"""Tests for the parser (tokens/string -> AST).

Save as: tests/test_parser.py

Written test-first, so they double as the specification. Contract:

    from algebra_tools.symbolic.parser import parse, parse_tokens
    from algebra_tools.symbolic.ast_nodes import Add, Func, Mul, Neg, Num, Pow, Var

    parse(text: str) -> Expr                  (tokenizes, then parses)
    parse_tokens(tokens: Sequence[Token]) -> Expr

AST shapes (frozen dataclasses; field names are used only inside the helpers below):
    Num(value: Fraction)        Var(name)        Neg(operand)       Pow(base, exp)
    Add(terms: tuple)           Mul(factors: tuple)                 Func(name, arg)

Design decisions these tests lock in. They are choices, not laws of nature, so change
a test deliberately if you decide differently:

  1. FAITHFUL, NOT NORMALIZED. The parser records what was written. A chain at one
     precedence level becomes ONE n-ary node ("1+2+3" -> Add of three terms), but
     parentheses are preserved ("1+(2+3)" -> Add(1, Add(2, 3))). Flattening and
     simplifying belong to `simplify`.
  2. No Sub or Div nodes. a-b is Add(a, Neg(b)); a/b is Mul(a, Pow(b, Num(-1))).
  3. A literal "-3" is Neg(Num(3)); the parser never builds a negative literal itself
     (Num(-1) appears only as the exponent standing for division).
  4. Precedence, lowest to highest:  + -   <   * / and implicit multiplication
     <   unary -   <   ^ **   <   atoms.  So -x^2 is Neg(Pow(x, 2)) but -a*b is
     Mul(Neg(a), b).  ^ is right-associative and its exponent may start with '-'.
  5. Implicit multiplication happens before a NAME or '(' only, never before a number.
     Single letters are separate variables ("xy" is x*y). Function names (sin, cos,
     tan, ln, exp, sqrt) need parentheses. "2 3", "x2" and "(x)3" are errors.
  6. Everything at the * / level is left-to-right and flat: "1/2x" is (1/2)*x.
  7. Errors are ParseError with .position = index where parsing could not continue
     (for "unexpected end", that is len(text)).
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import strategies as st

# Skip (rather than fail) until the modules exist, so CI stays green while the engine
# is being built. Once they exist, DELETE these importorskip lines so a missing or
# renamed module becomes a real failure instead of a silent skip.
nodes = pytest.importorskip("algebra_tools.symbolic.ast_nodes")
parser_module = pytest.importorskip("algebra_tools.symbolic.parser")
tokenizer = pytest.importorskip("algebra_tools.symbolic.tokenizer")
errors = pytest.importorskip("algebra_tools.errors")

parse = parser_module.parse
parse_tokens = parser_module.parse_tokens
tokenize = tokenizer.tokenize
ParseError = errors.ParseError

FUNCTIONS = ("sin", "cos", "tan", "ln", "exp", "sqrt")


# ---------------------------------------------------------------------------
# Tiny builders, so a change to a node's constructor touches only this block
# ---------------------------------------------------------------------------


def num(n: int, d: int = 1) -> object:
    return nodes.Num(Fraction(n, d))


def var(name: str) -> object:
    return nodes.Var(name)


def add(*terms: object) -> object:
    return nodes.Add(tuple(terms))


def mul(*factors: object) -> object:
    return nodes.Mul(tuple(factors))


def power(base: object, exp: object) -> object:
    return nodes.Pow(base, exp)


def neg(operand: object) -> object:
    return nodes.Neg(operand)


def func(name: str, arg: object) -> object:
    return nodes.Func(name, arg)


def inv(operand: object) -> object:
    """How division is represented: a / b is mul(a, inv(b))."""
    return nodes.Pow(operand, nodes.Num(Fraction(-1)))


x, y, z = var("x"), var("y"), var("z")
a, b, c = var("a"), var("b"), var("c")
one, two, three = num(1), num(2), num(3)


# ---------------------------------------------------------------------------
# Atoms
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("7", num(7)),
        ("0", num(0)),
        ("0.5", num(1, 2)),
        (".25", num(1, 4)),
        ("3.14", num(314, 100)),  # exact fraction, never a float
        ("x", x),
        ("X", var("X")),  # case-sensitive
        ("(x)", x),
        ("((7))", num(7)),
    ],
)
def test_atoms(text: str, expected: object) -> None:
    assert parse(text) == expected


def test_decimals_are_exact() -> None:
    assert parse("0.1").value + parse("0.2").value == Fraction(3, 10)


# ---------------------------------------------------------------------------
# Addition and subtraction
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1 + 2", add(one, two)),
        ("1 + 2 + 3", add(one, two, three)),  # a chain is ONE n-ary node
        ("x + y + z", add(x, y, z)),
        ("a - b", add(a, neg(b))),  # no Sub node
        ("a - b - c", add(a, neg(b), neg(c))),
        ("a - b + c", add(a, neg(b), c)),
        ("-a + b", add(neg(a), b)),
        ("a + -b", add(a, neg(b))),  # same tree as "a - b"
        ("1 - -2", add(one, neg(neg(two)))),
    ],
)
def test_sums(text: str, expected: object) -> None:
    assert parse(text) == expected


def test_subtraction_and_plus_negative_are_the_same_tree() -> None:
    assert parse("a - b") == parse("a + -b")


# ---------------------------------------------------------------------------
# Multiplication and division
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("a * b", mul(a, b)),
        ("a * b * c", mul(a, b, c)),
        ("a / b", mul(a, inv(b))),  # no Div node
        ("a / b / c", mul(a, inv(b), inv(c))),  # left to right, flat
        ("a * b / c", mul(a, b, inv(c))),
        ("a / b * c", mul(a, inv(b), c)),
        ("2 * -3", mul(two, neg(three))),
        ("-a * b", mul(neg(a), b)),  # unary minus binds tighter than *
        ("a / -b", mul(a, inv(neg(b)))),
    ],
)
def test_products_and_quotients(text: str, expected: object) -> None:
    assert parse(text) == expected


# ---------------------------------------------------------------------------
# Precedence
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1 + 2 * 3", add(one, mul(two, three))),
        ("1 * 2 + 3", add(mul(one, two), three)),
        ("(1 + 2) * 3", mul(add(one, two), three)),
        ("a - b * c", add(a, neg(mul(b, c)))),  # the whole product is negated
        ("a / b + c", add(mul(a, inv(b)), c)),
        ("-x^2", neg(power(x, two))),  # ^ binds tighter than unary minus
        ("(-x)^2", power(neg(x), two)),
        ("2 * 3^2", mul(two, power(three, two))),
    ],
)
def test_precedence(text: str, expected: object) -> None:
    assert parse(text) == expected


# ---------------------------------------------------------------------------
# Parentheses are preserved (the parser does not flatten or simplify)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1 + (2 + 3)", add(one, add(two, three))),
        ("(1 + 2) + 3", add(add(one, two), three)),
        ("a * (b * c)", mul(a, mul(b, c))),
        ("(a * b) * c", mul(mul(a, b), c)),
        ("(a + b)", add(a, b)),  # redundant outer parens vanish
        ("((a + b))", add(a, b)),
    ],
)
def test_parentheses_are_preserved_not_flattened(text: str, expected: object) -> None:
    assert parse(text) == expected


# ---------------------------------------------------------------------------
# Powers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("x^2", power(x, two)),
        ("x ^ 2", power(x, two)),
        ("2^x", power(two, x)),
        ("2^3^2", power(two, power(three, two))),  # right-associative
        ("x^2^3", power(x, power(two, three))),
        ("x^-1", power(x, neg(one))),  # exponent may start with '-'
        ("x^-2", power(x, neg(two))),
        ("x^(a + b)", power(x, add(a, b))),
        ("(x + 1)^2", power(add(x, one), two)),
        ("x^0.5", power(x, num(1, 2))),
    ],
)
def test_powers(text: str, expected: object) -> None:
    assert parse(text) == expected


@pytest.mark.parametrize("text", ["x**2", "x ** 2", "(x+1)**2", "2**3**2"])
def test_double_star_means_the_same_as_caret(text: str) -> None:
    assert parse(text) == parse(text.replace("**", "^"))


# ---------------------------------------------------------------------------
# Implicit multiplication
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("2x", mul(two, x)),
        ("2 x", mul(two, x)),
        ("xy", mul(x, y)),  # single-letter variables
        ("x y", mul(x, y)),
        ("2xy", mul(two, x, y)),
        ("3(x + 1)", mul(three, add(x, one))),
        ("(x + 1)(x - 1)", mul(add(x, one), add(x, neg(one)))),
        ("x(y)", mul(x, y)),  # a product, not a function call
        ("(x)(y)", mul(x, y)),
        ("2x^2", mul(two, power(x, two))),
        ("x^2y", mul(power(x, two), y)),  # ^ attaches only to x
        ("xy^2", mul(x, power(y, two))),  # ^ attaches only to y
        ("2^3x", mul(power(two, three), x)),
        ("-xy", mul(neg(x), y)),
        ("2x + 3y", add(mul(two, x), mul(three, y))),
        ("x - 2y", add(x, neg(mul(two, y)))),
    ],
)
def test_implicit_multiplication(text: str, expected: object) -> None:
    assert parse(text) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # One flat left-to-right chain at the * / level, as decision 6 says.
        # Some calculators read these differently: change deliberately if you do.
        ("1/2x", mul(one, inv(two), x)),  # (1/2)*x, not 1/(2x)
        ("a/bc", mul(a, inv(b), c)),  # (a/b)*c
        ("2x/3y", mul(two, x, inv(three), y)),
    ],
)
def test_division_then_implicit_multiplication_is_left_to_right(
    text: str, expected: object
) -> None:
    assert parse(text) == expected


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("name", FUNCTIONS)
def test_each_function_parses_to_func(name: str) -> None:
    assert parse(f"{name}(x)") == func(name, x)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("sin(x + 1)", func("sin", add(x, one))),
        ("sin(cos(x))", func("sin", func("cos", x))),
        ("2sin(x)", mul(two, func("sin", x))),
        ("x sin(x)", mul(x, func("sin", x))),
        ("sin(x)cos(x)", mul(func("sin", x), func("cos", x))),
        ("sin(x)^2", power(func("sin", x), two)),
        ("-sin(x)", neg(func("sin", x))),
        ("sqrt(x)/2", mul(func("sqrt", x), inv(two))),  # sqrt stays a Func, not Pow(x, 1/2)
        ("ln(x^2)", func("ln", power(x, two))),
    ],
)
def test_function_expressions(text: str, expected: object) -> None:
    assert parse(text) == expected


# ---------------------------------------------------------------------------
# Whitespace and equivalence of entry points
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("compact", "spaced"),
    [
        ("x+1", "  x  +  1 "),
        ("x+1", "x +\n1"),
        ("2x^2", "2 x ^ 2"),
        ("a/b", "a / b"),
        ("(x+1)(x-1)", " ( x + 1 ) ( x - 1 ) "),
    ],
)
def test_spacing_never_changes_the_tree(compact: str, spaced: str) -> None:
    assert parse(compact) == parse(spaced)


@pytest.mark.parametrize("text", ["x + 1", "2x^2 - 3y", "(x+1)(x-1)", "sin(x)/2", "a/b/c"])
def test_parse_tokens_agrees_with_parse(text: str) -> None:
    assert parse_tokens(tokenize(text)) == parse(text)


def test_trees_are_values_that_can_be_hashed_and_compared() -> None:
    assert parse("x + 1") == parse("x+1")
    assert hash(parse("x + 1")) == hash(parse("x+1"))
    assert len({parse("x + 1"), parse("x+1"), parse("x + 2")}) == 2


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "position"),
    [
        ("", 0),  # nothing to parse
        ("   ", 3),  # only whitespace: unexpected end of input
        ("*", 0),
        ("* 2", 0),  # starts with a binary operator
        ("2 +", 3),  # dangling operator: unexpected end
        ("2 *", 3),
        ("2 + * 3", 4),  # operator where an operand should be
        ("2 * / 3", 4),
        ("2 ^ * 3", 4),
        ("x^", 2),
        ("(x", 2),  # unclosed paren: unexpected end
        ("(x + 1", 6),
        ("x)", 1),  # stray closing paren
        ("()", 1),  # empty parens
        ("x = 3", 2),  # '=' belongs to solve, not the expression parser
        ("2 3", 2),  # a number cannot follow a factor
        ("x2", 1),
        ("(x)3", 3),
        ("sin x", 4),  # functions need '(': points at where '(' was expected
        ("sin", 3),
        ("sin()", 4),  # empty argument
        ("3 $ 4", 2),  # tokenizer error, same exception type
        ("1.2.3", 3),
    ],
)
def test_malformed_input_raises_parse_error_at_the_right_place(text: str, position: int) -> None:
    with pytest.raises(ParseError) as info:
        parse(text)
    assert info.value.position == position
    assert str(info.value)


def test_errors_are_algebra_errors() -> None:
    assert issubclass(ParseError, errors.AlgebraError)


# ---------------------------------------------------------------------------
# Property-based tests
# ---------------------------------------------------------------------------

# Characters that exercise operators, parens, functions and implicit multiplication.
FUZZ_ALPHABET = "0123456789.xyz+-*/^()= sincoqrtl"


@given(st.text(alphabet=FUZZ_ALPHABET, max_size=30))
def test_parse_returns_a_tree_or_a_parse_error_nothing_else(text: str) -> None:
    error_position = None
    try:
        parse(text)
    except ParseError as exc:
        error_position = exc.position
    if error_position is not None:
        assert 0 <= error_position <= len(text)


# Source-string generators. Children are always parenthesized, so every generated
# string is valid by construction and we test structure, not luck.
_atoms = st.one_of(
    st.integers(min_value=0, max_value=20).map(str),
    st.sampled_from(["x", "y", "z", "2x", "xy"]),
)


def _extend(children: st.SearchStrategy[str]) -> st.SearchStrategy[str]:
    return st.one_of(
        st.tuples(children, st.sampled_from("+-*/"), children).map(
            lambda t: f"({t[0]}) {t[1]} ({t[2]})"
        ),
        st.tuples(children, st.integers(min_value=0, max_value=5)).map(
            lambda t: f"({t[0]})^{t[1]}"
        ),
        children.map(lambda child: f"-({child})"),
        st.tuples(st.sampled_from(FUNCTIONS), children).map(lambda t: f"{t[0]}({t[1]})"),
    )


_nested = st.recursive(_atoms, _extend, max_leaves=8)
_chains = st.lists(_atoms, min_size=1, max_size=5).flatmap(
    lambda items: st.lists(
        st.sampled_from(["+", "-", "*", "/"]),
        min_size=len(items) - 1,
        max_size=len(items) - 1,
    ).map(lambda ops: "".join(f"{i} {o} " for i, o in zip(items, [*ops, ""], strict=True)).strip())
)
valid_sources = st.one_of(_nested, _chains)


@given(valid_sources)
def test_generated_expressions_always_parse(source: str) -> None:
    parse(source)  # must not raise


@given(valid_sources)
def test_inserting_spaces_between_tokens_never_changes_the_tree(source: str) -> None:
    spaced = " ".join(token.text for token in tokenize(source)[:-1])
    assert parse(spaced) == parse(source)


HAS_PRINTER = importlib.util.find_spec("algebra_tools.symbolic.printer") is not None


@pytest.mark.skipif(not HAS_PRINTER, reason="printer module not written yet")
@given(valid_sources)
def test_print_then_parse_returns_the_same_tree(source: str) -> None:
    from algebra_tools.symbolic.printer import to_text

    tree = parse(source)
    assert parse(to_text(tree)) == tree
