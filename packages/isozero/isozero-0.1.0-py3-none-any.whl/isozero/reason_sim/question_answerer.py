from typing import List, Dict, Any
import tiktoken

class QuestionAnswerer:
    def __init__(self, agent: Any, reasoning_steps: int = 3, max_tokens: int = 8000):
        self.agent = agent
        self.reasoning_steps = reasoning_steps
        self.max_tokens = max_tokens
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def answer_questions(self, question_doc_pairs: Dict[str, str]) -> Dict[str, Dict[str, List[str]]]:
        answers = {}
        for question, document in question_doc_pairs.items():
            truncated_document = self._truncate_document(document)
            answer = self._reason_and_answer(question, truncated_document)
            answers[question] = answer
        return answers

    def _truncate_document(self, document: str) -> str:
        tokens = self.tokenizer.encode(document)
        if len(tokens) > self.max_tokens:
            truncated_tokens = tokens[:self.max_tokens]
            return self.tokenizer.decode(truncated_tokens)
        return document

    def _reason_and_answer(self, question: str, document: str) -> Dict[str, List[str]]:
        reasoning_steps = []
        for step in range(self.reasoning_steps):
            prompt = self._create_reasoning_prompt(question, document, reasoning_steps, step)
            response = self.agent.run(prompt)
            reasoning_step = self._extract_reasoning(response)
            reasoning_steps.append(reasoning_step)

        solution_prompt = self._create_solution_prompt(question, document, reasoning_steps)
        solution_response = self.agent.run(solution_prompt)
        solution = self._extract_solution(solution_response)

        return {
            'reasoning': reasoning_steps,
            'solution': solution
        }

    def _create_reasoning_prompt(self, question: str, document: str, reasoning_steps: List[str], step: int) -> Dict[str, Any]:
        return {
            'text': {
                'task': f"Question: {question}\nDocument: {document}",
                'step': step,
                'reasoning': reasoning_steps,
                'max_steps': self.reasoning_steps
            }
        }

    def _create_solution_prompt(self, question: str, document: str, reasoning_steps: List[str]) -> Dict[str, Any]:
        return {
            'text': {
                'task': f"Question: {question}\nDocument: {document}",
                'step': self.reasoning_steps,
                'reasoning': reasoning_steps,
                'max_steps': self.reasoning_steps
            }
        }

    def _extract_reasoning(self, response: Dict[str, Any]) -> str:
        if 'text_data' in response and 'reasoning' in response['text_data']:
            return response['text_data']['reasoning']
        elif isinstance(response, str):
            return response
        elif isinstance(response, dict) and 'content' in response:
            return response['content']
        else:
            return str(response)  # Default to string representation if structure is unknown

    def _extract_solution(self, response: Dict[str, Any]) -> str:
        if 'text_data' in response and 'solution' in response['text_data']:
            return response['text_data']['solution']
        elif isinstance(response, str):
            return response
        elif isinstance(response, dict) and 'content' in response:
            return response['content']
        else:
            return str(response)  # Default to string representation if structure is unknown