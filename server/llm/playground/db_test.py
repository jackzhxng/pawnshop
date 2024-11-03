# NOTE: Ollama embeddings suck
# from langchain_ollama import OllamaEmbeddings
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS

from uuid import uuid4
from langchain_core.documents import Document

from langchain_huggingface.embeddings import HuggingFaceEmbeddings


# NOTE: Ollama embeddings suck
# embeddings = OllamaEmbeddings(
#     model="llama3.2",
# )

# According to https://python.langchain.com/api_reference/huggingface/embeddings/langchain_huggingface.embeddings.huggingface.HuggingFaceEmbeddings.html:
# Default model name is "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'trust_remote_code': True}
embeddings = HuggingFaceEmbeddings(
    model_kwargs=model_kwargs
)

index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

vector_store = FAISS(
    embedding_function=embeddings,
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={},
)

document_1 = Document(
    page_content="I had chocalate chip pancakes and scrambled eggs for breakfast this morning.",
    metadata={"source": "tweet"},
)

document_2 = Document(
    page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
    metadata={"source": "news"},
)

document_3 = Document(
    page_content="Building an exciting new project with LangChain - come check it out!",
    metadata={"source": "tweet"},
)

document_4 = Document(
    page_content="Robbers broke into the city bank and stole $1 million in cash.",
    metadata={"source": "news"},
)

document_5 = Document(
    page_content="Wow! That was an amazing movie. I can't wait to see it again.",
    metadata={"source": "tweet"},
)

document_6 = Document(
    page_content="Is the new iPhone worth the price? Read this review to find out.",
    metadata={"source": "website"},
)

document_7 = Document(
    page_content="The top 10 soccer players in the world right now.",
    metadata={"source": "website"},
)

document_8 = Document(
    page_content="LangGraph is the best framework for building stateful, agentic applications!",
    metadata={"source": "tweet"},
)

document_9 = Document(
    page_content="The stock market is down 500 points today due to fears of a recession.",
    metadata={"source": "news", "character": "Erik"},
)

documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
]
uuids = [str(uuid4()) for _ in range(len(documents))]

vector_store.add_documents(documents=documents, ids=uuids)

"""
Retriever
"""
retriever = vector_store.as_retriever(
    search_type="mmr", search_kwargs={"k": 1})
res = retriever.invoke("Stealing from the bank is a crime",
                       filter={"source": "news"})
print(f"Invoking 'Stealing from the bank is a crime': {res}")

"""
Similarity search
"""
results = vector_store.similarity_search_with_score(
    "What phone should I buy?",
    k=3,
    filter={"character": "Erik"},
)
for res, score in results:
    print(f"*[Score: {score:3f}] {res.page_content} [{res.metadata}]")
