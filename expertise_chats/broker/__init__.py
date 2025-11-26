# expertise_chats/broker/__init__.py
"""
Message broker package for expertise_chats.
"""

from expertise_chats.broker.infrastructure.rabbitMq.connection import RabbitMqConnection as BrokerConnection
from expertise_chats.broker.infrastructure.rabbitMq.consumer import RabbitMqConnection as Consumer
from expertise_chats.broker.infrastructure.rabbitMq.producer import RabbitMqProducer as Producer
from expertise_chats.broker.domain.event_handler import EventHandler, AsyncEventHandler

# Re-export the main classes users need
__all__ = [
   "BrokerConnection",
   "Consumer",
   "Producer",
   "EventHandler",
   "AsyncEventHandler"
]