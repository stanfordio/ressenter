from dateparser import parse as date_parse
from datetime import datetime

def parse_date(text: str) -> datetime:
    if text == "a few seconds ago":
        text = "now"
    
    return date_parse(text)

def parse_int(text: str) -> int:
    text = text.replace(",", "")
    return int(text)