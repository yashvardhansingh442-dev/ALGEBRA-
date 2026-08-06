"""
Tests for algebra_tools.generator.

Run with:  pytest tests/
"""
import os
import random as random_module
import sys
from dataclasses import FrozenInstanceError
from fractions import Fraction

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

from algebra_tools.generator import (  # noqa: E402
    Difficulty,
    Problem,
    generate,
    generate_arithmetic,
    generate_linear_equation,
)


class TestProblem:
    def test_check_accepts_matching_int(self):
        p = Problem(prompt="x = ?", answer=Fraction(5), topic="test", difficulty=Difficulty.EASY)
        assert p.check(5) is True

    def test_check_rejects_wrong_answer(self):
        p = Problem(prompt="x = ?", answer=Fraction(5), topic="test", difficulty=Difficulty.EASY)
        assert p.check(6) is False

    def test_check_accepts_string_input(self):
        p = Problem(prompt="x = ?", answer=Fraction(3, 4), topic="test", difficulty=Difficulty.EASY)
        assert p.check("3/4") is True

    def test_check_accepts_spaced_fraction_string(self):
        """Regression test: '1 / 2' should parse the same as '1/2'."""
        p = Problem(prompt="x = ?", answer=Fraction(1, 2), topic="test", difficulty=Difficulty.EASY)
        assert p.check("1 / 2") is True
        assert p.check(" 1/2 ") is True

    def test_check_handles_garbage_input_gracefully(self):
        p = Problem(prompt="x = ?", answer=Fraction(5), topic="test", difficulty=Difficulty.EASY)
        assert p.check("banana") is False
        assert p.check("1/0") is False

    def test_answer_display_whole_number(self):
        p = Problem(prompt="x = ?", answer=Fraction(7), topic="test", difficulty=Difficulty.EASY)
        assert p.answer_display() == "7"

    def test_answer_display_fraction(self):
        p = Problem(prompt="x = ?", answer=Fraction(12, 5), topic="test", difficulty=Difficulty.EASY)
        assert p.answer_display() == "12/5"

    def test_str_returns_prompt(self):
        p = Problem(prompt="3x + 4 = 10", answer=Fraction(2), topic="test", difficulty=Difficulty.EASY)
        assert str(p) == "3x + 4 = 10"

    def test_problem_is_immutable(self):
        p = Problem(prompt="x = ?", answer=Fraction(5), topic="test", difficulty=Difficulty.EASY)
        with pytest.raises(FrozenInstanceError):
            p.answer = Fraction(999)

    def test_solution_text_falls_back_to_explanation_when_no_steps(self):
        p = Problem(prompt="x = ?", answer=Fraction(5), topic="test", difficulty=Difficulty.EASY,
                    explanation="some explanation")
        assert p.solution_text() == "some explanation"

    def test_solution_text_uses_steps_when_present(self):
        p = Problem(prompt="x = ?", answer=Fraction(5), topic="test", difficulty=Difficulty.EASY,
                    steps=["step 1", "step 2"])
        assert p.solution_text() == "step 1\nstep 2"


class TestDifficultyValidation:
    def test_invalid_difficulty_string_raises_with_helpful_message(self):
        with pytest.raises(ValueError, match="easy, medium, hard"):
            generate_arithmetic(difficulty="impossible")

    def test_accepts_difficulty_enum_directly(self):
        p = generate_arithmetic(difficulty=Difficulty.MEDIUM, seed=1)
        assert p.difficulty is Difficulty.MEDIUM


class TestGenerateArithmetic:
    @pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
    def test_generates_a_valid_problem(self, difficulty):
        problem = generate_arithmetic(difficulty=difficulty, seed=42)
        assert isinstance(problem, Problem)
        assert problem.topic == "foundations"
        assert problem.difficulty == difficulty
        assert problem.prompt
        assert len(problem.steps) >= 2  # real step-by-step, not just one line

    def test_same_seed_is_reproducible(self):
        p1 = generate_arithmetic(difficulty="medium", seed=123)
        p2 = generate_arithmetic(difficulty="medium", seed=123)
        assert p1.prompt == p2.prompt
        assert p1.answer == p2.answer

    def test_does_not_mutate_global_random_state(self):
        """Regression test: generator must use a local Random instance,
        not random.seed()/random.randint() on the shared module."""
        random_module.seed(42)
        expected_next = random_module.random()

        random_module.seed(42)
        generate_arithmetic(difficulty="hard", seed=999)  # should not touch global state
        actual_next = random_module.random()

        assert actual_next == expected_next


class TestGenerateLinearEquation:
    @pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
    @pytest.mark.parametrize("seed", range(30))
    def test_generated_equation_is_solvable_and_correct(self, difficulty, seed):
        """The generator picks x first, then builds the equation — verify the
        round-trip actually holds for many random seeds, across all difficulties."""
        problem = generate_linear_equation(difficulty=difficulty, seed=seed)
        assert problem.check(problem.answer) is True

    def test_wrong_answer_is_rejected(self):
        problem = generate_linear_equation(difficulty="easy", seed=1)
        wrong = problem.answer + 1
        assert problem.check(wrong) is False

    def test_negative_coefficients_occur_on_medium_and_hard(self):
        """Regression test: coefficients used to only be drawn from a positive
        range even when the difficulty range was negative-inclusive."""
        for difficulty in ["medium", "hard"]:
            saw_negative = any(
                generate_linear_equation(difficulty=difficulty, seed=s).prompt.startswith("-")
                for s in range(100)
            )
            assert saw_negative, f"expected at least one negative leading coefficient at {difficulty}"

    def test_no_stray_plus_sign_after_equals(self):
        """Regression test for the '5x + 8 = + 8x - 1' formatting bug."""
        for difficulty in ["easy", "medium", "hard"]:
            for seed in range(100):
                p = generate_linear_equation(difficulty=difficulty, seed=seed)
                assert "= +" not in p.prompt
                assert "  " not in p.prompt

    def test_avoid_zero_prevents_zero_answers(self):
        for seed in range(200):
            p = generate_linear_equation(difficulty="medium", seed=seed, avoid_zero=True)
            assert p.answer != 0

    def test_does_not_mutate_global_random_state(self):
        random_module.seed(7)
        expected_next = random_module.random()

        random_module.seed(7)
        generate_linear_equation(difficulty="hard", seed=555)
        actual_next = random_module.random()

        assert actual_next == expected_next

    def test_solution_steps_contain_final_answer(self):
        p = generate_linear_equation(difficulty="medium", seed=3)
        assert any(str(p.answer) in step or p.answer_display() in step for step in p.steps)

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
