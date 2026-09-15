from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer

from .normalization import is_doi_syntax_valid, normalize_doi
from .parsing import parse_manuscript
from .validation import validate_output

app = typer.Typer(help="Deterministic utilities for Medical Journal Matcher.")


@app.command("parse")
def parse_command(
    manuscript: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
) -> None:
    """Parse a manuscript locally and report metadata without echoing its text."""
    text = parse_manuscript(manuscript)
    typer.echo(json.dumps({"path": manuscript.name, "characters": len(text)}, ensure_ascii=False))


@app.command("validate-doi")
def validate_doi_command(dois: list[str]) -> None:
    """Validate DOI syntax; this does not claim online resolvability."""
    results = [
        {
            "input": value,
            "normalized": normalize_doi(value),
            "syntax_valid": is_doi_syntax_valid(value),
        }
        for value in dois
    ]
    typer.echo(json.dumps(results, ensure_ascii=False, indent=2))


@app.command("validate-output")
def validate_output_command(
    result: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    schema: Annotated[Path, typer.Option()] = Path("references/output-schema.json"),
) -> None:
    """Validate a machine-readable result against schema version 1.0.0."""
    instance = json.loads(result.read_text(encoding="utf-8"))
    errors = validate_output(instance, schema)
    if errors:
        for error in errors:
            typer.echo(error, err=True)
        raise typer.Exit(code=1)
    typer.echo("valid")
