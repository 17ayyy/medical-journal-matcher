import typer

from medical_journal_matcher.cli import validate_doi_command

if __name__ == "__main__":
    typer.run(validate_doi_command)
