import typer

from medical_journal_matcher.cli import parse_command

if __name__ == "__main__":
    typer.run(parse_command)
