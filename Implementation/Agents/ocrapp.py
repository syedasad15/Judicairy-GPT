import fitz  # PyMuPDF
from PIL import Image
import easyocr
import numpy as np
import re
import psutil
import time

# Load OCR reader once
_reader = None
def get_reader():
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(["en"], gpu=False)
    return _reader

def ocr_img(img: Image.Image) -> str:
    reader = get_reader()
    results = reader.readtext(np.array(img), detail=0)
    return " ".join(results)

def strip_html(text: str) -> str:
    return re.sub(r"<[^>]*>", "", text)

def extract_pdf_text(pdf_bytes: bytes) -> str:
    MAX_MEM_MB = 1200  # Raise memory limit to 1.2 GB
    MAX_TIME_S = 180   # Raise time limit to 3 minutes
    MAX_IMG_SIZE = 800  # Skip images larger than 800 pixels
    DPI_FALLBACK = 100  # Use lower DPI for fallback OCR

    start_time = time.time()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    all_parts = []

    for page_num, page in enumerate(doc, start=1):
        if psutil.virtual_memory().used // 1024**2 > MAX_MEM_MB:
            raise MemoryError("Memory limit exceeded")
        if time.time() - start_time > MAX_TIME_S:
            raise TimeoutError("Time limit exceeded")

        parts = []

        # 1. Extract native text blocks
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda b: (b[1], b[0]))  # Sort by Y, then X
        parts.extend([b[4] for b in blocks if b[4].strip()])

        # 2. OCR embedded images
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            pix = fitz.Pixmap(doc, xref)
            if max(pix.width, pix.height) > MAX_IMG_SIZE:
                pix = None
                continue
            if pix.n - pix.alpha < 4:
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            else:
                pix = fitz.Pixmap(fitz.csRGB, pix)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            ocr_text = ocr_img(img)
            if ocr_text:
                parts.append(ocr_text)

        # 3. If page still has no text, fallback to full page OCR
        if not parts:
            pix = page.get_pixmap(dpi=DPI_FALLBACK)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            fallback_text = ocr_img(img)
            if fallback_text:
                parts.append(fallback_text)

        all_parts.append("\n".join(parts))

    doc.close()
    return strip_html("\n\n".join(all_parts))\
