"""
Tests for algebra_tools.generator.

Run with:  pytest tests/
"""
import os
import sys
from fractions import Fraction

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from algebra_tools.generator import (  # noqa: E402
    Problem,
    generate,
    generate_arithmetic,
    generate_linear_equation,
)


class TestProblem:
    def test_check_accepts_matching_int(self):
        p = Problem(prompt="x = ?", answer=Fraction(5), topic="test", difficulty="easy")
        assert p.check(5) is True

    def test_check_rejects_wrong_answer(self):
        p = Problem(prompt="x = ?", answer=Fraction(5), topic="test", difficulty="easy")
        assert p.check(6) is False

    def test_check_accepts_string_input(self):
        p = Problem(prompt="x = ?", answer=Fraction(3, 4), topic="test", difficulty="easy")
        assert p.check("3/4") is True

    def test_check_handles_garbage_input_gracefully(self):
        p = Problem(prompt="x = ?", answer=Fraction(5), topic="test", difficulty="easy")
        assert p.check("banana") is False
        assert p.check("1/0") is False

    def test_answer_display_whole_number(self):
        p = Problem(prompt="x = ?", answer=Fraction(7), topic="test", difficulty="easy")
        assert p.answer_display() == "7"

    def test_answer_display_fraction(self):
        p = Problem(prompt="x = ?", answer=Fraction(12, 5), topic="test", difficulty="easy")
        assert p.answer_display() == "12/5"


class TestGenerateArithmetic:
    @pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
    def test_generates_a_valid_problem(self, difficulty):
        problem = generate_arithmetic(difficulty=difficulty, seed=42)
        assert isinstance(problem, Problem)
        assert problem.topic == "foundations"
        assert problem.difficulty == difficulty
        assert problem.prompt  # non-empty

    def test_same_seed_is_reproducible(self):
        p1 = generate_arithmetic(difficulty="medium", seed=123)
        p2 = generate_arithmetic(difficulty="medium", seed=123)
        assert p1.prompt == p2.prompt
        assert p1.answer == p2.answer

    def test_invalid_difficulty_raises(self):
        with pytest.raises(ValueError):
            generate_arithmetic(difficulty="impossible")


class TestGenerateLinearEquation:
    @pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
    @pytest.mark.parametrize("seed", range(20))
    def test_generated_equation_is_solvable_and_correct(self, difficulty, seed):
        """The generator picks x first, then builds the equation — verify that
        round-trip actually holds for many random seeds, across all difficulties."""
        problem = generate_linear_equation(difficulty=difficulty, seed=seed)
        assert problem.check(problem.answer) is True

    def test_wrong_answer_is_rejected(self):
        problem = generate_linear_equation(difficulty="easy", seed=1)
        wrong = problem.answer + 1
        assert problem.check(wrong) is False

    def test_invalid_difficulty_raises(self):
        with pytest.raises(ValueError):
            generate_linear_equation(difficulty="nightmare")


class TestGenerateDispatcher:
    def test_generate_routes_to_correct_topic(self):
        problem = generate("linear-equations", difficulty="easy", seed=7)
        assert problem.topic == "linear-equations"

    def test_unknown_topic_raises(self):
        with pytest.raises(ValueError):
            generate("trigonometry", difficulty="easy")
