import json
import unicodecsv as csv
from datetime import datetime
from .util import flatten
import sys

_format = "jsonl"
_output = sys.stdout.buffer
_csv_writer = None


def set_format(format):
    global _format, _csv_writer

    _format = format
    _csv_writer = None


def set_output(output):
    global _output, _csv_writer

    _output = output
    _csv_writer = None


def disable_standard_output():
    result_listeners.remove(write_standard_output)


def write_standard_output(obj: dict):
    global _csv_writer

    if _format == "jsonl":
        _output.write((json.dumps(obj) + "\n").encode("utf-8"))
    elif _format == "csv":
        obj = flatten(obj)
        if _csv_writer == None:
            _csv_writer = csv.DictWriter(_output, obj.keys())
            _csv_writer.writeheader()
        _csv_writer.writerow(obj)


result_listeners = [write_standard_output]  # Functions to call on each result


def emit(obj: dict):
    global result_listeners

    # Serialize keys
    for key in obj.keys():
        if type(obj[key]) == datetime:
            obj[key] = datetime.isoformat(obj[key])

    for listener in result_listeners:
        listener(obj)


def close():
    _output.close()
