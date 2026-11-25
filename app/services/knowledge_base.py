
import hashlib
from pathlib import Path

import chromadb

from app.services.gemini_service import generate_embeddings


BASE_DIR = Path(__file__).resolve().parents[2]
CHROMA_PATH = BASE_DIR / "data" / "chroma_db"

CHROMA_PATH.mkdir(parents=True, exist_ok=True)

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

collection = chroma_client.get_or_create_collection(
    name="resolveai_knowledge"
)


def split_into_chunks(text, chunk_size=1000, overlap=150):
    """Split a document into smaller overlapping text chunks."""

    text = " ".join(text.split())

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start += chunk_size - overlap

    return chunks


def add_document(text, source):
    """Embed document chunks and store them in ChromaDB."""

    chunks = split_into_chunks(text)

    if not chunks:
        raise ValueError("The document contains no readable text.")

    embeddings = generate_embeddings(
        chunks,
        "RETRIEVAL_DOCUMENT"
    )

    ids = []
    metadatas = []

    for index, chunk in enumerate(chunks):
        unique_value = f"{source}:{index}:{chunk}"
        document_id = hashlib.sha256(
            unique_value.encode("utf-8")
        ).hexdigest()

        ids.append(document_id)

        metadatas.append({
            "source": source,
            "chunk": index
        })

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


def search_knowledge_base(query, results_count=3):
    """Find relevant document chunks using semantic search."""

    if collection.count() == 0:
        return []

    query_embedding = generate_embeddings(
        [query],
        "RETRIEVAL_QUERY"
    )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(results_count, collection.count())
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    matches = []

    for document, metadata in zip(documents, metadatas):
        matches.append({
            "text": document,
            "source": metadata.get("source", "Unknown")
        })

    return matches


def get_knowledge_count():
    """Return the number of stored document chunks."""

    return collection.count()
