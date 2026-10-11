#!/usr/bin/env python3
"""
Command-line interface for phonetic translator.
"""
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Optional
import json

from translator import PhoneticTranslator

app = typer.Typer(help="Phonetic Translator CLI")
console = Console()


@app.command()
def translate(
    text: str = typer.Argument(..., help="Text to translate"),
    source: str = typer.Argument(..., help="Source language code"),
    target: str = typer.Argument(..., help="Target language code"),
    json_output: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Translate text between languages via phonetics."""
    translator = PhoneticTranslator()
    try:
        result = translator.translate(text, source, target)
        if json_output:
            console.print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            console.print(Panel.fit(
                f"[bold]{result['target']}[/bold]",
                title=f"[green]{source.upper()} → {target.upper()}[/green]",
                border_style="green",
            ))
            table = Table(show_header=False, box=None)
            table.add_row("Source:", result['source'])
            table.add_row("Source IPA:", f"[cyan]{result['src_ipa']}[/cyan]")
            table.add_row("Target IPA:", f"[cyan]{result['tgt_ipa']}[/cyan]")
            table.add_row("Confidence:", f"{result['confidence']:.1%}")
            console.print(table)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def transliterate(
    text: str = typer.Argument(..., help="Text to transliterate"),
    language: str = typer.Argument(..., help="Language code"),
):
    """Convert text to IPA phonetic transcription."""
    translator = PhoneticTranslator()
    try:
        ipa = translator.text_to_ipa(text, language)
        console.print(f"[bold]{text}[/bold] → [cyan]{ipa}[/cyan]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def languages():
    """List supported languages."""
    translator = PhoneticTranslator()
    langs = translator.supported_languages()
    table = Table(title="Supported Languages")
    table.add_column("Code", style="cyan")
    LANGUAGE_NAMES = {
        'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
        'it': 'Italian', 'pt': 'Portuguese', 'nl': 'Dutch', 'ru': 'Russian',
        'zh': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean', 'ar': 'Arabic',
        'hi': 'Hindi', 'tr': 'Turkish', 'pl': 'Polish', 'sv': 'Swedish',
        'vi': 'Vietnamese', 'th': 'Thai',
    }
    for code in langs:
        table.add_row(code, LANGUAGE_NAMES.get(code, code))
    console.print(table)


@app.command()
def batch(
    input_file: str = typer.Argument(..., help="Input file"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o"),
):
    """Batch translate from file."""
    translator = PhoneticTranslator()
    results = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                result = translator.translate(parts[0], parts[1], parts[2])
                results.append(result)
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            for r in results:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
        console.print(f"[green]✓[/green] Results written to {output_file}")
    else:
        for r in results:
            console.print(f"{r['source']} → {r['target']}")


if __name__ == "__main__":
    app()
