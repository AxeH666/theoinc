from apps.ai_assistant.models import KnowledgeBase


CHROMA_PATH = "/app/chroma_db"
COLLECTION_NAME = "solar_knowledge"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer

        _embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

    return _embedding_model


def get_collection():
    import chromadb

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def index_knowledge_base():
    """Index all active knowledge base entries into ChromaDB."""
    knowledge_entries = list(
        KnowledgeBase.objects.filter(is_active=True).order_by("id")
    )

    collection = get_collection()

    existing = collection.get()
    existing_ids = existing.get("ids", [])
    if existing_ids:
        collection.delete(ids=existing_ids)

    if not knowledge_entries:
        return 0

    documents = [
        f"{entry.title}\n\nCategory: {entry.get_category_display()}\n\n{entry.content}"
        for entry in knowledge_entries
    ]
    embeddings = get_embedding_model().encode(documents).tolist()
    ids = [f"knowledge-base-{entry.pk}" for entry in knowledge_entries]
    metadatas = [
        {
            "knowledge_base_id": entry.pk,
            "title": entry.title,
            "category": entry.category,
        }
        for entry in knowledge_entries
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    return len(ids)


def search_knowledge(query_text, n_results=3):
    """Search indexed knowledge entries and return the best matching chunks."""
    collection = get_collection()
    current = collection.get(limit=1)
    if not current.get("ids"):
        index_knowledge_base()
        current = collection.get(limit=1)

    if not current.get("ids"):
        return []

    query_embedding = get_embedding_model().encode([query_text]).tolist()[0]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    documents = results.get("documents", [[]])
    return documents[0] if documents else []
