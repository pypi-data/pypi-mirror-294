# services/agent_service.py
import logging
from mem0rylol.models.agent_memory import AgentMemory
from mem0rylol.services.memory_service import MemoryService  # Move this import to the end of the file
from typing import Optional
from mem0rylol.utils.logger import logger

class AgentService:
    def __init__(self, config, langchain_client, memory_model, memory_service):
        self.config = config
        self.langchain_client = langchain_client
        self.memory_model = memory_model
        self.memory_service = memory_service
        self.agent_memory = AgentMemory(memory_model)  # Add this line

    async def process_agent_request(self, user_id: str, session_id: str, request: str) -> str:
        try:
            memories = await self.memory_service.retrieve_memory(user_id, session_id, request)
            if memories is None or len(memories) == 0:
                return "I don't have any relevant information to answer that question."
            
            # Process the request using the retrieved memories
            context = "\n".join([memory['text'] for memory in memories])
            prompt = f"""
            Based on the following context and the user's request, provide a relevant and concise response:

            Context:
            {context}

            User Request: {request}

            Response:
            """
            
            response = await self.langchain_client["chain"].ainvoke({"input": prompt})
            answer = response.content if hasattr(response, 'content') else str(response)
            
            # Update the agent's memory with the new interaction
            await self.memory_service.process_and_store_memory(
                user_id,
                session_id,
                f"User asked: {request}\nAgent responded: {answer}"
            )
            
            return answer
        except Exception as e:
            logger.error(f"Error processing request for agent {user_id}_{session_id}: {str(e)}")
            return "I'm sorry, but I encountered an error while processing your request."

    async def create_agent(self, user_id: str, session_id: str):
        try:
            # Create agent memory collection
            await self.memory_service.create_user_memory_collection(user_id, session_id)
            
            # Rest of the method implementation...
        except Exception as e:
            logger.error(f"Error creating agent memory collection: {str(e)}")
            raise

    async def delete_agent(self, agent_id: str):
        await self.agent_memory.delete_agent_memory(agent_id)