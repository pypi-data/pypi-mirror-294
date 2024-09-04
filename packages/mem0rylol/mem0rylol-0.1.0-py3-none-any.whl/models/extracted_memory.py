from pydantic import BaseModel
from typing import List, Dict, Any

class ExtractedMemory(BaseModel):
    user_id: str
    session_id: str
    memories: List[Dict[str, Any]]