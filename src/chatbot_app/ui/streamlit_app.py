import streamlit as st

from chatbot_app.core.pdf_utils import extract_text_from_pdf, split_text_into_chunks
from chatbot_app.core.retriever import get_answer


def main():
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
