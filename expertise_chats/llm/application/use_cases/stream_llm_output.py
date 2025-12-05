from expertise_chats.llm.domain.services.llm_service import LlmService
from expertise_chats.llm.application.use_cases.handle_chunk import HandleChunk
from expertise_chats.llm.application.use_cases.end_audio_stream import EndAudioStream
from expertise_chats.broker.domain.interaction_event import InteractionEvent
from expertise_chats.broker.domain.producer import Producer


class StreamLlmOutput:
    def __init__(
        self,
        llm_service: LlmService,
        chunk_hander: HandleChunk,
        end_audio_stream: EndAudioStream,
        producer: Producer
    ):
        self.__llm_service = llm_service
        self.__chunk_handler = chunk_hander
        self.__end_audio_stream = end_audio_stream
        self.__producer = producer

    async def execute(
        self,
        prompt:str,
        event: InteractionEvent,
        temperature: float = 0.0
       
    ):
        chunks = []
        sentence = "" 
        async for chunk in self.__llm_service.generate_stream(
            prompt=prompt,
            temperature=temperature
        ):
            chunks.append(chunk)
            sentence = self.__chunk_handler.execute(
                sentence=sentence,
                chunk=chunk,
                event=event
            )

        # After streaming all chunks, send any remaining text for voice
        if event.voice and sentence.strip():
            self.__end_audio_stream.execute(
                sentence=sentence,
                event=event
            )
        
        self.__producer.publish(
            routing_key="messages.outgoing.send",
            event_message={
                "llm_response": "".join(chunks)
            }
        )

        return "".join(chunks)