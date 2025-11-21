class Retriever:
    def add_document(self, doc_id: str, text: str, metadata: dict):
        pass

    def query(self, question: str, top_k: int = 5):
        """Return list of {text, metadata} chunks relevant to `question`."""
        pass