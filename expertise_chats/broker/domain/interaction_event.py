from expertise_chats.broker.domain.base_event import BaseEvent

class InteractionEvent(BaseEvent):
    user_id: str
    company_id: str
    agent_id: str
    voice: bool = False