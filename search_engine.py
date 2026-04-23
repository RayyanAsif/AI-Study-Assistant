def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def find_relevant_chunks(query, chunks):
    relevant = []
    query_words = set(query.lower().split())

    for chunk in chunks:
        chunk_words = set(chunk.lower().split())
        if query_words.intersection(chunk_words):
            relevant.append(chunk)

    # Returns the top 3 most relevant chunks to keep the payload clean
    return " ".join(relevant[:3])
