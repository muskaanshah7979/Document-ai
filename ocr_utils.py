
import os
import cv2
import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
OCR_LANG = "eng"

def preprocess_image_for_ocr(image_path: str) -> Image.Image:
    """Preprocess image to improve OCR accuracy."""
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    gray = cv2.bilateralFilter(gray, d=7, sigmaColor=75, sigmaSpace=75)
    
    
    thr = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 35, 11
    )
    
    
    scale = 1.5
    resized = cv2.resize(thr, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    return Image.fromarray(resized)

def ocr_image(image_path: str) -> str:
    """Run OCR on an image file and return extracted text."""
    pil_img = preprocess_image_for_ocr(image_path)
    text = pytesseract.image_to_string(pil_img, lang=OCR_LANG)
    return text