"""Main script for running the zero-shot reasoning simulation."""

import json
import os
import csv
from dotenv import load_dotenv
from .claude import ClaudeAgent
from .math_simulation import MathProblemSimulation
from .math_wrapper import MathSimulationWrapper

def run_simulation():
    """Run the zero-shot reasoning simulation on a test set of math problems."""
    # Load environment variables for secure API key storage
    load_dotenv()

    # Load test set
    with open('testset.json', 'r') as f:
        test_set = json.load(f)

    # Initialize OpenAI agent
    agent = ClaudeAgent(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    results = []

    for problem in test_set:
        simulation = MathProblemSimulation(problem)
        wrapper = MathSimulationWrapper(agent, simulation)
        
        # Run simulation
        for _ in range(4):  # 3 reasoning steps + 1 solution step
            wrapper.step()
        
        # Get final state
        final_state = wrapper.simulation.get_state()
        
        # Extract Claude's answer
        claude_answer = final_state['text_data']['solution']
        
        # Compare with correct answer
        correct_answer = problem['Answer']
        score = 1 if isinstance(claude_answer, (int, float)) and abs(claude_answer - correct_answer) < 0.01 else 0
        
        results.append({
            'ID': problem['ID'],
            'Claude_Answer': claude_answer,
            'Correct_Answer': correct_answer,
            'Score': score
        })

    # Calculate aggregate score
    aggregate_score = sum(result['Score'] for result in results)

    # Write results to CSV
    with open('results.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['ID', 'Claude_Answer', 'Correct_Answer', 'Score'])
        writer.writeheader()
        writer.writerows(results)

    print(f"Aggregate Score: {aggregate_score}/{len(test_set)}")

if __name__ == "__main__":
    run_simulation()
