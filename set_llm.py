from langchain_community.llms.ollama import Ollama

model_name = "llama3"

def set_llm():
    llm_model = Ollama(model=model_name)
    return llm_model