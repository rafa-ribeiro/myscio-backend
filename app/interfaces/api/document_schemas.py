from pydantic import BaseModel


class SearchDocumentRequest(BaseModel):
    prompt: str


class SearchDocumentResponse(BaseModel):
    response: str
