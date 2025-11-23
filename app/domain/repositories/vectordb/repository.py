from typing import Protocol
from abc import ABC, abstractmethod

class VectorDBRepository(ABC):

    @abstractmethod
    def similarity_search(self, query: str, k: int = 3):
        ...

    @abstractmethod
    def save_documents(self, documents: list, collection_name: str = "main_collection"):
        ...
