"""Smoke tests: the package imports and the CLI's argument handling behaves.

Save as: tests/test_smoke.py

These deliberately avoid depending on engine behavior, so they pass today and
keep passing as modules are added. They also give pytest something to collect,
which CI and the pre-push hook require (pytest exits with an error on zero tests).
"""

from __future__ import annotations

import pytest

from algebra_tools import cli


def test_package_imports() -> None:
    import algebra_tools

    assert algebra_tools is not None


def test_help_exits_zero(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--help"])
    assert exc_info.value.code == 0
    assert "algebra" in capsys.readouterr().out


def test_version_prints_a_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["--version"])
    assert exc_info.value.code == 0
    assert capsys.readouterr().out.startswith("algebra ")


def test_topics_lists_every_known_topic(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["topics"]) == cli.EXIT_OK
    assert capsys.readouterr().out.split() == list(cli.TOPICS)


@pytest.mark.parametrize(
    "argv",
    [
        [],  # no command
        ["nonsense"],  # unknown command
        ["practice"],  # missing required --topic
        ["practice", "--topic", "not-a-topic"],
        ["practice", "--topic", "linear", "--count", "0"],  # must be positive
        ["eval", "x", "--set", "not-an-assignment"],
    ],
)
def test_bad_usage_exits_with_code_2(argv: list[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(argv)
    assert exc_info.value.code == 2


def test_every_topic_is_a_valid_practice_choice() -> None:
    parser = cli.build_parser()
    for topic in cli.TOPICS:
        args = parser.parse_args(["practice", "--topic", topic])
        assert args.topic == topic
