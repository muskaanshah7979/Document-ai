### Document AI Automation System

## Overview
A Streamlit app that extracts key details from uploaded documents (PDFs or images).  
Supports Aadhaar,PAN, and Invoice formats.
If auto‑detection fails, users can select the type from a dropdown.

## Features
- Upload PDFs or images (PNG, JPG, JPEG)  
- OCR with Tesseract + preprocessing via OpenCV  
- Auto document type detection (Aadhaar, PAN, Invoice)  
- Clean tabular output of extracted fields  
- Manual dropdown override if detection fails  

## Tech Stack
- Python, Streamlit  
- OpenCV, Pytesseract, pdfplumber  
- pandas  

## Usage:
streamlit run app_streamlit.py
1. Upload a document.  
2. System detects type and extracts fields.  
3. Results shown in a table.  
4. If not detected, choose type manually.  

