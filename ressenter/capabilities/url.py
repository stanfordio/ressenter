from ..util import (
    parse_date,
    pull_url_id,
    pull_comments_page,
)
from ..output import emit


def fetch(url=None, sort="latest", after_id="0", after_time="Jan 1, 2000", max=None):
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
            if comment["time"] is not None and comment["time"] < after_time:
                return

            comment["url"] = url

            emit(comment)
            total_emitted += 1

            if max is not None:
                if total_emitted >= max:
                    return

        page += 1
