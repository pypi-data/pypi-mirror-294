# config/langchain.py
from langchain_groq import ChatGroq
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

def get_langchain_client(openai_api_key, zilliz_cloud_uri, zilliz_cloud_token):
    # Initialize the ChatGroq model
    chat_model = ChatGroq(
        temperature=0.7,
        model_name="mixtral-8x7b-32768",
        max_tokens=1024
    )

    # Initialize the OpenAI embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Create a conversation memory
    memory = ConversationBufferMemory()

    # Create a conversation chain
    chain = ConversationChain(
        llm=chat_model,
        memory=memory,
        verbose=True
    )

    # Return a dictionary containing the initialized components
    return {
        "chain": chain,
        "embeddings": embeddings,
        "zilliz_cloud_uri": zilliz_cloud_uri,
        "zilliz_cloud_token": zilliz_cloud_token,
        "llm": chat_model  # Add this line to include the llm in the returned dictionary
    }