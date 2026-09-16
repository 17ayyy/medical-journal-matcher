import json
from pathlib import Path

from typer.testing import CliRunner

from medical_journal_matcher.cli import app
from tests.factories import valid_output

runner = CliRunner()


def test_parse_command_reports_metadata_without_text(tmp_path: Path) -> None:
    manuscript = tmp_path / "private-manuscript.txt"
    manuscript.write_text("unpublished secret result", encoding="utf-8")

    result = runner.invoke(app, ["parse", str(manuscript)])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload == {"path": manuscript.name, "characters": 25}
    assert "unpublished secret result" not in result.stdout


def test_validate_doi_command_distinguishes_invalid_input() -> None:
    result = runner.invoke(
        app,
        ["validate-doi", "https://doi.org/10.1000/ABC.1", "not-a-doi"],
    )
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload[0]["normalized"] == "10.1000/abc.1"
    assert payload[0]["syntax_valid"] is True
    assert payload[1]["syntax_valid"] is False


def test_validate_output_command_accepts_valid_public_result(tmp_path: Path) -> None:
    output = tmp_path / "result.json"
    output.write_text(json.dumps(valid_output(), ensure_ascii=False), encoding="utf-8")
    result = runner.invoke(app, ["validate-output", str(output)])
    assert result.exit_code == 0
    assert result.stdout.strip() == "valid"
