from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
sentences = [
    "Hugging Face makes NLP easy.",
    "Transformers are powerful for deep learning."
]

embeddings = model.encode(sentences)
print("Embedding shape: ", embeddings.shape)

