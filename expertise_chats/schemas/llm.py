from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID
from expertise_chats.llm.domain.entities import Message

class InteractionRequest(BaseModel):
    input: str
    chat_id: UUID
    company_id: UUID
    chat_history: List[Dict[str, Any]]
    user_id: UUID
    voice: Optional[bool] = False

class LlmResponse(BaseModel):
    response: str
    data: Optional[Any] = None


class IncommingMessageEvent(BaseModel):
    chat_history: List[Message]