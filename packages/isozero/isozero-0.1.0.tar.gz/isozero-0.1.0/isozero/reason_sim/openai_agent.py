from openai import OpenAI
from typing import Dict, Any, List
import logging

class OpenAIAgent:
    """
    An agent that uses OpenAI's GPT models for reasoning and question answering tasks.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        """
        Initialize the OpenAIAgent with an API key and model choice.
        
        Args:
            api_key (str): The OpenAI API key.
            model (str): The OpenAI model to use. Default is "gpt-4o-mini".
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.logger = logging.getLogger(__name__)
    
    def run(self, agent_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the agent on the given input.
        
        Args:
            agent_input (Dict[str, Any]): A dictionary containing the input for the agent.
        
        Returns:
            Dict[str, Any]: A dictionary containing the agent's output.
        """
        try:
            text_data = agent_input['text']
            prompt = self._create_prompt(text_data)
            response = self._get_openai_response(prompt)
            return self._parse_response(response, text_data['step'])
        except KeyError as e:
            self.logger.error(f"Missing key in agent_input: {e}")
            raise ValueError(f"Invalid agent_input: {e}")
        except Exception as e:
            self.logger.error(f"Error in run method: {e}")
            raise
    
    def _create_prompt(self, text_data: Dict[str, Any]) -> str:
        """
        Create a prompt for the OpenAI model based on the text data.
        
        Args:
            text_data (Dict[str, Any]): A dictionary containing the input text data.
        
        Returns:
            str: The formatted prompt for the OpenAI model.
        """
        task = text_data.get('task') or text_data.get('question', '')
        step = text_data.get('step', 0)
        reasoning = text_data.get('reasoning', [])
        max_steps = text_data.get('max_steps', 3)
        
        reasoning_text = "; ".join(reasoning) if reasoning else "No previous reasoning."
        
        if step < max_steps - 1:
            return f"""
            Task or Question: {task}
            
            Previous reasoning steps:
            {reasoning_text}
            
            You are on step {step + 1} of {max_steps} in the reasoning process.
            Provide the next step of reasoning to solve this task or answer this question.
            Focus on analyzing the given information and building upon previous steps.
            """
        else:
            return f"""
            Task or Question: {task}
            
            Previous reasoning steps:
            {reasoning_text}
            
            Based on your reasoning, provide the final solution or answer.
            Be concise and direct in your response.
            """
    
    def _get_openai_response(self, prompt: str) -> str:
        """
        Get a response from the OpenAI model.
        
        Args:
            prompt (str): The prompt to send to the OpenAI model.
        
        Returns:
            str: The response from the OpenAI model.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI assistant specialized in solving reasoning tasks through careful analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.logger.error(f"Error in OpenAI API call: {e}")
            raise
    
    def _parse_response(self, response: str, step: int) -> Dict[str, Any]:
        """
        Parse the response from the OpenAI model.
        
        Args:
            response (str): The response from the OpenAI model.
            step (int): The current step in the reasoning process.
        
        Returns:
            Dict[str, Any]: A dictionary containing the parsed response.
        """
        if step < 3:
            return {"text_data": {"reasoning": response}}
        else:
            return {"text_data": {"solution": response}}