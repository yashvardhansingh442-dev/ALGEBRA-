"""
Algebra problem generator and answer checker.

Generates randomized practice problems for the topics in this repo (Foundations
arithmetic and Linear Equations) and checks learner answers exactly.

Library use:
    from algebra_tools.generator import generate, Difficulty

    problem = generate("linear-equations", difficulty=Difficulty.MEDIUM, seed=42)
    print(problem.prompt)           # e.g. "8x - 1 = 5x - 4"
    print(problem.check("-1"))      # True or False
    print(problem.solution_text())  # step-by-step working

CLI use: python -m algebra_tools (see cli.py)
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass
from enum import Enum
from fractions import Fraction
from typing import Callable, Dict, Optional, Tuple, Union


class Difficulty(str, Enum):
    """Problem difficulty. A str subclass, so ``Difficulty.EASY == "easy"`` is True."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    @classmethod
    def coerce(cls, value: Union[str, "Difficulty"]) -> "Difficulty":
        """Accept a Difficulty or its string name; raise a helpful ValueError otherwise."""
        try:
            return cls(value)
        except ValueError:
            names = ", ".join(d.value for d in cls)
            raise ValueError(f"difficulty must be one of: {names} (got {value!r})") from None


# (low, high) range for the numbers used in a problem at each difficulty.
_RANGES: Dict[Difficulty, Tuple[int, int]] = {
    Difficulty.EASY: (1, 10),
    Difficulty.MEDIUM: (-15, 15),
    Difficulty.HARD: (-25, 25),
}

_INT_RE = re.compile(r"[+-]?\d+")
_FRACTION_RE = re.compile(r"([+-]?\d+)\s*/\s*(\d+)")
_DECIMAL_RE = re.compile(r"[+-]?(\d+\.?\d*|\.\d+)")


def _parse_answer(raw: object) -> Optional[Fraction]:
    """Turn a learner answer into an exact Fraction, or None if it is not a number.

    Strings are parsed exactly ("1/2", "1 / 2", "0.5"); "0.33333" is the rational
    33333/100000, not 1/3. Floats are handled separately in Problem.check.
    """
    if isinstance(raw, bool):  # True would otherwise be read as 1
        return None
    if isinstance(raw, Fraction):
        return raw
    if isinstance(raw, int):
        return Fraction(raw)
    if isinstance(raw, str):
        s = raw.strip()
        m = _FRACTION_RE.fullmatch(s)
        if m:
            den = int(m.group(2))
            return Fraction(int(m.group(1)), den) if den else None
        if _INT_RE.fullmatch(s) or _DECIMAL_RE.fullmatch(s):
            return Fraction(s)
    return None


@dataclass(frozen=True)
class Problem:
    """A generated problem: the prompt shown to the learner, its exact answer, and working."""

    prompt: str
    answer: Fraction
    topic: str
    difficulty: Difficulty
    explanation: str = ""
    steps: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # frozen dataclass: object.__setattr__ normalises the inputs once, at construction.
        object.__setattr__(self, "difficulty", Difficulty.coerce(self.difficulty))
        object.__setattr__(self, "steps", tuple(self.steps))

    def __str__(self) -> str:
        return self.prompt

    def check(self, user_answer: object) -> bool:
        """True only if the answer is exactly right; never raises.

        Accepts int, Fraction, str ("3/4", "1 / 2", "0.5") and float. Anything that is
        not a number, or that divides by zero, is simply wrong.
        """
        if isinstance(user_answer, float):
            # shortcut: floats must equal the double nearest the answer, so 0.5 matches
            # 1/2 and 0.3333333333333333 matches 1/3 but 0.33333 does not; upgrade if
            # the CLI ever needs to accept rounded answers.
            return user_answer == float(self.answer)
        parsed = _parse_answer(user_answer)
        return parsed is not None and parsed == self.answer

    def answer_display(self) -> str:
        """Whole number if possible, else 'p/q'."""
        if self.answer.denominator == 1:
            return str(self.answer.numerator)
        return f"{self.answer.numerator}/{self.answer.denominator}"

    def solution_text(self) -> str:
        """Step-by-step working, one step per line; falls back to the explanation."""
        return "\n".join(self.steps) if self.steps else self.explanation


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _rand_nonzero(rng: random.Random, low: int, high: int) -> int:
    """Random int in [low, high], never zero (used for coefficients)."""
    n = 0
    while n == 0:
        n = rng.randint(low, high)
    return n


def _paren(n: int) -> str:
    """Operand after an operator: negatives are wrapped, so '5 + (-3)', never '5 + -3'."""
    return f"({n})" if n < 0 else str(n)


def _x_term(coef: int, first: bool) -> str:
    """'3x', '-x' for a leading term; '+ 5x', '- x' for a later one."""
    mag = "x" if abs(coef) == 1 else f"{abs(coef)}x"
    if first:
        return f"-{mag}" if coef < 0 else mag
    return f"- {mag}" if coef < 0 else f"+ {mag}"


def _const(val: int) -> str:
    """Trailing constant as '+ 5' / '- 5' ('' for zero)."""
    if val == 0:
        return ""
    return f"+ {val}" if val > 0 else f"- {abs(val)}"


def _lhs(coef: int, const: int) -> str:
    """Render coef*x + const as text, e.g. '3x - 1'."""
    return " ".join(p for p in (_x_term(coef, True), _const(const)) if p)


# ---------------------------------------------------------------------------
# generators
# ---------------------------------------------------------------------------


def generate_arithmetic(
    difficulty: Union[str, Difficulty] = Difficulty.EASY, seed: Optional[int] = None
) -> Problem:
    """Order-of-operations integer arithmetic (Foundations topic)."""
    diff = Difficulty.coerce(difficulty)
    rng = random.Random(seed)  # local instance: never touches global random state
    low, high = _RANGES[diff]
    a = _rand_nonzero(rng, low, high)
    b = _rand_nonzero(rng, low, high)
    c = _rand_nonzero(rng, 1, 5)
    steps: Tuple[str, ...]

    if diff is Difficulty.EASY:
        prod = b * c
        prompt = f"{a} + {_paren(b)} × {c}"
        answer = a + prod
        steps = (
            f"Multiplication comes before addition: {_paren(b)} × {c} = {prod}",
            f"Now add: {a} + {_paren(prod)} = {answer}",
        )
        explanation = "Multiplication before addition (PEMDAS)."
    elif diff is Difficulty.MEDIUM:
        d = rng.randint(1, 3)
        inner = c - d
        prod = b * inner
        prompt = f"{a} - {_paren(b)} × ({c} - {d})"
        answer = a - prod
        steps = (
            f"Parentheses first: ({c} - {d}) = {inner}",
            f"Then multiply: {_paren(b)} × {_paren(inner)} = {prod}",
            f"Finally subtract: {a} - {_paren(prod)} = {answer}",
        )
        explanation = "Parentheses first, then multiplication, then subtraction."
    else:
        d = rng.randint(1, 3)
        exp = rng.choice([2, 3])
        inner = c - d
        powered = inner**exp
        prod = b * powered
        prompt = f"{a} + {_paren(b)} × ({c} - {d})^{exp}"
        answer = a + prod
        steps = (
            f"Parentheses first: ({c} - {d}) = {inner}",
            f"Then the exponent: {_paren(inner)}^{exp} = {powered}",
            f"Then multiply: {_paren(b)} × {_paren(powered)} = {prod}",
            f"Finally add: {a} + {_paren(prod)} = {answer}",
        )
        explanation = "Parentheses, then exponent, then multiplication, then addition."

    return Problem(prompt, Fraction(answer), "foundations", diff, explanation, steps)


def generate_linear_equation(
    difficulty: Union[str, Difficulty] = Difficulty.EASY,
    seed: Optional[int] = None,
    avoid_zero: bool = False,
) -> Problem:
    """A solvable equation ax + b = cx + d with an integer answer (Linear Equations topic).

    Built backwards: x is chosen first, then d is solved for, so the answer is known by
    construction. Easy uses positive coefficients; medium and hard allow negatives.
    ``avoid_zero=True`` guarantees x != 0.
    """
    diff = Difficulty.coerce(difficulty)
    rng = random.Random(seed)
    low, high = _RANGES[diff]
    coef_low, coef_high = (1, 9) if diff is Difficulty.EASY else (-high, high)

    x = rng.randint(low, high)
    while avoid_zero and x == 0:
        x = rng.randint(low, high)
    a = _rand_nonzero(rng, coef_low, coef_high)
    c = _rand_nonzero(rng, coef_low, coef_high)
    while c == a:  # a == c would leave 0x = something: no / infinitely many solutions
        c = _rand_nonzero(rng, coef_low, coef_high)
    b = rng.randint(low, high)
    d = (a - c) * x + b  # solved from a*x + b = c*x + d

    prompt = f"{_lhs(a, b)} = {_lhs(c, d)}"
    k = a - c  # coefficient of x once the x terms are on the left
    verb = "subtract" if c > 0 else "add"
    steps = [
        f"Start with: {prompt}",
        f"Move the x terms to the left ({verb} {_x_term(abs(c), True)} on both sides): "
        f"{_lhs(k, b)} = {d}",
    ]
    if b != 0:
        verb = "subtract" if b > 0 else "add"
        steps.append(
            f"Move the constant to the right ({verb} {abs(b)} on both sides): "
            f"{_x_term(k, True)} = {d - b}"
        )
    if k != 1:
        steps.append(f"Divide both sides by {k}: x = {x}")
    explanation = (
        "Collect x terms on one side and constants on the other, "
        f"then divide by the coefficient of x to get x = {x}."
    )
    return Problem(prompt, Fraction(x), "linear-equations", diff, explanation, tuple(steps))


TOPIC_GENERATORS: Dict[str, Callable[..., Problem]] = {
    "foundations": generate_arithmetic,
    "linear-equations": generate_linear_equation,
}


def generate(
    topic: str,
    difficulty: Union[str, Difficulty] = Difficulty.EASY,
    seed: Optional[int] = None,
) -> Problem:
    """Generate a problem for a registered topic. Raises ValueError for unknown topics."""
    if topic not in TOPIC_GENERATORS:
        raise ValueError(f"Unknown topic {topic!r}. Available: {', '.join(TOPIC_GENERATORS)}")
    return TOPIC_GENERATORS[topic](difficulty=difficulty, seed=seed)
