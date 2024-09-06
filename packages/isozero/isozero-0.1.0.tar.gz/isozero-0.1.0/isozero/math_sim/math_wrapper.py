"""This module contains the SimulationWrapper class for wrapping the simulation and agent interaction."""

from .basewrapper import BaseWrapper

class MathSimulationWrapper(BaseWrapper):
    """A wrapper class for managing the interaction between the simulation and the agent."""

    def __init__(self, agent, simulation):
        """
        Initialize the SimulationWrapper.

        Args:
            agent: The agent to use for problem-solving.
            simulation: The simulation to run.
        """
        super().__init__(agent)
        self.simulation = simulation

    def step(self):
        """
        Perform a single step in the simulation.

        Returns:
            dict: The updated state of the simulation after the step.
        """
        sim_state = self.simulation.get_state()
        agent_input = self._convert_to_agent_input(sim_state)
        agent_output = self.agent.run(agent_input)
        sim_input = self._convert_from_agent_output(agent_output)
        return self.simulation.step(sim_input)

    def _convert_to_agent_input(self, sim_state):
        """
        Convert the simulation state to agent input format.

        Args:
            sim_state (dict): The current state of the simulation.

        Returns:
            dict: The converted input for the agent.
        """
        return {'text': sim_state['text_data']}

    def _convert_from_agent_output(self, agent_output):
        """
        Convert the agent output to simulation input format.

        Args:
            agent_output (dict): The output from the agent.

        Returns:
            dict: The converted input for the simulation.
        """
        return agent_output

    def reset(self):
        """Reset the simulation and the agent if applicable."""
        self.simulation.reset()

    def render(self):
        """
        Render the current state of the simulation.

        Returns:
            str: A string representation of the current simulation state.
        """
        return self.simulation.render()

    def close(self):
        """Close the simulation and perform any necessary cleanup."""
        self.simulation.close()
