# services/memory_service.py
from mem0rylol.utils.logger import logger
from mem0rylol.models.memory_model import MemoryModel
from mem0rylol.services.memory_extraction_service import MemoryExtractionService
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
        self.memory_model = MemoryModel(config)
        self.milvus_client = config.get_milvus_client()  # Add this line

    async def initialize(self):
        self.memory_model.initialize()
        # Add any additional async initialization if needed

    async def process_and_store_memory(
        self,
        user_id: str,
        session_id: str,
        input_text: str,
        metadata: Optional[Dict[Any, Any]] = None
    ) -> Any:
        if not await self.create_user_memory_collection(user_id, session_id):
            logger.error(f"Failed to create or ensure collection for user {user_id} and session {session_id}")
            return None
        
        extracted_memory = await self.memory_extraction_service.extract_and_embed_memories(user_id, session_id, input_text, metadata)
        
        for memory in extracted_memory.memories:
            await self._process_single_memory(user_id, session_id, memory)
        
        return extracted_memory

    async def store_user_memory(self, user_id: str, session_id: str, memory_text: str) -> bool:
        collection_name = self._get_collection_name(user_id, session_id)
        try:
            logger.info(f"Attempting to store memory in collection: {collection_name}")
            if not await self.ensure_collection_exists(user_id, session_id):
                raise Exception("Failed to create or ensure collection exists")

            logger.info("Generating embedding for memory text")
            embedding = await self.langchain_client["embeddings"].aembed_query(memory_text)
            
            memory = {"text": memory_text, "vector": embedding}
            logger.info(f"Storing memory: {memory_text[:50]}...")
            result = await self.memory_model.store_memory(collection_name, memory)
            logger.info(f"Memory stored: {result}, Collection: {collection_name}")
            logger.info(f"Memory stored result: {result}")
            logger.info(f"Collection name: {collection_name}")
            logger.info(f"Memory text: {memory_text}")
            logger.info(f"Embedding length: {len(embedding)}")
            return result
        except Exception as e:
            logger.error(f"Error storing user memory: {str(e)}")
            logger.exception("Detailed traceback:")
            return False

    async def retrieve_memories(self, user_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        session_id = "default"  # You might want to handle session_id differently
        collection_name = self._get_collection_name(user_id, session_id)
        try:
            logger.info(f"Attempting to retrieve memories from collection: {collection_name}")
            logger.info(f"Query: {query}")
            
            query_embedding = await self.langchain_client["embeddings"].aembed_query(query)
            
            retrieved_memories = await self.memory_model.retrieve_memory(collection_name, query_embedding, top_k)
            logger.info(f"Retrieved {len(retrieved_memories)} memories")
            logger.info(f"Retrieved memories: {retrieved_memories}")
            return retrieved_memories
        except Exception as e:
            logger.error(f"Error retrieving memories: {str(e)}")
            logger.exception("Detailed traceback:")
            return []

    async def _update_existing_memories(self, new_memory: Dict[str, Any], similar_memories: List[Dict[str, Any]]) -> Dict[str, Any]:
        prompt = self._generate_update_prompt(new_memory, similar_memories)
        updated_memory = await self._process_update_with_llm(prompt)
        return updated_memory

    def _generate_update_prompt(self, new_memory: Dict[str, Any], similar_memories: List[Dict[str, Any]]) -> str:
        existing_memories = "\n".join([f"- {memory['text']} (Similarity: {memory['distance']})" for memory in similar_memories])
        prompt = f"""
        You are an expert at merging, updating, and organizing memories. When provided with existing memories and new information, your task is to merge and update the memory list to reflect the most accurate and current information. You are also provided with the matching score for each existing memory to the new information. Make sure to leverage this information to make informed decisions about which memories to update or merge.
        Guidelines:
        - Eliminate duplicate memories and merge related memories to ensure a concise and updated list.
        - If a memory is directly contradicted by new information, critically evaluate both pieces of information:
            - If the new memory provides a more recent or accurate update, replace the old memory with new one.
            - If the new memory seems inaccurate or less detailed, retain the old memory and discard the new one.
        - Maintain a consistent and clear style throughout all memories, ensuring each entry is concise yet informative.
        - If the new memory is a variation or extension of an existing memory, update the existing memory to reflect the new information.
        Here are the details of the task:
        - Existing Memories:
        {existing_memories}
        - New Memory: {new_memory['text']}
        
        Updated memory:
        """
        return prompt

    async def _process_update_with_llm(self, prompt: str) -> Dict[str, Any]:
        response = await self.langchain_client["chain"].ainvoke({"input": prompt})
        updated_text = response.content if hasattr(response, 'content') else str(response)
        updated_embedding = await self.langchain_client["embeddings"].aembed_query(updated_text)
        return {
            "text": updated_text,
            "vector": updated_embedding
        }

    async def create_user_memory_collection(self, user_id: str, session_id: str) -> bool:
        try:
            await self.initialize()  # Ensure the MemoryModel is initialized
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
            raise Exception("Failed to create user memory collection") from e

    async def delete_user_memory_collection(self, user_id: str, session_id: str) -> bool:
        collection_name = self._get_collection_name(user_id, session_id)
        try:
            if await self.memory_model.has_collection(collection_name):
                result = await self.memory_model.drop_collection(collection_name)
                logger.info(f"Deleted collection {collection_name}")
                return result
            else:
                logger.info(f"Collection {collection_name} does not exist")
                return True
        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            return False

    async def generate_memory_based_response(self, user_id: str, session_id: str, query: str, top_k: int = 5) -> str:
        # Step 1: Retrieve relevant memories
        relevant_memories = await self.retrieve_relevant_memories(user_id, session_id, query, top_k)

        # Step 2: Generate response using the prompt and relevant memories
        response = await self._generate_response(query, relevant_memories)

        return response

    async def retrieve_relevant_memories(self, user_id: str, session_id: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        collection_name = f"user_{user_id}_session_{session_id}"
        query_embedding = await self.langchain_client["embeddings"].aembed_query(query)
        memories = await self.memory_model.retrieve_memory(collection_name, query_embedding, top_k)
        return memories

    async def _generate_response(self, query: str, relevant_memories: List[Dict[str, Any]]) -> str:
        prompt = self._create_response_prompt(query, relevant_memories)
        response = await self.langchain_client["chain"].ainvoke({"input": prompt})
        return response.content if hasattr(response, 'content') else str(response)

    def _create_response_prompt(self, query: str, relevant_memories: List[Dict[str, Any]]) -> str:
        memories_text = "\n".join([f"- {memory['text']}" for memory in relevant_memories])
        prompt = f"""
        You are an expert at answering questions based on the provided memories. Your task is to provide accurate and concise answers to the questions by leveraging the information given in the memories.
        Guidelines:
        - Extract relevant information from the memories based on the question.
        - If no relevant information is found, make sure you don't say no information is found. Instead, accept the question and provide a general response.
        - Ensure that the answers are clear, concise, and directly address the question.
        Here are the details of the task:

        Question: {query}

        Relevant Memories:
        {memories_text}

        Please provide a response based on the question and the relevant memories:
        """
        return prompt

    async def _process_single_memory(self, user_id: str, session_id: str, memory: Dict[str, Any]):
        collection_name = f"user_{user_id}_session_{session_id}"
        try:
            similar_memories = await self.memory_model.retrieve_memory(collection_name, memory['vector'], top_k=5)
            if similar_memories:
                updated_memory = await self._update_existing_memories(memory, similar_memories)
                await self.memory_model.store_memory(collection_name, updated_memory)
            else:
                await self.memory_model.store_memory(collection_name, memory)
        except Exception as e:
            logger.error(f"Error processing single memory: {str(e)}")
            raise

    async def delete_or_recreate_collection(self, user_id: str, session_id: str) -> bool:
        collection_name = f"user_{user_id}_session_{session_id}"
        try:
            if await self.memory_model.has_collection(collection_name):
                await self.memory_model.drop_collection(collection_name)
            return await self.create_user_memory_collection(user_id, session_id)
        except Exception as e:
            logger.error(f"Error deleting or recreating collection: {str(e)}")
            raise

    async def ensure_collection_exists(self, user_id: str, session_id: str) -> bool:
        collection_name = f"user_{user_id}_session_{session_id}"
        try:
            if not await self.memory_model.has_collection(collection_name):
                schema = self._create_collection_schema()
                return await self.memory_model.create_collection(collection_name, schema)
            return True
        except Exception as e:
            logger.error(f"Error ensuring collection exists: {str(e)}")
            raise

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

    async def get_collection_size(self, user_id: str, session_id: str) -> int:
        collection_name = self._get_collection_name(user_id, session_id)
        return await self.memory_model.get_collection_size(collection_name)

    async def has_user_memory_collection(self, user_id: str, session_id: str) -> bool:
        collection_name = self._get_collection_name(user_id, session_id)
        return await self.memory_model.has_collection(collection_name)

    async def check_collection_status(self, user_id: str, session_id: str):
        collection_name = self._get_collection_name(user_id, session_id)
        try:
            exists = await self.memory_model.has_collection(collection_name)
            logger.info(f"Collection {collection_name} exists: {exists}")
            if exists:
                size = await self.memory_model.get_collection_size(collection_name)
                logger.info(f"Collection {collection_name} size: {size}")
                schema = await self.memory_model.get_collection_schema(collection_name)
                logger.info(f"Collection {collection_name} schema: {schema}")
        except Exception as e:
            logger.error(f"Error checking collection status: {str(e)}")
            logger.exception("Detailed traceback:")