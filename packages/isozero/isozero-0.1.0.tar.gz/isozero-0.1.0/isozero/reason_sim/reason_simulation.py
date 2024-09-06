from typing import Dict, Any

class ReasonSimulation:
    """
    A simulation environment for reasoning tasks.
    """

    def __init__(self, reason: str, max_steps: int = 3, total_questions: int = 1):
        """
        Initialize the ReasonSimulation.

        Args:
            reason: The reasoning task or question to be solved.
            max_steps: The maximum number of reasoning steps (default: 3).
            total_questions: The total number of questions in the set (default: 1).
        """
        self.reason = reason
        self.max_steps = max_steps
        self.total_questions = total_questions
        self.questions_completed = 0
        self.current_state = {
            'text_data': {
                'reason': reason,
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
            A dictionary representing the current state.
        """
        return self.current_state

    def step(self, sim_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Advance the simulation by one step.

        Args:
            sim_input: The input to the simulation for this step.

        Returns:
            The updated state of the simulation after this step.
        """
        step = self.current_state['text_data']['step']
        reasoning = sim_input['text_data'].get('reasoning', '')
        solution = sim_input['text_data'].get('solution', None)

        if step < self.max_steps - 1:
            self.current_state['text_data']['reasoning'].append(reasoning)
            self.current_state['text_data']['step'] += 1
        elif step == self.max_steps - 1:
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
        Render the current state of the simulation as a string.

        Returns:
            A string representation of the current state.
        """
        return str(self.current_state)

    def close(self):
        """Close the simulation and perform any necessary cleanup.""" 
        self.questions_completed += 1
        if self.questions_completed == self.total_questions:
            print("Reason simulation closed")