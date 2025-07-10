from .base_agent import BaseAgent, AgentContext
from typing import Dict, Any
from langchain import BaseLanguageModel
from langchain.prompts import PromptTemplate

class ConversationAgent(BaseAgent):
    """Agent specialized in natural language conversations about fashion."""
    
    def __init__(self, llm: BaseLanguageModel, context: AgentContext):
        super().__init__(llm, context)
        self.prompt_template = PromptTemplate(
            input_variables=["history", "user_message"],
            template="""Given the following conversation history and user message, respond in a friendly and helpful manner:
            
            History:
            {history}
            
            User: {user_message}
            Assistant:"""
        )
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a conversation turn."""
        history = "\n".join(
            f"User: {msg['user']}\nAssistant: {msg['assistant']}"
            for msg in self.context.conversation_history[-5:]  # Last 5 messages
        )
        
        prompt = self.prompt_template.format(
            history=history,
            user_message=input_data.get("message", "")
        )
        
        response = self.llm.predict(prompt)
        return {"response": response}
    
    def get_agent_type(self) -> str:
        return "conversation"
