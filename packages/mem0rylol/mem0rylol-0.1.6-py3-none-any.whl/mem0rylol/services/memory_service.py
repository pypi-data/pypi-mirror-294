# services/memory_service.py
from mem0rylol.utils.logger import logger
from mem0rylol.models.memory_model import MemoryModel
from mem0rylol.services.memory_extraction_service import MemoryExtractionService
from mem0rylol.models.extracted_memory import ExtractedMemory
from typing import List, Dict, Any, Optional
import asyncio
from langchain.prompts import PromptTemplate
from langchain.llms import BaseLLM
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility # type: ignore

import uuid
from mem0rylol.config import Config
from loguru import logger

class MemoryService:
    def __init__(self, config: Config, langchain_client, memory_extraction_service: MemoryExtractionService):
        self.config = config
        self.langchain_client = langchain_client
        self.memory_extraction_service = memory_extraction_service
        self.memory_model = MemoryModel(config)  # Initialize MemoryModel here
        self.milvus_client = None

    async def initialize(self):
        await self.memory_model.initialize()
        self.milvus_client = self.config.get_milvus_client()

    async def create_user_memory_collection(self, user_id: str, session_id: str) -> bool:
        try:
            await self.initialize()
            collection_name = f"user_{user_id}_session_{session_id}"
            logger.info(f"Attempting to create collection: {collection_name}")
            if await self.memory_model.has_collection(collection_name):
                logger.info(f"Collection {collection_name} already exists. Dropping it.")
                await self.memory_model.drop_collection(collection_name)
            schema = self._create_collection_schema()
            logger.info(f"Creating collection with schema: {schema}")
            result = await self.memory_model.create_collection(collection_name, schema)
            if not result:
                logger.error("Failed to create collection")
                return False
            logger.info(f"Successfully created collection: {collection_name}")
            return result
        except Exception as e:
            logger.error(f"Error creating user memory collection: {str(e)}")
            logger.exception("Detailed traceback:")
            return False

    async def store_memory(self, memory: ExtractedMemory) -> bool:
        collection_name = self._get_collection_name(memory.user_id, memory.session_id)
        try:
            for mem in memory.memories:
                logger.debug(f"Attempting to store memory: {mem}")
                result = await self.memory_model.store_memory(collection_name, mem)
                logger.debug(f"Store memory result: {result}")
                if not result:
                    logger.error(f"Failed to store memory in collection {collection_name}")
                    return False
            return True
        except Exception as e:
            logger.error(f"Error storing memory: {str(e)}")
            return False

    async def retrieve_memories(self, user_id: str, session_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        collection_name = self._get_collection_name(user_id, session_id)
        try:
            query_embedding = await self.langchain_client["embeddings"].aembed_query(query)
            return await self.memory_model.retrieve_memory(collection_name, query_embedding, top_k)
        except Exception as e:
            logger.error(f"Error retrieving memories: {str(e)}")
            return []

    async def delete_user_memories(self, user_id: str) -> bool:
        try:
            collections = await self.get_user_sessions(user_id)
            for collection_name in collections:
                await self.memory_model.drop_collection(collection_name)
            return True
        except Exception as e:
            logger.error(f"Error deleting user memories: {str(e)}")
            return False

    async def delete_session_memories(self, user_id: str, session_id: str) -> bool:
        collection_name = self._get_collection_name(user_id, session_id)
        try:
            return await self.memory_model.drop_collection(collection_name)
        except Exception as e:
            logger.error(f"Error deleting session memories: {str(e)}")
            return False

    async def get_user_sessions(self, user_id: str) -> List[str]:
        try:
            all_collections = await self.memory_model.list_collections()
            return [coll for coll in all_collections if coll.startswith(f"user_{user_id}_session_")]
        except Exception as e:
            logger.error(f"Error getting user sessions: {str(e)}")
            return []

    async def extract_and_store_memories(self, user_id: str, session_id: str, input_text: str) -> bool:
        extracted_memory = await self.memory_extraction_service.extract_and_embed_memories(user_id, session_id, input_text)
        collection_name = f"{user_id}_{session_id}_memories"
        
        success = True
        for memory in extracted_memory.memories:
            result = await self.memory_model.store_memory(collection_name, memory)
            if not result:
                success = False
                break
        
        return success

    def _get_collection_name(self, user_id: str, session_id: str) -> str:
        return f"user_{user_id}_session_{session_id}"

    def _create_collection_schema(self):
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=1536)
        ]
        schema = CollectionSchema(fields, "Memory schema")
        return schema

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Cleanup code if needed
        pass