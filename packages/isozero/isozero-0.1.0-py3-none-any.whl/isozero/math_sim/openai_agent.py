import openai

client = OpenAI()

class OpenAIAgent:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def run(self, agent_input):
        prompt = self._create_prompt(agent_input)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or any other suitable OpenAI model
            messages=[
                {"role": "system", "content": prompt}
        ],
            max_tokens=150
        )
        return self._parse_response(response.choices[0].message.content, agent_input['text']['step'])

    def _create_prompt(self, agent_input):
        text_data = agent_input['text']
        problem = text_data['problem']
        step = text_data['step']
        reasoning = text_data['reasoning']

        if step < 3:
            return f"Math Problem: {problem}\n\nPrevious reasoning steps:\n{'; '.join(reasoning)}\n\nYou are on step {step + 1} of 3 in the reasoning process. Provide the next step of reasoning to solve this math problem."
        else:
            return f"Math Problem: {problem}\n\nPrevious reasoning steps:\n{'; '.join(reasoning)}\n\nBased on your reasoning, provide the final numerical solution to the math problem. Your answer should be a single number without any additional text."

    def _parse_response(self, response, step):
        content = response.strip()
        if step < 3:
            return {"text_data": {"reasoning": content}}
        else:
            try:
                solution = float(content.split()[-1])  # Take the last word and convert to float
                return {"text_data": {"solution": solution}}
            except ValueError:
                return {"text_data": {"solution": content}}
