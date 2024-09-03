import asyncio
import inspect
import logging
from typing import Any, Callable

import click
from mbpy.mpip import find_and_sort
from minspect.inspecting import inspect_library
from msearch.parse import mparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme
from msearch.search import search_github, search_huggingface, search_web
from msearch.browse import browse
custom_theme = Theme({"default": "on white"})
console = Console(theme=custom_theme)
logger = logging.getLogger(__name__)

def parse_and_run(query: str, func: Callable) -> Any:
    args, kwargs = mparse(query)
    for key, value in kwargs.items():
        value: str = str(value)
        if value.isnumeric():
            kwargs[key] = float(value)
        elif value.lower() in ['true', 'false']:
            kwargs[key] = value.lower() == 'true'
    try:
        return func(*args, **kwargs)
    except Exception as e:
        console.print(Panel(f"Error: {e}", title="Error", style="bold red"))
        console.print(f"Received args: {args} and kwargs: {kwargs}")
        console.print(Panel(f"Correct usage: {inspect.signature(func)}", title="Usage"))
        exit(1)

@click.command()
@click.argument('query', nargs=-1)
@click.option('--engine', '-e', default='web', help='Search engine to use: web, github, inspect, pypi, hf')
def cli(query, engine: str):
    """Search for info on the web, github, pypi, or inspect a library"""
    query = ' '.join(query)
    
    if engine == 'web':
        results = search_web(query)
        
        if not results:
            console.print(Panel("No results found.", title="Web Search Results"))
        else:
            table = Table(title="Web Search Results", show_header=True, header_style="bold magenta")
            table.add_column("Title", style="cyan", width=40, overflow="fold")
            table.add_column("URL", style="blue", width=40, overflow="fold")
            table.add_column("Snippet", style="green", width=40, overflow="fold")
            for result in results:
                table.add_row(
                    result.get('title', 'No title'),
                    result.get('url', 'No URL'),
                    result.get('snippet', 'No snippet')
                )
            console.print(Panel(table, expand=True))
            browse([r["url"] for r in results])
    elif engine == 'github':
        results = search_github(query)

        if not results:
            console.print(Panel("No results found.", title="GitHub Search"))
        else:
            table = Table(title="GitHub Search Results")
            table.add_column("Repository", style="cyan", no_wrap=True)
            table.add_column("URL", style="magenta")
            table.add_column("Description", style="green")
            table.add_column("Stars", justify="right", style="yellow")
            table.add_column("Forks", justify="right", style="yellow")
            for repo in results:
                table.add_row(repo['name'], repo['url'], repo['description'], str(repo['stars']), str(repo['forks']))
            console.print(Panel(table))
            browse([r["url"] for r in results])
    elif engine == 'inspect':
        if "depth" not in query:
            query += " depth=0"
        if "signatures" not in query:
            query += " signatures=True"
        if "docs" not in query:
            query += " docs=False"
        result = parse_and_run(query, inspect_library)
        console.print(Panel(f"Inspecting module: {query}", title="Module Inspection"))
        console.print(Panel(result.get('functions', 'No functions found'), title="Functions"))
        console.print(Panel(result.get('classes', 'No classes found'), title="Classes"))
        console.print(Panel(result.get('variables', 'No variables found'), title="Variables"))
    elif engine == "pypi":
        result = parse_and_run(query, find_and_sort)
        table = Table(title="PyPI Search Results")
        table.add_column("Package", style="cyan", no_wrap=True)
        table.add_column("Version", style="magenta")
        table.add_column("Description", style="green")
        for package in results:
            table.add_row(package['name'], package['version'], package['summary'])
        console.print(Panel(table))
    elif engine == "hf":
        result = parse_and_run(query, search_huggingface)
        if not results:
            console.print(Panel("No results found.", title="HuggingFace Search"))
        else:
            table = Table(title="HuggingFace Search Results", show_header=True, header_style="bold magenta")
            table.add_column("Type", style="cyan", no_wrap=True)
            table.add_column("Name", style="magenta")
            table.add_column("URL", style="blue")
            table.add_column("Downloads", justify="right", style="green")
            table.add_column("Likes", justify="right", style="yellow")
            for item in results:
                table.add_row(item['type'].capitalize(), item['name'], item['url'], str(item['downloads']), str(item['likes']))
            console.print(Panel(table, expand=False))
            console.print(Panel(f"Total results: {len(results)}", title="Summary", style="bold green"))
    else:
        console.print(f"Invalid search engine: {engine}")
        return 1

    return 0

if __name__ == "__main__":
    exit(cli())
