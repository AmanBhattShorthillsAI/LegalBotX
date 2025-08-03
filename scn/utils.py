from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

def extract_text_auto(pdf_path):
    """Extract text from a PDF file using PyPDF2. Falls back to OCR if direct extraction fails."""
    # Try direct extraction with PyPDF2
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        if text.strip():  # If non-empty text found
            return text
    except Exception as e:
        print(f"PyPDF2 extraction failed: {e}")

    # Fallback to OCR
    try:
        images = convert_from_path(pdf_path)
        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img)
        return ocr_text
    except Exception as e:
        print(f"OCR extraction failed: {e}")
        return ""


def chunk_text(text, max_chunk_size=512):
    """Split text into chunks of up to max_chunk_size characters, attempting to split at sentence boundaries."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks, current_chunk = [], ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks


from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(chunks):
    """Generate embeddings for a list of text chunks using SentenceTransformer."""
    return model.encode(chunks, show_progress_bar=True)

