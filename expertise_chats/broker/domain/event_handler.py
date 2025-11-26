from abc import ABC, abstractmethod
from typing import Dict, Any

class EventHandler(ABC):
    @abstractmethod
    def handle(self, payload: Dict[str, Any]):
        raise NotImplementedError()
    
class AsyncEventHandler(ABC):
    @abstractmethod
    async def handle(self, payload: Dict[str, Any]):
        raise NotImplementedError()