import streamlit as st
import fitz  # PyMuPDF – no Poppler
from PIL import Image
import easyocr
import numpy as np
import io

# -------------------------------------------------
# 1️⃣  One-time load of EasyOCR Reader (CPU)
# -------------------------------------------------
@st.cache_resource
def load_reader():
    return easyocr.Reader(["en"], gpu=False)  # change gpu=True if CUDA available

reader = load_reader()

# -------------------------------------------------
# 2️⃣  OCR helper
# -------------------------------------------------
def ocr_img(img: Image.Image) -> str:
    results = reader.readtext(np.array(img), detail=0)
    return " ".join(results)

# -------------------------------------------------
# 3️⃣  Core extractor: text layer + inline images + fallback page render
# -------------------------------------------------
def extract_all_text(pdf_bytes, progress_bar):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    total_pages = len(doc)
    full_parts = []

    for page_num, page in enumerate(doc, start=1):
        page_parts = []

        # 1) Native text layer with formatting
        blocks = page.get_text("blocks")
        blocks.sort(key=lambda block: (block[1], block[0]))  # Sort by y, then by x coordinate
        for b in blocks:
            text = b[4]
            font_size = b[5]  # Font size is the 6th element in the block
            font_name = b[6]  # Font name is the 7th element in the block
            page_parts.append(f'<p style="font-size: {font_size}pt; font-family: {font_name};">{text}</p>')

        # 2) Inline / embedded images
        for img_info in page.get_images(full=True):
            xref = img_info[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha < 4:  # GRAY or RGB
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            else:                      # CMYK → RGB
                pix = fitz.Pixmap(fitz.csRGB, pix)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            txt = ocr_img(img)
            if txt:
                page_parts.append(f'<p style="font-size: 12pt; font-family: Arial;">{txt}</p>')
            pix = None

        # 3) If no text at all → render page bitmap
        if not page_parts:
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            txt = ocr_img(img)
            if txt:
                page_parts.append(f'<p style="font-size: 12pt; font-family: Arial;">{txt}</p>')

        full_parts.append("\n".join(page_parts))
        progress_bar.progress(page_num / total_pages, text=f"Processing page {page_num}/{total_pages}")

    return full_parts
# -------------------------------------------------
# 4️⃣  Strip HTML for TXT download
# -------------------------------------------------
import re
def strip_html(text):
    return re.sub(r"<[^>]*>", "", text)

# -------------------------------------------------
# 5️⃣  Streamlit UI
# -------------------------------------------------
st.markdown("# 🎯 OCR-Zero")
st.title("📄 PDF OCR (EasyOCR – No Tesseract Binary)")
st.write("Upload a PDF and extract **all** readable text.")

uploaded = st.file_uploader("Choose a PDF", type=["pdf"])

if uploaded:
    if st.button("Process PDF"):
        progress_bar = st.progress(0, text="Processing…")
        with st.spinner("Processing…"):
            text_parts = extract_all_text(uploaded.read(), progress_bar)
        st.success("Done!")

        # Build HTML for display
        html_display = "\n".join(
            f"<h3>Page {i+1}</h3><div>{page}</div>" for i, page in enumerate(text_parts)
        )
        st.markdown(html_display, unsafe_allow_html=True)

        # Clean TXT for download
        plain_txt = strip_html("\n\n".join(text_parts))
        st.download_button(
            label="Download TXT",
            data=plain_txt,
            file_name=f"{uploaded.name.rsplit('.',1)[0]}.txt",
            mime="text/plain",
        )