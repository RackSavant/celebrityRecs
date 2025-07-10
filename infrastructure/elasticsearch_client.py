from elasticsearch import Elasticsearch
from typing import Dict, Any, List
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class ElasticsearchClient:
    """Client for interacting with Elasticsearch."""
    
    def __init__(self):
        self.client = Elasticsearch(settings.elasticsearch_url)
        self.index_name = "fashion-items"
        
    def create_index(self) -> bool:
        """Create Elasticsearch index with mapping."""
        mapping = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "name": {"type": "text"},
                    "description": {"type": "text"},
                    "styles": {"type": "keyword"},
                    "brand": {"type": "keyword"},
                    "category": {"type": "keyword"},
                    "size": {"type": "keyword"},
                    "color": {"type": "keyword"},
                    "price": {"type": "float"},
                    "image_url": {"type": "text"},
                    "timestamp": {"type": "date"}
                }
            }
        }
        
        try:
            if not self.client.indices.exists(index=self.index_name):
                self.client.indices.create(index=self.index_name, body=mapping)
            return True
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            return False
    
    def index_item(self, item: Dict[str, Any]) -> bool:
        """Index a fashion item."""
        try:
            self.client.index(
                index=self.index_name,
                id=item["id"],
                body=item,
                refresh=True
            )
            return True
        except Exception as e:
            logger.error(f"Error indexing item: {e}")
            return False
    
    def search_items(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search for fashion items."""
        try:
            response = self.client.search(
                index=self.index_name,
                body=query
            )
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except Exception as e:
            logger.error(f"Error searching items: {e}")
            return []
