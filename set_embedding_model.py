from langchain_community.embeddings.ollama import OllamaEmbeddings

model_name = "mxbai-embed-large"

def set_embedding_model():
    embedding_model = OllamaEmbeddings(model=model_name)
    return embedding_model