from expertise_chats.broker.domain.interaction_event import InteractionEvent
from expertise_chats.schemas.ws import WsPayload
from expertise_chats.broker.domain.producer import Producer
from expertise_chats.llm.domain.schemas import LlmMessageEvent


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
        agent_id = event.agent_id
        event_data = LlmMessageEvent(**event.event_data)
        message_id = event_data.chat_history[0].message_id

        if event.voice:
            sentence += chunk
            # Check for sentence-ending punctuation
            if any(p in chunk for p in [".", "?", "!"]) and len(sentence) > 10:
                ws_payload = WsPayload(
                    agent_id=str(agent_id),
                    message_id=str(message_id),
                    type="AUDIO",
                    data=sentence.strip()
                )

                event.event_data =ws_payload.model_dump()

                self.__producer.publish(
                    routing_key=f"streaming.audio.outbound.send",
                    event_message=event
                )

                sentence = ""
            return sentence
        else:
            ws_payload = WsPayload(
                agent_id=str(agent_id),
                message_id=str(message_id),
                type="TEXT",
                data=chunk
            )

            event.event_data = ws_payload.model_dump()

            self.__producer.publish(
                routing_key=f"streaming.general.outbound.send",
                event_message=event
            )
            return ""