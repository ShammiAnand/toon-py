import json
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from .encoder import encode
from .types import EncodeOptions

console = Console()


def main_command(
    input_source: Optional[str] = typer.Argument(
        None, help="JSON file path, JSON string, or read from stdin if not provided"
    ),
    indent: int = typer.Option(2, "--indent", "-i", help="Number of spaces per indentation level"),
    delimiter: str = typer.Option(
        "comma",
        "--delimiter",
        "-d",
        help="Delimiter for arrays: comma, tab, or pipe",
    ),
    length_marker: bool = typer.Option(
        False, "--length-marker", "-l", help="Add '#' prefix to array lengths"
    ),
    output: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output file path (default: stdout)"
    ),
):
    try:
        if input_source is None:
            if sys.stdin.isatty():
                console.print("[red]Error: No input provided. Use a file, JSON string, or pipe data via stdin.[/red]")
                raise typer.Exit(1)
            json_data = sys.stdin.read()
        else:
            input_path = Path(input_source)
            if input_path.exists() and input_path.is_file():
                json_data = input_path.read_text()
            else:
                json_data = input_source

        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            console.print(f"[red]Error: Invalid JSON - {e}[/red]")
            raise typer.Exit(1)

        delimiter_map = {
            "comma": ",",
            "tab": "\t",
            "pipe": "|",
            ",": ",",
            "\t": "\t",
            "|": "|",
        }

        if delimiter not in delimiter_map:
            console.print(f"[red]Error: Invalid delimiter '{delimiter}'. Use: comma, tab, or pipe[/red]")
            raise typer.Exit(1)

        options = EncodeOptions(
            indent=indent,
            delimiter=delimiter_map[delimiter],
            length_marker="#" if length_marker else False,
        )

        result = encode(data, options)

        if output:
            output_path = Path(output)
            output_path.write_text(result)
            console.print(f"[green]TOON output written to {output}[/green]")
        else:
            print(result)

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


def app():
    typer.run(main_command)


if __name__ == "__main__":
    app()
