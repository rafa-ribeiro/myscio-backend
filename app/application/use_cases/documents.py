from app.core.logger import logger
from app.domain.repositories.vectordb.repository import VectorDBRepository
from app.infrastructure.documents.doc_handler import load_from_file_obj


class NewDocumentFromFileObjUseCases:
    def __init__(self, vector_db: VectorDBRepository):
        self.vector_db = vector_db

    async def save(self, file_obj):
        documents = await load_from_file_obj(file_obj=file_obj)
        result = self.vector_db.save_documents(documents=documents)

        if not result:
            logger.error(f"Error on saving documents to vector database. Document = {documents}")
            raise Exception("Failed to save documents to the vector database.")
