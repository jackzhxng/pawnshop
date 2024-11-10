import faiss
from sentence_transformers import SentenceTransformer


class VectorStore():
    def __init__(self) -> None:
        self.docs = []
        self.model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        # 768 dimensional based on https://huggingface.co/sentence-transformers/all-mpnet-base-v2
        self.index = faiss.IndexFlatL2(768)
        pass 

    def add_documents(self, *docs):
        self.docs.extend(docs)
        embeddings = self.model.encode(list(docs))
        self.index.add(embeddings)

    """
    Queries the k-nearest neighbors to the query string `query`
    """
    def similarity_search(self, query, k):
        query_embedding = self.model.encode([query])
        # Explains the output: https://github.com/facebookresearch/faiss/wiki/Getting-started#searching
        _, I = self.index.search(query_embedding, k)

        result = []
        for i in range(k):
            # print(f"{i}: {self.docs[I[0][i]]}")
            result.append(self.docs[I[0][i]])
        return result




v = VectorStore()
v.add_documents("foo", "bar")
v.similarity_search("hi", 3)
v.add_documents("hello", "world")
print(v.similarity_search("hi", 3))
