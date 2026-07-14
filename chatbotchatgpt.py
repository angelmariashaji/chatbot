import re
import streamlit as st
import pdfplumber


def extract_text_from_pdf(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    return "\n\n".join(pages)


def split_text_into_chunks(text):
    paragraphs = re.split(r"\n\s*\n", text.strip())
    chunks = []
    current = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        if len(current) + len(paragraph) <= 500:
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


def get_answer(question, chunks):
    if not chunks:
        return "Please upload a PDF with readable text.", []

    question_tokens = set(normalize(question))
    scored_chunks = []

    for chunk in chunks:
        chunk_tokens = set(normalize(chunk))
        overlap = len(question_tokens & chunk_tokens)
        score = overlap + 0.1 * len([token for token in question_tokens if token in chunk_tokens])
        scored_chunks.append((score, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    best_chunk = scored_chunks[0][1] if scored_chunks else chunks[0]
    relevant_chunks = [chunk for _, chunk in scored_chunks[:3]]

    return best_chunk, relevant_chunks


st.set_page_config(page_title="PDF Chatbot", page_icon="📄")
st.title("PDF Chatbot")
st.write("Upload a PDF and ask a question about it.")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:
    text = extract_text_from_pdf(uploaded_file)
    chunks = split_text_into_chunks(text)

    st.success(f"Loaded {len(chunks)} text chunks from the document.")

    question = st.text_input("Ask a question about the PDF")

    if question:
        answer, relevant_chunks = get_answer(question, chunks)

        st.subheader("Answer")
        st.write(answer)

        with st.expander("Relevant passages"):
            for index, chunk in enumerate(relevant_chunks, start=1):
                st.write(f"**Passage {index}**")
                st.write(chunk)
