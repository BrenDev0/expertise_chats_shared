from expertise_chats.broker.domain.interaction_event import InteractionEvent
from expertise_chats.schemas.ws import WsPayload
from expertise_chats.broker.domain.producer import Producer


class HandleChunk:
    def __init__(
        self,
        producer: Producer
    ):
        self.__producer = producer

    def execute(
        self,
        sentence: str,
        chunk: str,
        event: InteractionEvent
    ):
        if event.voice:
            sentence += chunk
            # Check for sentence-ending punctuation
            if any(p in chunk for p in [".", "?", "!"]) and len(sentence) > 10:
                ws_payload = WsPayload(
                    type="AUIDO",
                    data=sentence.strip()
                )

                event.event_data =ws_payload.model_dump()

                self.__producer.publish(
                    routing_key=f"streaming.audio.outbound.send",
                    event_message=event
                )

                sentance = ""
            return sentance
        else:
            ws_payload = WsPayload(
                type="TEXT",
                data=chunk
            )

            event.event_data =ws_payload.model_dump()

            self.__producer.publish(
                routing_key=f"streaming.general.outbound.send",
                event_message=event
            )
            return ""