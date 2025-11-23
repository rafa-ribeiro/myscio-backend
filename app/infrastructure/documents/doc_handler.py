from typing import Iterable, List
from uuid import uuid4

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def _assign_id_to_documents(documents: List[Document]) -> None:
    for doc in documents:
        if not doc.metadata:
            doc.metadata = {}

        doc.metadata["id"] = str(uuid4())


def load_from_file(filepath: str) -> list[Document]:
    loader = TextLoader(filepath)
    documents = loader.load()
    _assign_id_to_documents(documents=documents)
    return documents


def load_from_string(content: str) -> list[Document]:
    documents = [Document(page_content=content)]
    _assign_id_to_documents(documents=documents)
    return documents


async def load_from_file_obj(file_obj) -> list[Document]:
    content = await file_obj.read()
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    documents = [Document(page_content=content)]
    _assign_id_to_documents(documents=documents)
    return documents


def split_documents(
        documents: Iterable[Document],
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        length_function=len,
        is_separator_regex: bool = False
) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function,
        is_separator_regex=is_separator_regex
    )
    return text_splitter.split_documents(documents)
