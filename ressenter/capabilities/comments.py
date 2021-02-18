from ..util import (
    parse_date,
    pull_comments_page,
)
from ..output import emit


def fetch(sort="latest", after_id="0", after_time="Jan 1, 2000", max=None):
    after_id = int(after_id.strip(), 16)
    after_time = parse_date(after_time)

    page = 1
    total_emitted = 0
    while (
        len(
            page_comments := pull_comments_page(s=sort, p=page, v="discussion", cpp=350)
        )
        > 0
    ):
        for comment in page_comments:
            if int(comment["id"], 16) < after_id:
                return
            if comment["time"] is not None and comment["time"] < after_time:
                return

            emit(comment)
            total_emitted += 1

            if max is not None:
                if total_emitted >= max:
                    return

        page += 1
