
import pdfplumber
from pdf2image import convert_from_path
from ocr_utils import ocr_image

def parse_pdf_text(pdf_path: str) -> str:
  
    full_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            full_text.append(txt)
    joined = "\n".join(full_text).strip()
    if len(joined) >= 200:
        return joined

   
    ocr_texts = []
    images = convert_from_path(pdf_path, dpi=300)
    for idx, img in enumerate(images):
        temp_path = f"_tmp_page_{idx}.png"
        img.save(temp_path)
        ocr_texts.append(ocr_image(temp_path))
    return "\n".join(ocr_texts)