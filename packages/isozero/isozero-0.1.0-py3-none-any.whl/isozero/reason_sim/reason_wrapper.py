from .base_wrapper import BaseWrapper

class ReasonSimulationWrapper(BaseWrapper):
    def __init__(self, agent, simulation):
        self.agent = agent
        self.simulation = simulation

    def step(self):
        sim_state = self.simulation.get_state()
        agent_input = self._convert_to_agent_input(sim_state)
        agent_output = self.agent.run(agent_input)
        sim_input = self._convert_from_agent_output(agent_output)
        return self.simulation.step(sim_input)

    def _convert_to_agent_input(self, sim_state):
        """
        Convert the simulation state to a format the agent can understand.

        Args:
            sim_state: The current state of the simulation.

        Returns:
            A dictionary containing the formatted input for the agent.
        """
        text_data = sim_state['text_data']
        return {
            'text': {
                'task': text_data['reason'],
                'step': text_data['step'],
                'reasoning': text_data['reasoning'],
                'max_steps': self.simulation.max_steps
            }
        }

    def _convert_from_agent_output(self, agent_output):
        return agent_output

    def reset(self):
        self.simulation.reset()

    def render(self):
        return self.simulation.render()

    def close(self):
        self.simulation.close()