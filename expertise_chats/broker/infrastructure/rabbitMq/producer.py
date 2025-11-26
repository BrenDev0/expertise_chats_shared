import json 
from pydantic import BaseModel
from typing import Dict, Any, Union
import pika
import logging

from expertise_chats.broker.infrastructure.rabbitMq.connection import RabbitMqConnection

logger = logging.getLogger(__name__)

class RabbitMqProducer:
    def __init__(self, exchange: str):
        self.__exchange = exchange

    def publish(
        self,
        routing_key: str,
        event_message: Union[BaseModel, Dict[str, Any], str],
    ): 
        channel = RabbitMqConnection.get_channel()

        if isinstance(event_message, BaseModel):
            body = event_message.model_dump_json()
        elif isinstance(event_message, dict):  
            body = json.dumps(event_message)
        else:
            body = str(event_message)

        channel.basic_publish(
            exchange=self.__exchange,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )