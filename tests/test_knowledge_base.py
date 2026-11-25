
import app.services.knowledge_base as kb

class FakeCollection:
    def __init__(self):
        self.documents = []
        self.metadatas = []
        self.ids = []

    def count(self):
        return len(self.documents)

    def upsert(self, ids, documents, embeddings, metadatas):
        self.ids = ids
        self.documents = documents
        self.metadatas = metadatas

    def query(self, query_embeddings, n_results):
        return {
            "documents": [self.documents[:n_results]],
            "metadatas": [self.metadatas[:n_results]]
        }

def test_document_chunking():
    text = "abcdefghijklmnopqrstuvwxyz"

    chunks = kb.split_into_chunks(
        text,
        chunk_size=10,
        overlap=2
    )

    assert len(chunks) == 3
    assert chunks[0][-2:] == chunks[1][:2]
    assert chunks[1][-2:] == chunks[2][:2]

def test_empty_document_rejected():
    try:
        kb.add_document("   ", "empty.txt")
        assert False, "Expected ValueError"
    except ValueError as error:
        assert "no readable text" in str(error)

def test_document_storage(monkeypatch):
    fake_collection = FakeCollection()
    monkeypatch.setattr(kb, "collection", fake_collection)

    monkeypatch.setattr(
        kb,
        "generate_embeddings",
        lambda texts, task_type: [[0.1, 0.2] for _ in texts]
    )

    count = kb.add_document(
        "This is a sample customer support policy.",
        "sample_policy.txt"
    )

    assert count == 1
    assert len(fake_collection.documents) == 1
    assert fake_collection.metadatas[0]["source"] == "sample_policy.txt"

def test_knowledge_search(monkeypatch):
    fake_collection = FakeCollection()

    fake_collection.documents = [
        "Duplicate payments must be verified before refund."
    ]
    fake_collection.metadatas = [
        {"source": "sample_policy.txt", "chunk": 0}
    ]

    monkeypatch.setattr(kb, "collection", fake_collection)

    monkeypatch.setattr(
        kb,
        "generate_embeddings",
        lambda texts, task_type: [[0.1, 0.2]]
    )

    results = kb.search_knowledge_base(
        "I was charged twice.",
        results_count=3
    )

    assert len(results) == 1
    assert results[0]["source"] == "sample_policy.txt"
    assert "Duplicate payments" in results[0]["text"]