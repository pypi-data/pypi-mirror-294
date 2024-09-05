# tests/test_memory_service.py
import pytest
from mem0rylol.services.memory_service import MemoryService
from mem0rylol.config.config import Config
from mem0rylol.services.memory_extraction_service import MemoryExtractionService
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

@pytest.mark.asyncio
async def test_create_user_memory_collection():
    # Print environment variables for debugging
    logger.info(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')[:5] if os.getenv('OPENAI_API_KEY') else 'None'}...")
    logger.info(f"ZILLIZ_CLOUD_URI: {os.getenv('ZILLIZ_CLOUD_URI')}")
    logger.info(f"ZILLIZ_CLOUD_TOKEN: {os.getenv('ZILLIZ_CLOUD_TOKEN')[:5] if os.getenv('ZILLIZ_CLOUD_TOKEN') else 'None'}...")

    # Check if all required environment variables are set
    assert os.getenv("OPENAI_API_KEY") is not None, "OPENAI_API_KEY is not set in the environment"
    assert os.getenv("ZILLIZ_CLOUD_URI") is not None, "ZILLIZ_CLOUD_URI is not set in the environment"
    assert os.getenv("ZILLIZ_CLOUD_TOKEN") is not None, "ZILLIZ_CLOUD_TOKEN is not set in the environment"

    # Create a Config instance and print its values
    config = Config()
    config.print_config()

    # Add these lines after creating the Config instance
    assert config.ZILLIZ_CLOUD_URI is not None, "ZILLIZ_CLOUD_URI is not set in Config"
    assert config.ZILLIZ_CLOUD_TOKEN is not None, "ZILLIZ_CLOUD_TOKEN is not set in Config"

    # Get the langchain client
    langchain_client = config.get_langchain_client()

    # Initialize MemoryService with the required arguments
    memory_extraction_service = MemoryExtractionService(config, langchain_client)
    memory_service = MemoryService(config, langchain_client, memory_extraction_service)

    # Initialize the MemoryService
    await memory_service.initialize()

    # Run the test
    result = await memory_service.create_user_memory_collection("test_user", "test_session")
    assert result == True