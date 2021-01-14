import click
from ..util import (
    parse_date,
    pull_url_id,
    pull_comments_page,
    add_click_options,
    COMMENT_PAGE_OPTIONS,
)
from ..output import emit


@click.command(
    "url",
    help="Pull comments for a particular URL. Note that several comment metadata items (such as upvotes, downvotes, and comments) are not available when pulling comments from a URL.",
)
@click.argument("url")
@add_click_options(COMMENT_PAGE_OPTIONS)
def command(url, sort, after_id, after_time, max):
    # Note: a lot of metadata is unavailable for comments from URLs

    after_id = int(after_id.strip(), 16)
    after_time = parse_date(after_time)
    url_id = pull_url_id(url)

    if url_id is None:
        return

    page = 1
    total_emitted = 0
    while (
        len(
            page_comments := pull_comments_page(
                s=sort, p=page, v="begin", cpp=350, uid=url_id
            )
        )
        > 0
    ):
        for comment in page_comments:
            if int(comment["id"], 16) < after_id:
                return
            if comment["time"] < after_time:
                return

            comment["url"] = url

            emit(comment)
            total_emitted += 1

            if max is not None:
                if total_emitted >= max:
                    return

        page += 1
