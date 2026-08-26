
import pymupdf  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    """
    Takes a Streamlit uploaded PDF file
    and returns extracted plain text.
    """

    pdf_bytes = uploaded_file.read()

    document = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    text = ""

    for page in document:
        text += page.get_text()

    return text