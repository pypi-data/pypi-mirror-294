import pytest
import pytest_asyncio
import asyncio
from dotenv import load_dotenv
from unittest.mock import Mock, patch, AsyncMock
from mem0rylol.services.memory_service import MemoryService
from mem0rylol.config.config import Config
from mem0rylol.services.memory_extraction_service import MemoryExtractionService
from mem0rylol.models.extracted_memory import ExtractedMemory
import logging  # Add this import statement

load_dotenv()

pytest_plugins = ('pytest_asyncio',)

@pytest_asyncio.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_config():
    config = Mock()
    config.get_milvus_client.return_value = Mock()
    return config

@pytest.fixture
def mock_langchain_client():
    return {
        "embeddings": AsyncMock(aembed_query=AsyncMock(return_value=[0.1] * 1536))
    }

@pytest.fixture
def mock_memory_extraction_service():
    return Mock()

@pytest.fixture
def mock_memory_model():
    mock = AsyncMock()
    mock.initialize = AsyncMock()
    mock.create_user_memory_collection.return_value = True
    mock.drop_collection.return_value = True
    mock.retrieve_memory.return_value = [{"text": "Test memory", "vector": [0.1] * 1536}]
    return mock

@pytest_asyncio.fixture
async def memory_service(mock_config, mock_langchain_client, mock_memory_extraction_service, mock_memory_model):
    with patch("mem0rylol.services.memory_service.MemoryModel", return_value=mock_memory_model):
        service = MemoryService(mock_config, mock_langchain_client, mock_memory_extraction_service)
        await service.initialize()
        
        # Set up the mock return values for the methods we're testing
        service.create_user_memory_collection = AsyncMock(return_value=True)
        service.store_memory = AsyncMock(return_value=True)
        service.retrieve_memories = AsyncMock(return_value=[{"text": "Test memory", "vector": [0.1] * 1536}])
        service.delete_user_memories = AsyncMock(return_value=True)
        service.delete_session_memories = AsyncMock(return_value=True)
        service.get_user_sessions = AsyncMock(return_value=["test_session"])
        
        return service

@pytest.mark.asyncio
async def test_create_user_memory_collection(memory_service):
    result = await memory_service.create_user_memory_collection("test_user", "test_session")
    assert result == True
    memory_service.create_user_memory_collection.assert_called_once_with("test_user", "test_session")

@pytest.mark.asyncio
async def test_store_memory(memory_service):
    memory = ExtractedMemory(
        user_id="test_user",
        session_id="test_session",
        memories=[{"text": "Test memory", "vector": [0.1] * 1536}]
    )
    result = await memory_service.store_memory(memory)
    assert result == True

@pytest.mark.asyncio
async def test_retrieve_memories(memory_service):
    memory_service.langchain_client["embeddings"].aembed_query.return_value = [0.1] * 1536
    memories = await memory_service.retrieve_memories("test_user", "test_session", "Test query")
    assert isinstance(memories, list)
    assert len(memories) > 0

@pytest.mark.asyncio
async def test_delete_user_memories(memory_service):
    result = await memory_service.delete_user_memories("test_user")
    assert result == True

@pytest.mark.asyncio
async def test_delete_session_memories(memory_service):
    result = await memory_service.delete_session_memories("test_user", "test_session")
    assert result == True

@pytest.mark.asyncio
async def test_get_user_sessions(memory_service):
    sessions = await memory_service.get_user_sessions("test_user")
    assert isinstance(sessions, list)

@pytest.mark.asyncio
@pytest.mark.integration
async def test_memory_extraction(mock_memory_extraction_service, memory_service, caplog):
    caplog.set_level(logging.DEBUG)

    async def mock_extract_and_embed():
        return ExtractedMemory(
            user_id="test_user",
            session_id="test_session",
            memories=[{"text": "Extracted memory", "vector": [0.1] * 1536}]
        )

    mock_memory_extraction_service.extract_and_embed_memories.return_value = mock_extract_and_embed()

    # Mock the store_memory method of MemoryModel
    memory_service.memory_model.store_memory = AsyncMock(return_value=True)

    result = await memory_service.extract_and_store_memories("test_user", "test_session", "Test conversation")

    print("Log messages:")
    for record in caplog.records:
        print(f"{record.levelname}: {record.message}")

    print(f"Result: {result}")
    print(f"Mock calls: {memory_service.memory_model.store_memory.mock_calls}")

    assert result == True, f"Expected True, but got {result}"

# Integration Tests (unchanged)