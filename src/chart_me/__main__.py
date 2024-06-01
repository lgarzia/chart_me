# Third party imports
import typer


def chart_me_cli() -> None:
    do_stuff = "do stuff"
    typer.echo(do_stuff)


def main() -> None:
    """dispatch to type"""
    typer.run(chart_me_cli)
