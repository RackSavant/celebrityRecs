from .base_agent import BaseAgent, AgentContext
from typing import Dict, Any
from langchain import BaseLanguageModel
from langchain.prompts import PromptTemplate

class PersonalizationAgent(BaseAgent):
    """Agent specialized in generating personalized fashion recommendations."""
    
    def __init__(self, llm: BaseLanguageModel, context: AgentContext):
        super().__init__(llm, context)
        self.prompt_template = PromptTemplate(
            input_variables=["user_profile", "recent_interactions", "current_context"],
            template="""Given the user's profile, recent interactions, and current context,
            generate personalized fashion recommendations:
            
            User Profile:
            {user_profile}
            
            Recent Interactions:
            {recent_interactions}
            
            Current Context:
            {current_context}
            
            Return recommendations in JSON format with the following structure:
            {"recommendations": [
                {"item_id": "", "reason": "", "confidence": 0.0-1.0}
            ]}"""
        )
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized recommendations."""
        prompt = self.prompt_template.format(
            user_profile=self.context.user_profile,
            recent_interactions=self.context.conversation_history[-3:],  # Last 3 interactions
            current_context=input_data.get("context", "")
        )
        
        result = self.llm.predict(prompt)
        return self._parse_result(result)
    
    def get_agent_type(self) -> str:
        return "personalization"
    
    def _parse_result(self, result: str) -> Dict[str, Any]:
        """Parse the LLM's response into a structured format."""
        try:
            import json
            return json.loads(result)
        except json.JSONDecodeError:
            return {"recommendations": []}
