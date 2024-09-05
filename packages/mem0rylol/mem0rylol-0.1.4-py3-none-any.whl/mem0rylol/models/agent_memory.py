# models/agent_memory.py
from typing import Dict, List, Union, Optional
from .memory_model import MemoryModel

class AgentMemory:
    def __init__(self, memory_model):
        self.memory_model = memory_model
        self.memory = {}  # Initialize the memory attribute

    async def update_memory(self, agent_id: str, data: Dict[str, Union[str, int, float, List[float]]]):
        collection_name = f"agent_{agent_id}_memory"
        await self.memory_model.store_memory(collection_name, data)

    async def get_memory(self, agent_id: str, query: str, top_k: int = 5, similarity_threshold: float = 0.95):
        collection_name = f"agent_{agent_id}_memory"
        memories = await self.memory.retrieve_memory(collection_name, query, top_k, similarity_threshold)
        return memories

    async def create_agent_memory(self, agent_id: str, schema: Dict[str, Union[str, int]]):
        collection_name = f"agent_{agent_id}_memory"
        await self.memory.create_collection(collection_name, schema)

    async def delete_agent_memory(self, agent_id: str, recreate: bool = False, new_schema: Optional[Dict[str, Union[str, int]]] = None):
        collection_name = f"agent_{agent_id}_memory"
        await self.memory.delete_or_recreate_collection(collection_name, recreate, new_schema)