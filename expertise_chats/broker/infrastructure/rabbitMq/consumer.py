import logging 
import json
import asyncio
from typing import Union, Dict, Any
from expertise_chats.broker.domain.consumer import Consumer
from expertise_chats.broker.domain.event_handler import EventHandler, AsyncEventHandler
from expertise_chats.broker.infrastructure.rabbitMq.connection import RabbitMqConnection
logger = logging.getLogger(__name__)

class RabbitMqConsumer(Consumer):
    def __init__(self, queue_name, handler: Union[EventHandler, AsyncEventHandler]):
        self._queue_name = queue_name
        self._event_handler = handler
        self._channel = RabbitMqConnection.get_channel()


    def start(self):
        assert self._queue_name, "queue_name must be defined in subclass"

        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(
            queue=self._queue_name,
            on_message_callback=self._handle_message
        )

        logger.info(f"Listening on queue: {self._queue_name}")
        self._channel.start_consuming()

    def _handle_message(
        self,
        ch,
        method,
        properties,
        body
    ):
        try: 
            payload = json.loads(body)
            
            if isinstance(self._event_handler, AsyncEventHandler):
                asyncio.run(self.handle_async(payload))

            else: 
                self.handle(payload)

            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        except Exception as e:
            logger.error(f"Error handling task in queue {self._queue_name} : {method.delivery_tag}::::::::::::{e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        
    def handle(self, payload: Dict[str, Any]):
        self._event_handler.handle(payload)
    
    async def handle_async(self, payload: Dict[str, Any]):
        await self._event_handler.handle(payload)

    