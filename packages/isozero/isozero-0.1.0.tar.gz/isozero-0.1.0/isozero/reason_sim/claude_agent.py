from anthropic import Anthropic
from typing import Dict, Any, List, Tuple
import logging

class ClaudeAgent:
    """
    A class representing an AI agent using Anthropic's Claude model for reasoning tasks.
    """

    def __init__(self, api_key: str, model: str = "claude-2"):
        """
        Initialize the ClaudeAgent.

        Args:
            api_key (str): The API key for authenticating with Anthropic's API.
            model (str, optional): The specific Claude model to use. Defaults to "claude-2".
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.is_claude_3 = model.startswith("claude-3")
        self.logger = logging.getLogger(__name__)

    def run(self, agent_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a reasoning step using the Claude model.

        This method takes the current state of the reasoning task, generates the next step
        or final solution using the Claude model, and returns the result.

        Args:
            agent_input (Dict[str, Any]): A dictionary containing the current state of the reasoning task.
                Expected keys are 'task', 'step', 'reasoning', and 'max_steps'.

        Returns:
            Dict[str, Any]: A dictionary containing either the next reasoning step or the final solution.
        """
        try:
            text_data = agent_input['text']
            task = text_data['task']
            step = text_data['step']
            reasoning = text_data['reasoning']
            max_steps = text_data['max_steps']

            prompt = self._create_prompt(task, step, reasoning, max_steps)
            
            response = self.client.completions.create(
                model=self.model,
                prompt=prompt,
                max_tokens_to_sample=300,
                temperature=0.7,
                stop_sequences=["\n\nHuman:"]
            )
            
            return self._parse_response(response.completion, step, max_steps)
        except Exception as e:
            self.logger.error(f"Error in run method: {e}")
            raise
        
    def _create_prompt(self, task: str, step: int, reasoning: List[str], max_steps: int) -> str:
        system_prompt = "You are an AI assistant specialized in solving reasoning tasks through careful analysis."
        human_prompt = f"Task: {task}\n\nPrevious reasoning steps:\n"
        
        for i, reason in enumerate(reasoning, 1):
            human_prompt += f"{i}. {reason}\n"
        
        if step < max_steps - 1:
            human_prompt += f"\nProvide step {step + 1} of the reasoning process."
        else:
            human_prompt += "\nBased on the previous steps, provide the final solution to the task."
        
        return f"{system_prompt}\n\nHuman: {human_prompt}\n\nAssistant:"
    
    def _create_messages(self, task: str, step: int, reasoning: List[str], max_steps: int) -> Tuple[List[Dict[str, str]], str]:
        """
        Create a list of messages and system prompt for the Claude model based on the current state of the reasoning task.

        Args:
            task (str): The main task or question to be reasoned about.
            step (int): The current step in the reasoning process.
            reasoning (List[str]): A list of previous reasoning steps.
            max_steps (int): The total number of steps in the reasoning process.

        Returns:
            Tuple[List[Dict[str, str]], str]: A tuple containing a list of message dictionaries and the system prompt.
        """
        system_prompt = "You are an AI assistant specialized in solving reasoning tasks through careful analysis."
        human_prompt = f"Task: {task}\n\nPrevious reasoning steps:\n"
        
        for i, reason in enumerate(reasoning, 1):
            human_prompt += f"{i}. {reason}\n"
        
        if step < max_steps - 1:
            human_prompt += f"\nProvide step {step + 1} of the reasoning process."
        else:
            human_prompt += "\nBased on the previous steps, provide the final solution to the task."
        
        return f"{system_prompt}\n\nHuman: {human_prompt}\n\nAssistant:"

    def _messages_to_prompt(self, messages: List[Dict[str, str]], system_prompt: str) -> str:
        """
        Convert a list of messages and system prompt to a single prompt string for the Completions API.

        Args:
            messages (List[Dict[str, str]]): A list of message dictionaries.
            system_prompt (str): The system prompt.

        Returns:
            str: A formatted prompt string.
        """
        prompt = f"{system_prompt}\n\n"
        for message in messages:
            if message['role'] == 'user':
                prompt += "User: " + message['content'] + "\n\n"
            elif message['role'] == 'assistant':
                prompt += "Assistant: " + message['content'] + "\n\n"
        prompt += "Assistant: "
        return prompt

    def _parse_response(self, response: str, step: int, max_steps: int) -> Dict[str, Any]:
        """
        Parse the response from the Claude model into the required format.

        Args:
            response (str): The raw response string from the Claude model.
            step (int): The current step in the reasoning process.
            max_steps (int): The total number of steps in the reasoning process.

        Returns:
            Dict[str, Any]: A dictionary containing either the next reasoning step or the final solution.
        """
        if step < max_steps - 1:
            return {"text_data": {"reasoning": response.strip()}}
        else:
            return {"text_data": {"solution": response.strip()}}