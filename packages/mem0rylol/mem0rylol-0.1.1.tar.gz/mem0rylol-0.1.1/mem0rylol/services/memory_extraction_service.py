from mem0rylol.models.extracted_memory import ExtractedMemory
from typing import List, Dict, Any, Optional
import asyncio
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from pydantic import BaseModel

class MemoryExtractionService:
    def __init__(self, config, langchain_client):
        self.config = config
        self.langchain_client = langchain_client
        self.llm = self.langchain_client["llm"]
        self.embeddings = self.langchain_client["embeddings"]
        self.prompt = PromptTemplate(
            input_variables=["input", "metadata"],
            template=self._generate_extraction_prompt_template()
        )
        self.chain = (
            {"input": RunnablePassthrough(), "metadata": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    async def extract_and_embed_memories(
        self,
        user_id: str,
        session_id: str,
        input_text: str,
        metadata: Optional[Dict[Any, Any]] = None
    ) -> Any:
        extracted_memories = await self._extract_memories(input_text, metadata or {})
        embedded_memories = await self._embed_memories(extracted_memories)
        return ExtractedMemory(user_id=user_id, session_id=session_id, memories=embedded_memories)

    async def _extract_memories(self, input_text: str, metadata: dict) -> List[str]:
        extracted_memories = await self.chain.ainvoke({"input": input_text, "metadata": metadata})
        return extracted_memories.split("\n")

    async def _embed_memories(self, memories: List[str]) -> List[Dict[str, Any]]:
        embeddings = await asyncio.gather(*[self.embeddings.aembed_query(memory) for memory in memories])
        return [{"text": memory, "vector": embedding} for memory, embedding in zip(memories, embeddings)]

    def _generate_extraction_prompt_template(self) -> str:
        return """
        Deduce the facts, preferences, and memories from the provided text.
        Just return the facts, preferences, and memories in bullet points:
        Natural language text: {input}
        User/Agent details: {metadata}
        Constraint for deducing facts, preferences, and memories:
        - The facts, preferences, and memories should be concise and informative.
        - Don't start by "The person likes Pizza". Instead, start with "Likes Pizza".
        - Don't remember the user/agent details provided. Only remember the facts, preferences, and memories.
        Deduced facts, preferences, and memories:
        """

    async def _process_with_llm(self, prompt: str) -> List[str]:
        response = await self.langchain_client["chain"].arun(prompt)
        return [memory.strip() for memory in response.split('\n') if memory.strip()]