from chatbot_app.core.pdf_utils import normalize


def get_answer(question, chunks):
    if not chunks:
        return "Please upload a PDF with readable text.", []

    question_tokens = set(normalize(question))
    scored_chunks = []

    for chunk in chunks:
        chunk_tokens = set(normalize(chunk))
        overlap = len(question_tokens & chunk_tokens)
        scored_chunks.append((overlap, chunk))

    scored_chunks.sort(key=lambda item: item[0], reverse=True)
    best_chunk = scored_chunks[0][1] if scored_chunks else chunks[0]
    relevant_chunks = [chunk for _, chunk in scored_chunks[:3]]

    return best_chunk, relevant_chunks
