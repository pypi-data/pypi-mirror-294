import os
from dotenv import load_dotenv
from pymilvus import connections
from loguru import logger

load_dotenv()

class Config:
    # Langchain
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Neo4J
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

    # Zilliz Cloud (Milvus)
    ZILLIZ_CLOUD_URI = os.getenv("ZILLIZ_CLOUD_URI")
    ZILLIZ_CLOUD_TOKEN = os.getenv("ZILLIZ_CLOUD_TOKEN")

    # Milvus
    MILVUS_HOST = os.getenv("MILVUS_HOST")
    MILVUS_PORT = os.getenv("MILVUS_PORT")

    @classmethod
    async def get_milvus_client(cls):
        try:
            connections.connect(
                alias="default", 
                uri=cls.ZILLIZ_CLOUD_URI,
                token=cls.ZILLIZ_CLOUD_TOKEN
            )
            return connections
        except Exception as e:
            logger.error(f"Failed to connect to Zilliz Cloud: {str(e)}")
            raise

    @classmethod
    def get_langchain_client(cls):
        from config.langchain import get_langchain_client
        return get_langchain_client(cls.GROQ_API_KEY, cls.OPENAI_API_KEY)

    @classmethod
    def get_milvus_connection(cls):
        return {
            "host": cls.ZILLIZ_CLOUD_URI,
            "port": cls.MILVUS_PORT
        }

    # Add other configuration methods as needed