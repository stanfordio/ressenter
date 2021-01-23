import click
from ..util import (
    parse_date,
    pull_comments_page,
    add_click_options,
    COMMENT_PAGE_OPTIONS,
)
from ..output import emit


@click.command("user", help="Pull all the comments of a particular user, identified by their UID")
@click.argument("user")
@add_click_options(COMMENT_PAGE_OPTIONS)
def command(user, sort, after_id, after_time, max):
    after_id = int(after_id.strip(), 16)
    after_time = parse_date(after_time)

    page = 1
    total_emitted = 0
    while (
        len(
            page_comments := pull_comments_page(
                s=sort, p=page, v="profile", cpp=350, user=user
            )
        )
        > 0
    ):
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
