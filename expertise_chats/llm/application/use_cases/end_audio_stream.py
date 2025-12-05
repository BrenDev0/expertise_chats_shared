from  expertise_chats.broker.domain.interaction_event import InteractionEvent
from expertise_chats.schemas.ws import WsPayload
from expertise_chats.broker.domain.producer import Producer

class EndAudioStream:
    def __init__(
        self,
        producer: Producer
    ):
        self.__producer = producer

    def execute(
        self,
        sentence: str,
        event: InteractionEvent
    ):
        ws_payload = WsPayload(
            type="AUIDO",
            data=sentence.strip()
        )

        event.event_data =ws_payload.model_dump()

        self.__producer.publish(
            routing_key=f"streaming.audio.outbound.send",
            event_message=event
        )

        ws_payload.type = "END"
        ws_payload.data = "END STREAM"

        event.event_data = ws_payload.model_dump()

        self.__producer.publish(
            routing_key=f"streaming.general.outbound.send",
            event_message=event
        )