from .base_agent import BaseAgent, AgentContext
from typing import Dict, Any
from langchain import BaseLanguageModel
from langchain.prompts import PromptTemplate

class StyleClassificationAgent(BaseAgent):
    """Agent specialized in classifying fashion styles."""
    
    def __init__(self, llm: BaseLanguageModel, context: AgentContext):
        super().__init__(llm, context)
        self.prompt_template = PromptTemplate(
            input_variables=["description", "image_url"],
            template="""Given the following fashion item description and image URL, classify the style into one or more categories:
            {description}
            Image URL: {image_url}
            
            Return the classification in JSON format with the following structure:
            {"styles": ["style1", "style2", ...], "confidence": 0.0-1.0}"""
        )
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Classify the fashion item's style."""
        prompt = self.prompt_template.format(
            description=input_data.get("description", ""),
            image_url=input_data.get("image_url", "")
        )
        
        result = self.llm.predict(prompt)
        return self._parse_result(result)
    
    def get_agent_type(self) -> str:
        return "style_classification"
    
    def _parse_result(self, result: str) -> Dict[str, Any]:
        """Parse the LLM's response into a structured format."""
        try:
            import json
            return json.loads(result)
        except json.JSONDecodeError:
            return {"styles": [], "confidence": 0.0}
