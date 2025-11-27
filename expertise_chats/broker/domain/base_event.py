from pydantic import BaseModel
from  typing import Dict, Any 

class BaseEvent(BaseModel):
    chat_id: str
    user_id: str
    event_data: Dict[str, Any]