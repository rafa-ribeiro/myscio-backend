from chromadb import HttpClient
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from app.core.logger import logger
from app.domain.repositories.vectordb.repository import VectorDBRepository


def get_chroma_client(chroma_host: str, chroma_port: int) -> HttpClient:
    client = HttpClient(host=chroma_host, port=chroma_port)
    return client


DEFAULT_COLLECTION = "main_collection"


class ChromaRepository(VectorDBRepository):

    def __init__(self, chroma_client: HttpClient, embeddings: Embeddings):
        self.chroma_client = chroma_client
        self.embeddings = embeddings

        self.vector_store = Chroma(
            collection_name=DEFAULT_COLLECTION,
            embedding_function=self.embeddings,
            client=self.chroma_client
        )

    def similarity_search(self, query: str, k: int = 3):
        results = self.vector_store.similarity_search(query=query, k=k)
        return results

    def save_documents(self, documents: list[Document], collection_name: str = DEFAULT_COLLECTION):
        try:
            self.vector_store.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=collection_name,
                client=self.chroma_client
            )
        except Exception as err:
            logger.log(f"Error saving documents to ChromaDB: {err}")
            return False
        else:
            return True
