import faiss
import numpy
from sentence_transformers import SentenceTransformer

document_1 = "I had chocalate chip pancakes and scrambled eggs for breakfast this morning."
document_2 = "The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees."
document_3 = "Building an exciting new project with LangChain - come check it out!"
document_4 = "Robbers broke into the city bank and stole $1 million in cash."
document_5 = "Wow! That was an amazing movie. I can't wait to see it again."
document_6 = "Is the new iPhone worth the price? Read this review to find out."
document_7 = "The top 10 soccer players in the world right now."
document_8 = "LangGraph is the best framework for building stateful, agentic applications!"
document_9 = "The stock market is down 500 points today due to fears of a recession."

documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9
]

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
embeddings = model.encode(documents)
# print(embeddings)
# print(len(embeddings))


# From https://github.com/facebookresearch/faiss/wiki/Getting-started
index = faiss.IndexFlatL2(len(embeddings[0]))   # build the index
# print(index.is_trained)
index.add(embeddings)                  # add vectors to the index
# print(index.ntotal)

# Explains the output: https://github.com/facebookresearch/faiss/wiki/Getting-started#searching
k = 4                          # we want to see 4 nearest neighbors
D, I = index.search(embeddings[:5], k) # sanity check
# print(I)
# print(D)

query_string = "I love playing football"
print(f"query string: {query_string}")
query =  model.encode([query_string])
D, I = index.search(query, 1)

print(f"result: {documents[I[0][0]]}")



