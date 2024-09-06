from typing import Dict, Any, List
import logging
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class HuggingFaceAgent:
    """
    An agent that uses Hugging Face's transformers for reasoning and question answering tasks.
    """
    
    def __init__(self, model_name: str = "google/flan-t5-large", max_length: int = 512):
        """
        Initialize the HuggingFaceAgent with a specified model.
        
        Args:
            model_name (str): The name of the Hugging Face model to use. Default is "google/flan-t5-large".
            max_length (int): The maximum length of input/output tokens. Default is 512.
        """
        self.model_name = model_name
        self.max_length = max_length
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None
        self.logger = logging.getLogger(__name__)

    def _load_model(self):
        """
        Lazy load the model to save memory when the agent is initialized but not used.
        """
        if self.tokenizer is None or self.model is None:
            try:
                self.logger.info(f"Loading model {self.model_name}...")
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(self.device)
                self.logger.info(f"Model {self.model_name} loaded successfully.")
            except Exception as e:
                self.logger.error(f"Failed to load model {self.model_name}: {str(e)}")
                raise

    def run(self, agent_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the agent on the given input.
        
        Args:
            agent_input (Dict[str, Any]): A dictionary containing the input for the agent.
        
        Returns:
            Dict[str, Any]: A dictionary containing the agent's output.
        """
        try:
            self._load_model()
            text_data = agent_input['text']
            task = text_data['task']
            step = text_data['step']
            reasoning = text_data.get('reasoning', [])
            max_steps = text_data['max_steps']

            prompt = self._create_prompt(task, step, reasoning, max_steps)
            response = self._generate_response(prompt)
            
            return self._parse_response(response, step, max_steps)
        except Exception as e:
            self.logger.error(f"Error in run method: {str(e)}")
            return {"text_data": {"reasoning": f"Error: {str(e)}", "solution": "Unable to generate a response due to an error."}}

    def _create_prompt(self, task: str, step: int, reasoning: List[str], max_steps: int) -> str:
        """
        Create a prompt for the Hugging Face model based on the current state of the reasoning task.

        Args:
            task (str): The main task or question to be reasoned about.
            step (int): The current step in the reasoning process.
            reasoning (List[str]): A list of previous reasoning steps.
            max_steps (int): The total number of steps in the reasoning process.

        Returns:
            str: A formatted prompt string.
        """
        prompt = f"Task: {task}\n\nPrevious reasoning steps:\n"
        for i, reason in enumerate(reasoning, 1):
            prompt += f"{i}. {reason}\n"
        
        if step < max_steps - 1:
            prompt += f"\nProvide step {step + 1} of the reasoning process."
        else:
            prompt += "\nBased on the previous steps, provide the final solution to the task."
        
        return prompt

    def _generate_response(self, prompt: str) -> str:
        """
        Generate a response from the Hugging Face model.

        Args:
            prompt (str): The input prompt for the model.

        Returns:
            str: The generated response from the model.
        """
        try:
            # Tokenize the input and move it to the appropriate device (CPU or GPU)
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=self.max_length).to(self.device)
            
            # Generate the output
            outputs = self.model.generate(**inputs, max_length=self.max_length, num_return_sequences=1, do_sample=True)
            
            # Decode the output tokens to a string
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            self.logger.error(f"Error in generating response: {str(e)}")
            return f"Error in generating response: {str(e)}"

    def _parse_response(self, response: str, step: int, max_steps: int) -> Dict[str, Any]:
        """
        Parse the response from the Hugging Face model into the required format.

        Args:
            response (str): The raw response string from the Hugging Face model.
            step (int): The current step in the reasoning process.
            max_steps (int): The total number of steps in the reasoning process.

        Returns:
            Dict[str, Any]: A dictionary containing either the next reasoning step or the final solution.
        """
        if step < max_steps - 1:
            return {"text_data": {"reasoning": response.strip()}}
        else:
            return {"text_data": {"solution": response.strip()}}