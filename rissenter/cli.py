#!/usr/bin/env python3

import click
from .commands import comments, user, url, trending
from . import output

@click.group()
@click.option(
    "--format",
    default="jsonl",
    help="output format",
    type=click.Choice(["jsonl", "csv"]),
)
def cli(format):
    output.set_format(format)

cli.add_command(comments.command)
cli.add_command(user.command)
cli.add_command(url.command)
cli.add_command(trending.command)
