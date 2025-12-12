import re
from dateutil import parser

def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

def parse_date(value: str):
    try:
        return parser.parse(value, dayfirst=True, fuzzy=True).date().isoformat()
    except Exception:
        return None