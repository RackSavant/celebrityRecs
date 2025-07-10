import json
from typing import Dict, Any, List
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def generate_unique_id() -> str:
    """Generate a unique identifier for recommendations or sessions."""
    return str(uuid.uuid4())

def format_timestamp(timestamp: datetime) -> str:
    """Format datetime object to ISO string."""
    return timestamp.isoformat()

def validate_json(data: Any) -> bool:
    """Validate if data is a valid JSON object."""
    try:
        json.dumps(data)
        return True
    except (TypeError, ValueError):
        return False

def merge_dictionaries(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Merge multiple dictionaries into one."""
    result = {}
    for d in dicts:
        result.update(d)
    return result

def batch_process(items: List[Any], batch_size: int = 100) -> List[List[Any]]:
    """Process items in batches."""
    return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
