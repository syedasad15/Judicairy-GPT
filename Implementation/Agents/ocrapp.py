import fitz  # PyMuPDF
from PIL import Image
import easyocr
import numpy as np
import re
import streamlit as st

@st.cache_resource
def get_reader():
    return easyocr.Reader(["en"], gpu=False)

def ocr_img(img: Image.Image) -> str:
    reader = get_reader()
    results = reader.readtext(np.array(img), detail=0)
    return " ".join(results)

def strip_html(text: str) -> str:
    return re.sub(r"<[^>]*>", "", text)

def process_pdf_stream(pdf_bytes: bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    total_pages = len(doc)

    for page_num, page in enumerate(doc, start=1):
        parts = []

        # Extract native text
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))
        parts.extend([b[4] for b in blocks if b[4].strip()])

        # OCR images embedded in page
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

        # Fallback full-page OCR if nothing found
        if not parts:
            pix = page.get_pixmap(dpi=150)  # Lower DPI to reduce memory
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            fallback_text = ocr_img(img)
            if fallback_text:
                parts.append(fallback_text)

        yield f"--- Page {page_num} ---\n" + "\n".join(parts)

    doc.close()
