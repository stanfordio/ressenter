from dateparser import parse as date_parse
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import urllib
import click
import collections

COMMENT_PAGE_OPTIONS = [
    click.option(
        "--sort",
        default="latest",
        help="comment sort order",
        type=click.Choice(["latest", "controversial", "top"]),
    ),
    click.option(
        "--after-id", default="0", help="pull no earlier than this comment ID", type=str
    ),
    click.option(
        "--after-time",
        default="Jan 1, 2000",
        help="pull no comments posted earlier than this time",
        type=str,
    ),
    click.option("--max", help="maximum number of comments to pull", type=int),
]


def flatten(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def parse_date(text: str) -> datetime:
    if text == "a few seconds ago":
        text = "now"

    return date_parse(text)


def add_click_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


def parse_int(text: str) -> int:
    text = text.replace(",", "")
    return int(text)


def try_get(func):
    try:
        return func()
    except:
        return None


def pull_url_id(url: str) -> str:
    resp = requests.get(
        f"https://dissenter.com/discussion/begin?"
        + urllib.parse.urlencode({"url": url})
    )
    soup = BeautifulSoup(resp.text, features="html.parser")
    return try_get(
        lambda: soup.find("div", {"data-commenturl-id": True}).get("data-commenturl-id")
    )


def pull_comments_page(**kwargs):
    resp = requests.get(
        f"https://dissenter.com/comment?" + urllib.parse.urlencode(kwargs)
    )
    soup = BeautifulSoup(resp.text, features="html.parser")

    comments = []
    for comment_elem in soup.find_all("div", class_="comment-container"):
        comments.append(
            {
                "id": try_get(lambda: comment_elem.get("data-comment-id").strip()),
                "author_id": try_get(
                    lambda: comment_elem.get("data-author-id").strip()
                ),
                "author_name": try_get(
                    lambda: comment_elem.find("span", class_="profile-name").text
                ),
                "author_url": try_get(
                    lambda: comment_elem.find("a", {"target": "dissenter-profile"}).get(
                        "href"
                    )
                ),
                "url": try_get(
                    lambda: comment_elem.find("a", {"target": "dissenter-item"}).get(
                        "href"
                    )
                ),
                "url_upvotes": try_get(
                    lambda: parse_int(
                        comment_elem.find("span", class_="stat-upvotes").text
                    )
                ),
                "url_downvotes": try_get(
                    lambda: parse_int(
                        comment_elem.find("span", class_="stat-downvotes").text
                    )
                ),
                "url_comments": try_get(
                    lambda: parse_int(
                        comment_elem.find(
                            "div", class_="row no-gutters align-items-center ml-auto"
                        ).text.split(" ")[0]
                    )
                ),
                "text": try_get(
                    lambda: comment_elem.find("div", class_="comment-body").text
                ),
                "replies": try_get(
                    lambda: parse_int(
                        comment_elem.find("span", class_="stat-replies").text
                    )
                ),
                "time": try_get(
                    lambda: parse_date(
                        comment_elem.find("a", {"title": "View comment"})
                        .find("span")
                        .text
                    )
                ),
            }
        )

    return comments
