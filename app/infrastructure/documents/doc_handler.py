import tempfile
from typing import Iterable, List
from uuid import uuid4

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.infrastructure.documents.exceptions import InvalidDocumentTypeError


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


async def _load_from_txt_obj(file_obj) -> list[Document]:
    content = await file_obj.read()
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    documents = [Document(page_content=content)]
    _assign_id_to_documents(documents=documents)
    return documents


async def _load_from_pdf_obj(file_obj) -> list[Document]:
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as temp_pdf:
        content = await file_obj.read()
        temp_pdf.write(content)
        loader = PyPDFLoader(temp_pdf.name)
        documents = loader.load()
        _assign_id_to_documents(documents=documents)
        return documents


SUPPORTED_FILE_TYPES = {
    'txt': _load_from_txt_obj,
    'pdf': _load_from_pdf_obj
}


async def load_from_file_obj(file_obj) -> list[Document]:
    file_extension = file_obj.filename.split('.')[-1].lower()
    loader = SUPPORTED_FILE_TYPES.get(file_extension, None)

    if not loader:
        raise InvalidDocumentTypeError(document_type=file_extension, valid_types=list(SUPPORTED_FILE_TYPES.keys()))

    documents = await loader(file_obj=file_obj)
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
