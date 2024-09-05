# models/memory_model.py
import logging
from urllib.parse import urlparse
from pymilvus import utility, MilvusClient, Collection, FieldSchema, CollectionSchema, DataType, connections  # type: ignore
from typing import Dict, List, Any, Optional
import asyncio
from functools import lru_cache
from langchain_community.vectorstores import Milvus
from mem0rylol.utils.logger import logger
from mem0rylol.config.config import Config

class MemoryModel:
    def __init__(self, config: Config):
        self.config = config
        self.milvus_client = None

    def initialize(self):
        self.milvus_client = self.config.get_milvus_client()
        # Add any additional initialization if needed

    async def has_collection(self, collection_name: str) -> bool:
        if not self.milvus_client:
            raise RuntimeError("MemoryModel not initialized. Call initialize() first.")
        return utility.has_collection(collection_name)

    async def create_collection(self, collection_name: str, schema: CollectionSchema) -> bool:
        try:
            collection = Collection(name=collection_name, schema=schema)
            collection.create_index(field_name="vector", index_params={"index_type": "IVF_FLAT", "metric_type": "L2", "params": {"nlist": 1024}})
            logger.info(f"Created collection: {collection_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating collection: {str(e)}")
            return False

    async def store_memory(self, collection_name: str, memory: Dict[str, Any]) -> bool:
        try:
            collection = Collection(collection_name)
            collection.load()
            result = collection.insert([memory])
            collection.flush()
            logger.info(f"Memory stored in collection {collection_name}: {memory}")
            return result.insert_count > 0
        except Exception as e:
            logger.error(f"Error storing memory in collection {collection_name}: {str(e)}")
            return False

    async def retrieve_memory(self, collection_name: str, query_embedding: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        try:
            collection = Collection(collection_name)
            collection.load()
            search_params = {
                "metric_type": "L2",
                "params": {"nprobe": 10},
            }
            results = collection.search(
                data=[query_embedding],
                anns_field="vector",
                param=search_params,
                limit=top_k,
                output_fields=["text"]
            )
            logger.info(f"Searching collection {collection_name} with query embedding of length {len(query_embedding)}")
            logger.info(f"Search params: {search_params}")
            logger.info(f"Raw search results: {results}")
            logger.info(f"Search results for collection {collection_name}: {results}")
            if not results or not results[0]:
                logger.warning(f"No results found for query in collection {collection_name}")
                return []
            memories = [{"text": hit.entity.get("text", ""), "distance": hit.distance} for hit in results[0]]
            logger.info(f"Retrieved memories from collection {collection_name}: {memories}")
            return memories
        except Exception as e:
            logger.error(f"Error retrieving memory from collection {collection_name}: {str(e)}")
            return []

    async def delete_or_recreate_collection(self, collection_name: str):
        if self.milvus_client:
            if self.milvus_client.has_collection(collection_name):
                self.milvus_client.drop_collection(collection_name)

    async def update_memory(self, collection_name: str, updated_memory: Dict[str, Any]):
        if self.milvus_client:
            self.milvus_client.upsert(collection_name, [updated_memory])

    async def delete_memory(self, collection_name: str, memory_id: str):
        if self.milvus_client:
            self.milvus_client.delete(collection_name, expr=f"id == {memory_id}")

    async def create_index(self, collection_name: str, field_name: str, index_params: dict):
        try:
            collection = self.get_collection(collection_name)
            collection.create_index(field_name, index_params)
            logger.info(f"Created index on collection {collection_name}, field {field_name}")
        except Exception as e:
            logger.error(f"Failed to create index on collection {collection_name}: {str(e)}")
            raise

    async def load_collection(self, collection_name: str):
        self.ensure_connection()
        try:
            collection = Collection(collection_name)
            await collection.load()
            logger.info(f"Collection {collection_name} loaded successfully")
        except Exception as e:
            logger.error(f"Error loading collection {collection_name}: {str(e)}")
            raise

    async def get_collection_size(self, collection_name: str) -> int:
        try:
            collection = Collection(collection_name)
            return collection.num_entities
        except Exception as e:
            logger.error(f"Error getting collection size: {str(e)}")
            return 0

    async def drop_collection(self, collection_name: str) -> bool:
        try:
            utility.drop_collection(collection_name)
            logger.info(f"Collection {collection_name} dropped successfully")
            return True
        except Exception as e:
            logger.error(f"Error dropping collection {collection_name}: {str(e)}")
            return False

    def get_collection(self, collection_name: str):
        # Implement this method
        pass

    def ensure_connection(self):
        # Implement this method
        pass

    def get_collection_schema(self, collection_name: str):
        # Implement this method
        pass