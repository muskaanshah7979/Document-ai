import streamlit as st
import cv2
import numpy as np
import pytesseract
from PIL import Image
import re
from dateutil import parser
import pdfplumber
import pandas as pd

st.title(" Document AI Automation System")
st.write("Upload a document (PDF or image) and automatically extract key details.")

uploaded_file = st.file_uploader("Upload a document", type=["pdf", "png", "jpg", "jpeg"])

def preprocess_image(uploaded_file):
    pil_img = Image.open(uploaded_file).convert("RGB")
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return thresh

def ocr_text(img, psm=6):
    cfg = f"--psm {psm} --oem 3"
    return pytesseract.image_to_string(img, config=cfg, lang="eng")

def ocr_digits(img):
    cfg = "--psm 6 -c tessedit_char_whitelist=0123456789"
    return pytesseract.image_to_string(img, config=cfg, lang="eng")


def detect_document_type(text):
    if "Aadhaar" in text or "UIDAI" in text:
        return "Aadhaar"
    elif "PAN" in text or "Income Tax" in text:
        return "PAN"
    elif "Invoice" in text or "Customer" in text:
        return "Invoice"
    else:
        return None


def extract_aadhaar(text, digits_text=""):
    fields = {}
    name_match = re.search(r"[A-Z][a-z]+ [A-Z][a-z]+(?: [A-Z][a-z]+)*", text)
    if name_match:
        fields["Name"] = name_match.group(0).strip()

    dob_match = re.search(r"DOB[: ]+(\d{2}[/-]\d{2}[/-]\d{4})", text)
    if dob_match:
        try:
            fields["DOB"] = parser.parse(dob_match.group(1), dayfirst=True).date().isoformat()
        except Exception:
            fields["DOB"] = dob_match.group(1)

    gender_match = re.search(r"\b(Male|Female)\b", text, re.I)
    if gender_match:
        fields["Gender"] = gender_match.group(1).title()

    id_match = re.search(r"\b\d{4}[ ]?\d{4}[ ]?\d{4}\b", text)
    if id_match:
        fields["Aadhaar Number"] = id_match.group(0).replace(" ", "")
    elif digits_text:
        digits_match = re.search(r"\d{12}", digits_text)
        if digits_match:
            fields["Aadhaar Number"] = digits_match.group(0)
    return fields

def extract_pan(text):
    fields = {}
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
       
        if "Income Tax" in line or "Permanent Account Number" in line:
            continue
        if line.lower().startswith("name"):
            fields["Name"] = line.split(":", 1)[-1].strip()
        elif "father" in line.lower():
            fields["Father's Name"] = line.split(":", 1)[-1].strip()
        elif line.lower().startswith("dob"):
            fields["DOB"] = line.split(":", 1)[-1].strip()
        elif re.match(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", line):
            fields["PAN Number"] = line.strip()
    return fields

def extract_invoice(text):
    fields = {}
    cust_match = re.search(r"Customer Name[:\- ]+([A-Za-z ]+)", text, re.I)
    if cust_match:
        fields["Customer Name"] = cust_match.group(1).strip()

    inv_match = re.search(r"Invoice (ID|No)[:\- ]+([A-Za-z0-9\-]+)", text, re.I)
    if inv_match:
        fields["Invoice ID"] = inv_match.group(2).strip()

    date_match = re.search(r"Date[:\- ]+(\d{2}[/-]\d{2}[/-]\d{4})", text)
    if date_match:
        fields["Invoice Date"] = date_match.group(1).strip()

    amt_match = re.search(r"(Amount|Total)[:\- ]+([\d,\.]+)", text, re.I)
    if amt_match:
        fields["Amount"] = amt_match.group(2).strip()
    return fields

if uploaded_file is not None:
    st.success(f"File {uploaded_file.name} uploaded successfully!")

    with st.spinner("Processing document..."):
        text = ""
        digits_text = ""

        if uploaded_file.name.lower().endswith(".pdf"):
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        else:
            processed_img = preprocess_image(uploaded_file)
            text = ocr_text(processed_img, psm=6)
            digits_text = ocr_digits(processed_img)

        text = text.strip()
        doc_type = detect_document_type(text)

        if doc_type is None:
            st.warning(" Document type not recognized. Please select the type below:")
            doc_type = st.selectbox("Select Document Type", ["Aadhaar", "PAN", "Invoice"])

        if doc_type == "Aadhaar":
            fields = extract_aadhaar(text, digits_text)
        elif doc_type == "PAN":
            fields = extract_pan(text)
        elif doc_type == "Invoice":
            fields = extract_invoice(text)
        else:
            fields = {}

    st.success(" Processing complete!")
    st.subheader(f"{doc_type} Document Details")

    if fields:
        df = pd.DataFrame(list(fields.items()), columns=["Field", "Value"])
        st.table(df)
    else:
        st.warning("No key fields detected.")