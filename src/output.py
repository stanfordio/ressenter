import json
import unicodecsv as csv
from datetime import datetime
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


def emit(obj: dict):
    global _csv_writer

    # Serialize keys
    for key in obj.keys():
        if type(obj[key]) == datetime:
            obj[key] = datetime.isoformat(obj[key])

    if _format == "jsonl":
        print(json.dumps(obj), file=_output)
    elif _format == "csv":
        if _csv_writer == None:
            _csv_writer = csv.DictWriter(_output, obj.keys())
            _csv_writer.writeheader()
        _csv_writer.writerow(obj)

def close():
    _output.close()
