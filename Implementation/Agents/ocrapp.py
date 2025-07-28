import fitz  # PyMuPDF
from PIL import Image
import easyocr
import numpy as np
import re
import streamlit as st

# 1. Cached EasyOCR reader for performance
@st.cache_resource
def get_reader():
    return easyocr.Reader(["en"], gpu=False)

# 2. OCR single image
def ocr_img(img: Image.Image) -> str:
    reader = get_reader()
    results = reader.readtext(np.array(img), detail=0)
    return " ".join(results)

# 3. Strip HTML (in case needed)
def strip_html(text: str) -> str:
    return re.sub(r"<[^>]*>", "", text)

# 4. Generator function for large PDF processing
def extract_pdf_text(pdf_bytes: bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    total_pages = len(doc)

    for page_num, page in enumerate(doc, start=1):
        parts = []

        # Extract native text
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))  # Y, then X
        parts.extend([b[4] for b in blocks if b[4].strip()])

        # OCR embedded images
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha < 4:
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            else:
                pix = fitz.Pixmap(fitz.csRGB, pix)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = ocr_img(img)
            if ocr_text:
                parts.append(ocr_text)

        # Fallback OCR if page is otherwise empty
        if not parts:
            pix = page.get_pixmap(dpi=150)  # Lower DPI for memory efficiency
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            fallback_text = ocr_img(img)
            if fallback_text:
                parts.append(fallback_text)

        yield f"--- Page {page_num} ---\n" + "\n".join(parts)

    doc.close()
