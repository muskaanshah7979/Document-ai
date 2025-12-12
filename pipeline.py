import os, mimetypes, pandas as pd
from ocr_utils import ocr_image
from pdf_utils import parse_pdf_text
from text_utils import clean_text
from extractors import extract_aadhaar, extract_pan, extract_amount, extract_dates

def detect_type(path: str):
    mime, _ = mimetypes.guess_type(path)
    if mime and mime.startswith("image"): return "image"
    if path.lower().endswith(".pdf"): return "pdf"
    return "unknown"

def extract_text(path: str):
    return ocr_image(path) if detect_type(path) == "image" else parse_pdf_text(path)

def process_document(path: str):
    raw = extract_text(path)
    cleaned = clean_text(raw)
    return {
        "file": os.path.basename(path),
        "aadhaar": extract_aadhaar(cleaned),
        "pan": extract_pan(cleaned),
        "amount": extract_amount(cleaned),
        "dates": extract_dates(cleaned),
        "raw_text": cleaned
    }

def process_folder(input_dir: str):
    rows = [process_document(os.path.join(input_dir, f)) for f in os.listdir(input_dir)]
    df = pd.DataFrame(rows)
    df.to_csv("outputs/extracted.csv", index=False)
    df.to_excel("outputs/extracted.xlsx", index=False)
    df.to_json("outputs/extracted.json", orient="records")
    return df