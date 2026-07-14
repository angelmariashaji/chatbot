import re
import pdfplumber


def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n\n".join(pages)


def split_text_into_chunks(text, chunk_limit=500):
    paragraphs = re.split(r"\n\s*\n", text.strip())
    chunks = []
    current = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(current) + len(paragraph) <= chunk_limit:
            current = f"{current}\n{paragraph}".strip() if current else paragraph
        else:
            if current:
                chunks.append(current)
            current = paragraph

    if current:
        chunks.append(current)

    return chunks


def normalize(text):
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).split()
