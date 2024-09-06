"""
isozero - A package for zero-shot reasoning in mathematical problem-solving.

This package provides tools for simulating and evaluating the performance of
AI agents on mathematical problems using a step-by-step reasoning approach.
"""

from .claude import ClaudeAgent
from .math_simulation import MathProblemSimulation
from .math_wrapper import MathSimulationWrapper

__all__ = ['ClaudeAgent', 'MathProblemSimulation', 'MathSimulationWrapper']
