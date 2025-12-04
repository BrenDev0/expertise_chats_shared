from typing import Union, Optional
from expertise_chats.broker import Producer, InteractionEvent, BaseEvent
from expertise_chats.schemas.ws import WsPayload
from expertise_chats.schemas.ws import RequestErrorBase


def handle_error(
    event: Union[BaseEvent, InteractionEvent],
    producer: Producer,
    server_error: bool = False,
    error: Optional[RequestErrorBase] = None,
):
    if server_error or not error:
        error = RequestErrorBase(
            error="Internal Server Error",
            detail="Unable to process request at this time"
        )
    

    ws_payload = WsPayload(
        type="ERROR",
        data=error.model_dump()
    )

    event.event_data = ws_payload

    producer.publish(
        routing_key="streaming.general.outbound.send",
        event_message=event
    )

    return 