import pinecone
from typing import Dict, List, Any, Optional
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    """Vector store implementation using Pinecone."""
    
    def __init__(self):
        pinecone.init(
            api_key=settings.pinecone_api_key,
            environment=settings.pinecone_environment
        )
        self.index_name = settings.vector_store_index
        
    def create_index(self) -> bool:
        """Create Pinecone index if it doesn't exist."""
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                self.index_name,
                dimension=settings.vector_store_dimension,
                metric="cosine"
            )
        return True
    
    def upsert(self, vectors: List[Dict[str, Any]]) -> bool:
        """Upsert vectors into the index."""
        try:
            pinecone_index = pinecone.Index(self.index_name)
            pinecone_index.upsert(vectors)
            return True
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            return False
    
    def similarity_search(self, query_vector: List[float], k: int = 5) -> List[Dict[str, Any]]:
        """Perform similarity search."""
        try:
            pinecone_index = pinecone.Index(self.index_name)
            results = pinecone_index.query(
                vector=query_vector,
                top_k=k,
                include_metadata=True
            )
            return results["matches"]
        except Exception as e:
            logger.error(f"Error performing similarity search: {e}")
            return []
