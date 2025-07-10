from abc import ABC, abstractmethod
from typing import Dict, Any, List
from langchain import BaseLanguageModel
from pydantic import BaseModel

class AgentContext(BaseModel):
    """Context information available to all agents."""
    user_profile: Dict[str, Any]
    conversation_history: List[Dict[str, str]]
    current_state: Dict[str, Any]

class BaseAgent(ABC):
    """Base class for all fashion recommendation agents."""
    
    def __init__(self, llm: BaseLanguageModel, context: AgentContext):
        self.llm = llm
        self.context = context
    
    @abstractmethod
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the input data and return results."""
        pass
    
    @abstractmethod
    def get_agent_type(self) -> str:
        """Return the type of agent."""
        pass
