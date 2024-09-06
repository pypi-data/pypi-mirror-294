"""This module contains the MathProblemSimulation class for simulating mathematical problem-solving."""

from typing import Dict, Any

class MathProblemSimulation:
    """A class representing a simulation of a mathematical problem-solving process."""

    def __init__(self, problem):
        """
        Initialize the MathProblemSimulation.

        Args:
            problem (dict): A dictionary containing the problem description and question.
        """
        self.problem = problem
        self.current_state = {
            'text_data': {
                'problem': problem['Body'] + " " + problem['Question'],
                'step': 0,
                'reasoning': [],
                'solution': None
            },
            'step_count': 0
        }

    def get_state(self) -> Dict[str, Any]:
        """
        Get the current state of the simulation.

        Returns:
            dict: The current state of the simulation.
        """
        return self.current_state

    def step(self, sim_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform a step in the simulation based on the input.

        Args:
            sim_input (dict): The input for the current step.

        Returns:
            dict: The updated state of the simulation.
        """
        step = self.current_state['text_data']['step']
        reasoning = sim_input['text_data'].get('reasoning', '')
        solution = sim_input['text_data'].get('solution', None)

        if step < 3:
            self.current_state['text_data']['reasoning'].append(reasoning)
            self.current_state['text_data']['step'] += 1
        elif step == 3:
            self.current_state['text_data']['solution'] = solution

        self.current_state['step_count'] += 1
        return self.current_state

    def reset(self):
        """Reset the simulation to its initial state."""
        self.current_state['text_data']['step'] = 0
        self.current_state['text_data']['reasoning'] = []
        self.current_state['text_data']['solution'] = None
        self.current_state['step_count'] = 0

    def render(self) -> str:
        """
        Render the current state of the simulation.

        Returns:
            str: A string representation of the current state.
        """
        return str(self.current_state)

    def close(self):
        """Close the simulation and perform any necessary cleanup."""
        print("Math Problem simulation closed")
