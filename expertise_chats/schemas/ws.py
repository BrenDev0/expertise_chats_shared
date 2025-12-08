from pydantic import BaseModel
from typing import Union, Dict, Any, Optional

class RequestErrorBase(BaseModel):
    error: str
    detail: str
    additional_info: Optional[Union[str, Dict[str, Any]]] = None

class WsPayload(BaseModel):
    message_id: Optional[str] = None
    type: str
    data: Union[str, Dict[str, Any]]