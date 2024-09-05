import os
from dotenv import load_dotenv
from pymilvus import connections  # type: ignore
from loguru import logger

load_dotenv()

class Config:
    def __init__(self):
        # Langchain
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

        # Zilliz Cloud (Milvus)
        self.ZILLIZ_CLOUD_URI = os.getenv("ZILLIZ_CLOUD_URI")
        self.ZILLIZ_CLOUD_TOKEN = os.getenv("ZILLIZ_CLOUD_TOKEN")

        # Milvus
        self.MILVUS_HOST = os.getenv("MILVUS_HOST")
        self.MILVUS_PORT = os.getenv("MILVUS_PORT")

    @classmethod
    def get_milvus_client(cls):
        from mem0rylol.config.milvus import get_milvus_client
        config = cls()  # Create an instance of Config
        return get_milvus_client(config.ZILLIZ_CLOUD_URI, config.ZILLIZ_CLOUD_TOKEN)

    @classmethod
    def get_langchain_client(cls):
        from mem0rylol.config.langchain import get_langchain_client
        config = cls()  # Create an instance of Config
        return get_langchain_client(config.OPENAI_API_KEY, config.ZILLIZ_CLOUD_URI, config.ZILLIZ_CLOUD_TOKEN)

    def print_config(self):
        logger.info(f"Config OPENAI_API_KEY: {self.OPENAI_API_KEY[:5] if self.OPENAI_API_KEY else 'None'}...")
        logger.info(f"Config ZILLIZ_CLOUD_URI: {self.ZILLIZ_CLOUD_URI}")
        logger.info(f"Config ZILLIZ_CLOUD_TOKEN: {self.ZILLIZ_CLOUD_TOKEN[:5] if self.ZILLIZ_CLOUD_TOKEN else 'None'}...")

    # Add other configuration methods as needed