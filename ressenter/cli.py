#!/usr/bin/env python3

import click
from . import output
from .util import (
    add_click_options,
    COMMENT_PAGE_OPTIONS,
)
from .output import emit
from .capabilities import comments, user, url, trending


@click.group()
@click.option(
    "--format",
    default="jsonl",
    help="output format",
    type=click.Choice(["jsonl", "csv"]),
)
def cli(format):
    output.set_format(format)


@click.command("comments", help="Pull all the most recent comments")
@add_click_options(COMMENT_PAGE_OPTIONS)
def comments_command(**kwargs):
    return comments.fetch(**kwargs)


@click.command("trending", help="Pull the current trending URLs")
def trending_command():
    return trending.fetch()


@click.command(
    "url",
    help="Pull comments for a particular URL. Note that several comment metadata items (such as upvotes, downvotes, and comments) are not available when pulling comments from a URL.",
)
@click.argument("url")
@add_click_options(COMMENT_PAGE_OPTIONS)
def url_command(**kwargs):
    return url.fetch(**kwargs)


@click.command(
    "user", help="Pull all the comments of a particular user, identified by their UID"
)
@click.argument("user")
@add_click_options(COMMENT_PAGE_OPTIONS)
def user_command(**kwargs):
    return user.fetch(**kwargs)


cli.add_command(comments_command)
cli.add_command(trending_command)
cli.add_command(url_command)
cli.add_command(user_command)
