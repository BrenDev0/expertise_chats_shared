import logging
from typing import List
import os
from qdrant_client import QdrantClient
from expertise_chats.llm.domain.repositories.vector_repository import VectorRepository
from expertise_chats.llm.domain.entities import SearchResult
logger = logging.getLogger(__name__)


class QdrantVectorRepository(VectorRepository):
    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
            https=True
        )
        
    async def similarity_search(
        self, 
        namespace: str,
        query_vector: List[float], 
        top_k: int = 4
    ) -> List[SearchResult]:
        results = self.client.query_points(
            collection_name=namespace,
            query=query_vector,
            limit=top_k,
            with_payload=True
        )
        
        return [
            SearchResult(
                id=point.id,
                score=point.score,
                payload=point.payload,
                text=point.payload.get("text"),
                metadata=point.payload.get("metadata") 
            )
            for point in results.points
        ]