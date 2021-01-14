import json
import unicodecsv as csv
from datetime import datetime

global _format


def set_format(format):
    global _format

    _format = format


def emit(obj: dict):
    # Serialize keys
    for key in obj.keys():
        if type(obj[key]) == datetime:
            obj[key] = datetime.isoformat(obj[key])

    print(json.dumps(obj))
