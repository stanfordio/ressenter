# Ressenter

Ressenter is a command line tool to pull content from Dissenter.com, a browser-based social network operated by Gab.com. (We will not reward either of these domains with hyperlinks.)

This tool does not require any authentication with Dissenter; all the data it pulls is available publicly.

Currently, this tool can:

* Reliably pull all comments made on Dissenter within the last seven days
* Pull the current 'top' comments
* Pull the current 'controversial' comments
* Pull the current trending URLs
* Pull all the comments for a particular URL
* Pull all the comments made by a particular user

## Robustness

This tool was made by reverse engineering Dissenter's API. (To be fair, it wasn't that hard.) Because we have no insight into Dissenter's internals, there's no guarantee that this tool provides an exhaustive or reliable archive of Dissenter content.

For example, we don't know whether comments become inaccessible after some period of time, or whether there is a limit on how many comments we can pull from any particular user.

## Usage

```
Usage: ressenter [OPTIONS] COMMAND [ARGS]...

Options:
  --format [jsonl|csv]  output format
  --help                Show this message and exit.

Commands:
  comments  Pull all the most recent comments
  trending  Pull the current trending URLs
  url       Pull comments for a particular URL.
  user      Pull all the comments of a particular user
```

Ressenter can output data to `jsonl` and `csv` (the default is `jsonl`). Just pass the `--format` option before the subcommand (e.g., `ressenter --format=csv comments`). All data is currently written to `stdout`; to save output to a file, use pipes (e.g., `ressenter comments > comments.jsonl`).

### `comments`

```
Usage: ressenter comments [OPTIONS]

  Pull all the most recent comments

Options:
  --sort [latest|controversial|top]
                                  comment sort order
  --after-id TEXT                 pull no earlier than this comment ID
  --after-time TEXT               pull no comments posted earlier than this
                                  time

  --max INTEGER                   maximum number of comments to pull
  --help                          Show this message and exit.
```

### `trending`

```
Usage: ressenter trending [OPTIONS]

  Pull the current trending URLs

Options:
  --help  Show this message and exit.
```

### `url`

```
Usage: ressenter url [OPTIONS] URL

  Pull comments for a particular URL. Note that several comment metadata
  items (such as upvotes, downvotes, and comments) are not available when
  pulling comments from a URL.

Options:
  --sort [latest|controversial|top]
                                  comment sort order
  --after-id TEXT                 pull no earlier than this comment ID
  --after-time TEXT               pull no comments posted earlier than this
                                  time

  --max INTEGER                   maximum number of comments to pull
  --help                          Show this message and exit.
```

### `user`

```
Usage: ressenter user [OPTIONS] USER

  Pull all the comments of a particular user, identified by their UID

Options:
  --sort [latest|controversial|top]
                                  comment sort order
  --after-id TEXT                 pull no earlier than this comment ID
  --after-time TEXT               pull no comments posted earlier than this
                                  time

  --max INTEGER                   maximum number of comments to pull
  --help                          Show this message and exit.
```

## Playbook

Here are some common use cases:

#### Pull all the most recent comments

```bash
ressenter comments
```

#### Pull all the recent top comments

```bash
ressenter comments --sort=top
```

#### Pull all the recent controversial comments

```bash
ressenter comments --sort=controversial
```

#### Pull all comments made in the past hour

```bash
ressenter comments --after-time "one hour ago"
```

#### Pull all the current trending URLs

```bash
ressenter trending
```

#### Pull all of the comments for a particular URL

```bash
ressenter url https://www.facebook.com
```

## Development

To run Ressenter locally, perform the following steps:

1. Install dependencies with `pipenv install`
2. Activate the virtual environment with `pipenv shell`
3. Run the tool using `main.py` -- for example, `./main.py comments`

## Packaging and Publishing

TODO (when/if we release on PyPi).

## Troubleshooting

If you work at the Stanford Internet Observatory, ping Miles McCain on Slack or via email to get help with Ressenter. To report bugs or submit feature requests, please open an issue.

## Desired Features

There are a few features that this tool currently lacks, but that we'd like to add. We haven't yet found reliable ways to extract this data. (If you have, please let us know!)

* Find the most recent URLs commented on
* Iterate through all the URLs with comments
* Iterate through all comments, instead of just those made in the past seven days