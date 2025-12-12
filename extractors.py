import re
from text_utils import parse_date

AADHAAR_RE = re.compile(r"\b(\d{4}\s?\d{4}\s?\d{4})\b")
PAN_RE = re.compile(r"\b([A-Z]{5}\d{4}[A-Z])\b", re.IGNORECASE)
AMOUNT_RE = re.compile(r"\b(?:Rs|INR)\s*[:\-]?\s*([0-9,]+(?:\.[0-9]{1,2})?)\b", re.IGNORECASE)
DATE_RE = re.compile(r"\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b")

def extract_aadhaar(text): return (AADHAAR_RE.search(text) or [None])[0]
def extract_pan(text): return (PAN_RE.search(text) or [None])[0]
def extract_amount(text): return (AMOUNT_RE.search(text) or [None])[1]
def extract_dates(text): return [parse_date(m.group(1)) for m in DATE_RE.finditer(text)]