# main.py
import asyncio
from mem0rylol.config import get_config
from mem0rylol.services.memory_service import MemoryService
from mem0rylol.services.agent_service import AgentService
from mem0rylol.models.memory_model import MemoryModel
from mem0rylol.config.config import Config
from loguru import logger
from mem0rylol.models.agent_memory import AgentMemory
from mem0rylol.services.memory_extraction_service import MemoryExtractionService

config = Config()
langchain_client = config.get_langchain_client()
memory_model = MemoryModel(config)
memory_extraction_service = MemoryExtractionService(config, langchain_client)
memory_service = MemoryService(config, langchain_client, memory_extraction_service)
agent_memory = AgentMemory(memory_model)
agent_service = AgentService(
    config,
    langchain_client,
    memory_model,
    memory_service
)

async def setup_memory_layer():
    memory_service = MemoryService()
    return memory_service

async def setup_agent_service(config: Config, langchain_client, memory_model: MemoryModel, memory_service: MemoryService):
    agent_service = AgentService(config, langchain_client, memory_model, memory_service)
    return agent_service

async def main():
    memory_service = await setup_memory_layer()
    agent_service = await setup_agent_service(config, langchain_client, memory_model, memory_service)
    
    # Example usage
    try:
        user_id = "user123"
        session_id = "session456"
        
        # Create user memory collection
        await memory_service.create_user_memory_collection(user_id, session_id)
        
        # Process and store a memory
        input_text = "I love pizza and enjoy watching sci-fi movies."
        extracted_memory = await memory_service.process_and_store_memory(user_id, session_id, input_text)
        logger.info(f"Extracted and stored memory: {extracted_memory}")
        
        # Retrieve and generate a response based on stored memories
        query = "What are my food preferences?"
        response = await memory_service.generate_memory_based_response(user_id, session_id, query)
        logger.info(f"Generated response: {response}")
        
        # Create an agent
        agent_id = "agent789"
        await agent_service.create_agent(agent_id)
        
        # Process an agent request
        agent_request = "What do I like to eat?"
        agent_response = await agent_service.process_agent_request(agent_id, agent_request)
        logger.info(f"Agent response: {agent_response}")
        
    finally:
        # Ensure proper cleanup
        await memory_service.delete_user_memory_collection(user_id, session_id)
        await agent_service.delete_agent(agent_id)

if __name__ == "__main__":
    asyncio.run(main())