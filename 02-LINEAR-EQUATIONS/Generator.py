"""
Algebra problem generator and solver.

Generates randomized practice problems for topics in this repo (starting with
Foundations arithmetic and Linear Equations) and can solve/check answers for them.

Usage as a library:
    from algebra_tools.generator import generate_linear_equation, generate_arithmetic

    problem = generate_linear_equation(difficulty="medium")
    print(problem.prompt)      # "3x + 7 = 22"
    print(problem.answer)      # 5.0
    print(problem.check(5))    # True

Usage as a CLI: see tools/cli.py
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction
from typing import Optional


@dataclass
class Problem:
    """A single generated problem: the text shown to the learner, and the answer."""
    prompt: str
    answer: Fraction
    topic: str
    difficulty: str
    explanation: str = ""

    def check(self, user_answer) -> bool:
        """Check a user-supplied answer (int, float, str, or Fraction) against the solution."""
        try:
            if isinstance(user_answer, str):
                user_answer = Fraction(user_answer)
            else:
                user_answer = Fraction(user_answer).limit_denominator(10_000)
        except (ValueError, ZeroDivisionError):
            return False
        return user_answer == self.answer

    def answer_display(self) -> str:
        """Human-friendly rendering of the answer (whole number if possible, else fraction)."""
        if self.answer.denominator == 1:
            return str(self.answer.numerator)
        return f"{self.answer.numerator}/{self.answer.denominator}"


_DIFFICULTY_RANGES = {
    "easy": (1, 10),
    "medium": (-15, 15),
    "hard": (-25, 25),
}


def _rand_nonzero(low: int, high: int) -> int:
    """Random int in [low, high], excluding zero (used for coefficients)."""
    n = 0
    while n == 0:
        n = random.randint(low, high)
    return n


def generate_arithmetic(difficulty: str = "easy", seed: Optional[int] = None) -> Problem:
    """Generate an order-of-operations / integer arithmetic problem (Foundations topic)."""
    if seed is not None:
        random.seed(seed)
    if difficulty not in _DIFFICULTY_RANGES:
        raise ValueError(f"difficulty must be one of {list(_DIFFICULTY_RANGES)}")

    low, high = _DIFFICULTY_RANGES[difficulty]
    a = _rand_nonzero(low, high)
    b = _rand_nonzero(low, high)
    c = _rand_nonzero(1, 5)  # small exponent-safe operand

    if difficulty == "easy":
        prompt = f"{a} + {b} * {c}"
        answer = Fraction(a) + Fraction(b) * Fraction(c)
        explanation = "Multiplication before addition (PEMDAS)."
    elif difficulty == "medium":
        prompt = f"{a} - {b} * ({c} - {random.randint(1, 3)})"
        # rebuild deterministically to keep prompt/answer in sync
        d = random.randint(1, 3)
        prompt = f"{a} - {b} * ({c} - {d})"
        answer = Fraction(a) - Fraction(b) * (Fraction(c) - Fraction(d))
        explanation = "Parentheses first, then multiplication, then subtraction."
    else:  # hard
        exp = random.choice([2, 3])
        prompt = f"{a} + {b} * ({c} - {random.randint(1, 3)}) ** {exp}"
        d = random.randint(1, 3)
        prompt = f"{a} + {b} * ({c} - {d}) ** {exp}"
        answer = Fraction(a) + Fraction(b) * (Fraction(c) - Fraction(d)) ** exp
        explanation = "Parentheses, then exponent, then multiplication, then addition."

    display_prompt = prompt.replace("**", "^").replace("*", "×")
    return Problem(display_prompt, answer, topic="foundations", difficulty=difficulty, explanation=explanation)


def generate_linear_equation(difficulty: str = "easy", seed: Optional[int] = None) -> Problem:
    """Generate a solvable linear equation of the form ax + b = cx + d (Linear Equations topic)."""
    if seed is not None:
        random.seed(seed)
    if difficulty not in _DIFFICULTY_RANGES:
        raise ValueError(f"difficulty must be one of {list(_DIFFICULTY_RANGES)}")

    low, high = _DIFFICULTY_RANGES[difficulty]

    # Pick the answer FIRST, then build an equation that produces it.
    # This guarantees every generated problem has a clean, checkable solution.
    x_value = Fraction(random.randint(low, high))

    a = _rand_nonzero(1, high if difficulty != "easy" else 9)
    c = _rand_nonzero(1, high if difficulty != "easy" else 9)
    while c == a:  # avoid accidental "infinite solutions" case unless requested
        c = _rand_nonzero(1, high if difficulty != "easy" else 9)
    b = random.randint(low, high)

    # a*x + b = c*x + d  =>  solve for d given x_value
    d = a * x_value + b - c * x_value

    def fmt_term(coef: int, is_first: bool = False) -> str:
        if coef == 1:
            return "x" if is_first else "+ x"
        if coef == -1:
            return "-x" if is_first else "- x"
        if is_first:
            return f"{coef}x"
        return f"+ {coef}x" if coef > 0 else f"- {abs(coef)}x"

    def fmt_const(val: Fraction, is_first: bool) -> str:
        if val == 0:
            return ""
        if is_first:
            return str(val)
        return f"+ {val}" if val > 0 else f"- {abs(val)}"

    left = fmt_term(a, is_first=True)
    left_const = fmt_const(Fraction(b), is_first=False)
    right = fmt_term(c, is_first=True)  # first term after "=" never needs a leading "+"
    right_const = fmt_const(d, is_first=False)

    prompt = f"{left} {left_const} = {right} {right_const}".replace("  ", " ").strip()
    explanation = (
        f"Collect x terms on one side and constants on the other, "
        f"then divide by the coefficient of x to get x = {x_value}."
    )
    return Problem(prompt, x_value, topic="linear-equations", difficulty=difficulty, explanation=explanation)


TOPIC_GENERATORS = {
    "foundations": generate_arithmetic,
    "linear-equations": generate_linear_equation,
}


def generate(topic: str, difficulty: str = "easy", seed: Optional[int] = None) -> Problem:
    """Generate a problem for any registered topic. Raises ValueError for unknown topics."""
    if topic not in TOPIC_GENERATORS:
        raise ValueError(f"Unknown topic '{topic}'. Available: {list(TOPIC_GENERATORS)}")
    return TOPIC_GENERATORS[topic](difficulty=difficulty, seed=seed)
