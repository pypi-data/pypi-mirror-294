from bs4 import BeautifulSoup
from typing import List

class TextExtractor:
    """
    A class for extracting plain text from various document formats.
    """

    @staticmethod
    def extract(documents: List[str]) -> List[str]:
        """
        Extract plain text from a list of documents.

        Args:
            documents: A list of strings, each containing the content of a document.

        Returns:
            A list of strings, each containing the extracted plain text from a document.
        """
        return [TextExtractor._extract_text(doc) for doc in documents]

    @staticmethod
    def _extract_text(document: str) -> str:
        """
        Extract plain text from a single document.

        This method attempts to parse the document as HTML and extract text.
        If it's not HTML, it returns the original content.
        """
        try:
            soup = BeautifulSoup(document, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        except:
            # If parsing as HTML fails, assume it's already plain text
            return document.strip()