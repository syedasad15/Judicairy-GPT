import fitz  # PyMuPDF
from PIL import Image
import easyocr
import numpy as np
import re
import streamlit as st

# -----------------------------
# 1. Load EasyOCR reader (cached)
# -----------------------------
@st.cache_resource
def get_reader():
    return easyocr.Reader(["en"], gpu=False)

# -----------------------------
# 2. OCR a single image
# -----------------------------
def ocr_img(img: Image.Image) -> str:
    reader = get_reader()
    results = reader.readtext(np.array(img), detail=0)
    return " ".join(results)

# -----------------------------
# 3. Remove HTML tags
# -----------------------------
def strip_html(text: str) -> str:
    return re.sub(r"<[^>]*>", "", text)

# -----------------------------
# 4. Extract text from PDF (streaming)
# -----------------------------
def extract_pdf_text(pdf_bytes: bytes):
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise RuntimeError(f"Failed to open PDF: {e}")

    for page_num, page in enumerate(doc, start=1):
        parts = []

        # Extract text blocks
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))  # Y, then X
        parts.extend([b[4] for b in blocks if b[4].strip()])

        # OCR images embedded in page
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.n - pix.alpha < 4:
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                else:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                ocr_text = ocr_img(img)
                if ocr_text:
                    parts.append(ocr_text)
            except Exception as e:
                st.warning(f"Skipping image due to error: {e}")

        # Fallback full-page OCR if nothing extracted
        if not parts:
            try:
                pix = page.get_pixmap(dpi=150)  # lower DPI for memory safety
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                fallback_text = ocr_img(img)
                if fallback_text:
                    parts.append(fallback_text)
            except Exception as e:
                st.warning(f"Fallback OCR failed on page {page_num}: {e}")

        yield f"--- Page {page_num} ---\n" + "\n".join(parts)

    doc.close()
