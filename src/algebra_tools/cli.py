#!/usr/bin/env python3
"""
CLI practice tool for ALGEBRA-.

Examples:
    python -m algebra_tools --topic foundations --difficulty easy --count 5
    python -m algebra_tools --topic linear-equations --difficulty hard --count 10
"""
from __future__ import annotations

import argparse
import sys

from algebra_tools.generator import TOPIC_GENERATORS, Difficulty, generate


def run_quiz(topic: str, difficulty: str, count: int) -> None:
    correct = 0
    attempted = 0
    for i in range(1, count + 1):
        problem = generate(topic, difficulty)
        print(f"\nQ{i}. Solve: {problem.prompt}")
        try:
            raw = input("Your answer (or 'q' to quit): ").strip()
        except EOFError:
            break
        if raw.lower() == "q":
            break
        attempted += 1
        if problem.check(raw):
            print("✅ Correct!")
            correct += 1
        else:
            print(f"❌ Not quite. Correct answer: {problem.answer_display()}")
            print("   Working:")
            for line in problem.solution_text().splitlines():
                print(f"     {line}")

    print(f"\nScore: {correct}/{attempted}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Practice algebra problems from the command line.")
    parser.add_argument("--topic", choices=list(TOPIC_GENERATORS), default="foundations")
    parser.add_argument("--difficulty", choices=[d.value for d in Difficulty], default="easy")
    parser.add_argument("--count", type=int, default=5, help="Number of problems to generate")
    args = parser.parse_args()

    if args.count < 1:
        print("--count must be at least 1", file=sys.stderr)
        sys.exit(1)

    run_quiz(args.topic, args.difficulty, args.count)


if __name__ == "__main__":
    main()
