import requests
from typing import List, Union
from bs4 import BeautifulSoup
import os

class DocumentLoader:
    """
    A class for loading documents from various sources.
    """

    @staticmethod
    def load(source: Union[str, List[str]]) -> List[str]:
        """
        Load document(s) from file(s), directory, or URL(s).

        Args:
            source: A string or list of strings representing file paths, directory path, or URLs.

        Returns:
            A list of strings, each containing the content of a loaded document.
        """
        if isinstance(source, str):
            source = [source]

        documents = []
        for item in source:
            if os.path.isfile(item):
                documents.append(DocumentLoader._load_file(item))
            elif os.path.isdir(item):
                documents.extend(DocumentLoader._load_directory(item))
            elif item.startswith(('http://', 'https://')):
                documents.append(DocumentLoader._load_webpage(item))
            else:
                raise ValueError(f"Invalid source: {item}")

        return documents

    @staticmethod
    def _load_file(file_path: str) -> str:
        """Load content from a single file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    @staticmethod
    def _load_directory(dir_path: str) -> List[str]:
        """Load content from all files in a directory."""
        documents = []
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            if os.path.isfile(file_path):
                documents.append(DocumentLoader._load_file(file_path))
        return documents

    @staticmethod
    def _load_webpage(url: str) -> str:
        """Load content from a webpage."""
        response = requests.get(url)
        response.raise_for_status()
        return response.text