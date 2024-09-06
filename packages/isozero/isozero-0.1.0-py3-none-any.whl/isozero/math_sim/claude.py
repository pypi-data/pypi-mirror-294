"""This module contains the ClaudeAgent class for interacting with the Anthropic API."""

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

class ClaudeAgent:
    """A class representing an AI agent using the Anthropic API for mathematical reasoning."""

    def __init__(self, api_key):
        """
        Initialize the ClaudeAgent.

        Args:
            api_key (str): The API key for accessing the Anthropic API.
        """
        self.client = Anthropic(api_key=api_key)

    def run(self, agent_input):
        """
        Run the agent with the given input.

        Args:
            agent_input (dict): A dictionary containing the input for the agent.

        Returns:
            dict: The agent's output.
        """
        prompt = self._create_prompt(agent_input)
        response = self.client.completions.create(
            model="claude-2",
            prompt=prompt,
            max_tokens_to_sample=300,
            stop_sequences=[HUMAN_PROMPT]
        )
        return self._parse_response(response.completion, agent_input['text']['step'])

    def _create_prompt(self, agent_input):
        """
        Create a prompt for the Anthropic API based on the agent input.

        Args:
            agent_input (dict): A dictionary containing the input for the agent.

        Returns:
            str: The generated prompt.
        """
        text_data = agent_input['text']
        problem = text_data['problem']
        step = text_data['step']
        reasoning = text_data['reasoning']

        if step < 3:
            return f"{HUMAN_PROMPT} Math Problem: {problem}\n\nPrevious reasoning steps:\n{'; '.join(reasoning)}\n\nYou are on step {step + 1} of 3 in the reasoning process. Provide the next step of reasoning to solve this math problem.{AI_PROMPT}"
        else:
            return f"{HUMAN_PROMPT} Math Problem: {problem}\n\nPrevious reasoning steps:\n{'; '.join(reasoning)}\n\nBased on your reasoning, provide the final numerical solution to the math problem. Your answer should be a single number without any additional text.{AI_PROMPT}"

    def _parse_response(self, response, step):
        """
        Parse the response from the Anthropic API.

        Args:
            response (str): The raw response from the API.
            step (int): The current step in the reasoning process.

        Returns:
            dict: The parsed response.
        """
        content = response.strip()
        if step < 3:
            return {"text_data": {"reasoning": content}}
        else:
            try:
                solution = float(content.split()[-1])  # Take the last word and convert to float
                return {"text_data": {"solution": solution}}
            except ValueError:
                return {"text_data": {"solution": content}}
