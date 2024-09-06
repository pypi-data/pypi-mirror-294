from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class DocumentSearch:
    """
    A class for searching documents based on questions.
    """

    def __init__(self, documents: List[str]):
        """
        Initialize the DocumentSearch with a list of documents.

        Args:
            documents: A list of strings, each containing the text of a document.
        """
        self.documents = documents
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(documents)

    def search(self, questions: List[str]) -> Dict[str, str]:
        """
        Search the documents for answers to the given questions.

        Args:
            questions: A list of strings, each containing a question.

        Returns:
            A dictionary mapping each question to the most relevant document text.
        """
        question_vector = self.vectorizer.transform(questions)
        similarities = cosine_similarity(question_vector, self.tfidf_matrix)
        
        results = {}
        for i, question in enumerate(questions):
            best_match_index = np.argmax(similarities[i])
            results[question] = self.documents[best_match_index]
        
        return results