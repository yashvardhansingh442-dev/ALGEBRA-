"""Tests for the tokenizer (string -> tokens).

Save as: tests/test_tokenizer.py

These tests are written BEFORE the module (test-first), so they double as the
specification. The contract they pin down:

    from algebra_tools.symbolic.tokenizer import Token, TokenKind, tokenize

    tokenize(text: str) -> list[Token]

    Token       immutable; fields: kind (TokenKind), text (str), position (int)
    TokenKind   NUMBER, NAME, PLUS, MINUS, STAR, SLASH, CARET,
                LPAREN, RPAREN, EQUALS, EOF

Rules:
    * Whitespace separates tokens and is otherwise ignored.
    * The list always ends with one EOF token whose position is len(text).
    * NUMBER: digits with at most one '.', e.g. 7, 3.14, .5 (text kept as written).
    * NAME: a maximal run of ASCII letters. "xy" and "sin" are each ONE token here;
      deciding that "xy" means x*y is the parser's job, not the tokenizer's.
    * A letter and a digit never join: "x2" is NAME then NUMBER, "2x" is NUMBER then NAME.
    * '**' is a single CARET token (text "**"), the same kind as '^'.
    * '=' is tokenized (EQUALS) so solve can split equations; the parser rejects it.
    * Bad input raises ParseError with .position = index of the offending character.

If you design something different, change the tests deliberately. That is the point
of writing them first.
"""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

# Skip (rather than fail) until the module exists, so CI stays green while the engine
# is being built. Once the module is in place, DELETE these importorskip lines so a
# missing or renamed module becomes a real failure instead of a silent skip.
tokenizer = pytest.importorskip("algebra_tools.symbolic.tokenizer")
errors = pytest.importorskip("algebra_tools.errors")

tokenize = tokenizer.tokenize
K = tokenizer.TokenKind
ParseError = errors.ParseError


def kinds(text: str) -> list:
    """Token kinds for ``text``, without the trailing EOF."""
    return [token.kind for token in tokenize(text)][:-1]


def texts(text: str) -> list[str]:
    """Token texts for ``text``, without the trailing EOF."""
    return [token.text for token in tokenize(text)][:-1]


# ---------------------------------------------------------------------------
# Structure: EOF
# ---------------------------------------------------------------------------


def test_empty_input_is_just_eof() -> None:
    tokens = tokenize("")
    assert [t.kind for t in tokens] == [K.EOF]
    assert tokens[0].position == 0


@pytest.mark.parametrize("text", ["x", "2 + 3", "2 + 3   ", "   ", "(x)"])
def test_stream_ends_with_one_eof_at_end_of_input(text: str) -> None:
    tokens = tokenize(text)
    assert tokens[-1].kind == K.EOF
    assert tokens[-1].position == len(text)
    assert [t.kind for t in tokens].count(K.EOF) == 1


# ---------------------------------------------------------------------------
# Numbers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("text", ["7", "42", "0", "3.14", "0.5", ".5", "100.25"])
def test_number_is_one_token_with_text_kept_as_written(text: str) -> None:
    assert kinds(text) == [K.NUMBER]
    assert texts(text) == [text]


def test_whitespace_splits_numbers() -> None:
    assert texts("2 3") == ["2", "3"]  # the tokenizer does not merge or reject these


# ---------------------------------------------------------------------------
# Names
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("text", ["x", "X", "xy", "sin", "sqrt", "abc"])
def test_letter_run_is_a_single_name_token(text: str) -> None:
    assert kinds(text) == [K.NAME]
    assert texts(text) == [text]


def test_function_names_are_ordinary_names_at_this_level() -> None:
    # Telling "sin" apart from "s*i*n" is the parser's responsibility.
    assert kinds("sin(x)") == [K.NAME, K.LPAREN, K.NAME, K.RPAREN]


def test_digit_then_letter_splits() -> None:
    assert kinds("2x") == [K.NUMBER, K.NAME]
    assert texts("2xy") == ["2", "xy"]


def test_letter_then_digit_splits() -> None:
    assert kinds("x2") == [K.NAME, K.NUMBER]


def test_names_are_case_sensitive() -> None:
    assert texts("xX") == ["xX"]  # preserved exactly, never lower-cased


# ---------------------------------------------------------------------------
# Operators and punctuation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "kind"),
    [
        ("+", K.PLUS),
        ("-", K.MINUS),
        ("*", K.STAR),
        ("/", K.SLASH),
        ("^", K.CARET),
        ("**", K.CARET),
        ("(", K.LPAREN),
        (")", K.RPAREN),
        ("=", K.EQUALS),
    ],
)
def test_single_symbol_kinds(text: str, kind: object) -> None:
    assert kinds(text) == [kind]
    assert texts(text) == [text]


def test_double_star_is_one_caret_token() -> None:
    assert kinds("x**2") == [K.NAME, K.CARET, K.NUMBER]
    assert texts("x**2") == ["x", "**", "2"]


def test_separated_stars_are_two_tokens() -> None:
    assert kinds("* *") == [K.STAR, K.STAR]


def test_triple_star_is_caret_then_star() -> None:
    assert kinds("***") == [K.CARET, K.STAR]


# ---------------------------------------------------------------------------
# Whitespace and positions
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    ["x+1", "x + 1", "  x  +  1  ", "x\t+\t1", "x\n+\n1", "x +\r\n 1"],
)
def test_whitespace_is_ignored(text: str) -> None:
    assert kinds(text) == [K.NAME, K.PLUS, K.NUMBER]
    assert texts(text) == ["x", "+", "1"]


def test_positions_are_character_indexes_into_the_input() -> None:
    #           0123456
    tokens = tokenize("2x + 13")
    assert [(t.text, t.position) for t in tokens] == [
        ("2", 0),
        ("x", 1),
        ("+", 3),
        ("13", 5),
        ("", 7),  # EOF
    ]


def test_a_realistic_expression() -> None:
    assert kinds("(x+1)**2/3") == [
        K.LPAREN,
        K.NAME,
        K.PLUS,
        K.NUMBER,
        K.RPAREN,
        K.CARET,
        K.NUMBER,
        K.SLASH,
        K.NUMBER,
    ]


def test_equation_tokenizes_with_equals() -> None:
    assert kinds("x^2 - 5x + 6 = 0") == [
        K.NAME,
        K.CARET,
        K.NUMBER,
        K.MINUS,
        K.NUMBER,
        K.NAME,
        K.PLUS,
        K.NUMBER,
        K.EQUALS,
        K.NUMBER,
    ]


# ---------------------------------------------------------------------------
# Token objects
# ---------------------------------------------------------------------------


def test_tokens_are_immutable() -> None:
    token = tokenize("x")[0]
    with pytest.raises(AttributeError):
        token.text = "y"  # type: ignore[misc]


def test_tokens_compare_by_value_and_are_hashable() -> None:
    assert tokenize("x + 1") == tokenize("x + 1")
    assert tokenize("x")[0] != tokenize("y")[0]
    assert len({tokenize("x")[0], tokenize("x")[0]}) == 1


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("text", "position"),
    [
        ("$", 0),
        ("2 $ 3", 2),
        ("x # y", 2),
        ("2 + ?", 4),
        ("x!", 1),
        ("a_b", 1),
        ("1.2.3", 3),  # second '.' in one number
        (".", 0),  # a lone dot is not a number
        ("3 + 4.5.6", 7),
    ],
)
def test_bad_input_raises_parse_error_at_the_offending_character(text: str, position: int) -> None:
    with pytest.raises(ParseError) as info:
        tokenize(text)
    assert info.value.position == position
    assert str(info.value)  # has a human-readable message


def test_parse_error_is_an_algebra_error() -> None:
    assert issubclass(ParseError, errors.AlgebraError)


# ---------------------------------------------------------------------------
# Nice-to-have input conveniences (optional; delete or implement as you like)
# ---------------------------------------------------------------------------
# xfail(strict=False): these are expected to fail until you add the feature, and
# will report XPASS (not an error) once you do.


@pytest.mark.xfail(reason="optional: normalize pasted unicode operators", strict=False)
@pytest.mark.parametrize(
    ("text", "kind"),
    [("\u2212", K.MINUS), ("\u00d7", K.STAR), ("\u00f7", K.SLASH), ("\u00b7", K.STAR)],
)
def test_unicode_operators_are_accepted(text: str, kind: object) -> None:
    assert kinds(f"x {text} y") == [K.NAME, kind, K.NAME]


# ---------------------------------------------------------------------------
# Property-based tests
# ---------------------------------------------------------------------------

# Small alphabet, so Hypothesis hits interesting combinations (dots, '**', digits
# next to letters) far more often than it would with arbitrary text.
ALPHABET = "0123456789.xyz+-*/^()= \t\n"


@given(st.text(alphabet=ALPHABET, max_size=40))
def test_tokenizing_never_crashes_and_is_lossless(text: str) -> None:
    error_position = None
    try:
        tokens = tokenize(text)
    except ParseError as exc:
        error_position = exc.position
    if error_position is not None:
        # The only allowed failure, and it must point inside the input.
        assert 0 <= error_position < len(text)
        return

    # Lossless: the token texts, joined, are the input minus whitespace.
    assert "".join(t.text for t in tokens) == "".join(text.split())

    # Each token's position points at its own text in the original input.
    for token in tokens[:-1]:
        assert text[token.position : token.position + len(token.text)] == token.text

    # Positions strictly increase, and the stream ends with EOF at len(text).
    positions = [t.position for t in tokens]
    assert positions == sorted(set(positions))
    assert tokens[-1].kind == K.EOF
    assert tokens[-1].position == len(text)


@given(st.text(alphabet=ALPHABET, max_size=40))
def test_tokenizing_is_deterministic(text: str) -> None:
    def run() -> object:
        try:
            return tokenize(text)
        except ParseError as exc:
            return ("error", exc.position)

    assert run() == run()
