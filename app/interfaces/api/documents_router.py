from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status, UploadFile, File

from app.application.use_cases.documents import NewDocumentFromFileObjUseCases
from app.application.use_cases.prompt import ContextualSearchUseCase
from app.infrastructure.dependency_injector.container import AppContainer
from app.interfaces.api import API_V1
from app.interfaces.api.document_schemas import SearchDocumentRequest, SearchDocumentResponse

router = APIRouter(prefix=f"{API_V1}/documents", tags=["Documents"])


@router.post(
    path="/upload/",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_201_CREATED: {"description": "File upload successful"}},
)
@inject
async def upload(
        file: UploadFile = File(...),
        new_document_use_case: NewDocumentFromFileObjUseCases = Depends(Provide[AppContainer.new_document_use_case]),
):
    await new_document_use_case.save(file_obj=file)


@router.post(
    path="/search/",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"description": "Successful AI search"}},
    response_model=SearchDocumentResponse,
)
@inject
def search(
        search_doc_request: SearchDocumentRequest,
        contextual_search_use_case: ContextualSearchUseCase = Depends(Provide[AppContainer.contextual_search_use_case]),
):
    response = contextual_search_use_case.search(prompt=search_doc_request.prompt)
    return SearchDocumentResponse(
        response=response
    )
