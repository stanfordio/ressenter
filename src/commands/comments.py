from datetime import date
import click
import requests
from bs4 import BeautifulSoup
from ..util import parse_date
import re
from ..output import emit


@click.command("comments")
@click.option('--sort', default="latest", help="comment sort order", type=click.Choice(['latest', 'controversial', 'top']))
@click.option('--after-id', default="0", help="pull no earlier than this comment ID", type=str)
@click.option('--after-time', default="Jan 1, 2000", help="pull no comments posted earlier than this time", type=str)
@click.option('--max', help="maximum number of comments to pull", type=int)
def command(sort, after_id, after_time, max):
    after_id = int(after_id.strip(), 16)
    after_time = parse_date(after_time)

    page = 1
    total_emitted = 0
    while len(page_comments := pull_page(sort, page)) > 0:
        for comment in page_comments:
            if int(comment["id"], 16) < after_id:
                return
            if comment["time"] < after_time:
                return

            emit(comment)
            total_emitted += 1

            if max is not None:
                if total_emitted >= max:
                    return
        
        page += 1


def pull_page(sort: str, page: int):
    resp = requests.get(
        f"https://dissenter.com/comment?v=discussion&s={sort}&p={page}&cpp=350")
    soup = BeautifulSoup(resp.text, features="html.parser")

    comments = []
    for comment_elem in soup.find_all("div", class_="comment-container"):
        comments.append({
            "id": comment_elem.get("data-comment-id").strip(),
            "author_id": comment_elem.get("data-author-id").strip(),
            "author_name": comment_elem.find("span", class_="profile-name").text,
            "author_url": comment_elem.find("a", {"target": "dissenter-profile"}).get("href"),
            "url": comment_elem.find("a", {"target": "dissenter-item"}).get("href"),
            "url_upvotes": comment_elem.find("span", class_="stat-upvotes").text,
            "url_downvotes": comment_elem.find("span", class_="stat-downvotes").text,
            "url_comments": comment_elem.find("a", {"href": re.compile(r"\/discussion\/begin\/.*")}),
            "text": comment_elem.find("div", class_="comment-body").text,
            "replies": comment_elem.find("span", class_="stat-replies").text,
            "time": parse_date(comment_elem.find("a", {"title": "View comment"}).find("span").text)
        })

    return comments
