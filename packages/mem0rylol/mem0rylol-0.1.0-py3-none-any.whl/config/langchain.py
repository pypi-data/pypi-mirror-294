# config/langchain.py
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore

def get_langchain_client(groq_api_key, openai_api_key):
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="mixtral-8x7b-32768"
    )
    
    underlying_embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=openai_api_key
    )
    
    store = LocalFileStore("./cache/")
    cached_embedder = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings, 
        store, 
        namespace=underlying_embeddings.model
    )
    
    memory_extraction_prompt = PromptTemplate(
        input_variables=["input"],
        template="Extract relevant memories, facts, and preferences from the following input:\n\n{input}\n\nExtracted memories (in bullet-point format):"
    )
    
    chain = memory_extraction_prompt | llm
    
    return {
        "llm": llm,
        "embeddings": cached_embedder,
        "chain": chain
    }