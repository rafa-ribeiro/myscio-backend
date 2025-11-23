from dependency_injector import containers, providers

from app.application.use_cases.documents import NewDocumentFromFileObjUseCases
from app.application.use_cases.prompt import ContextualSearchUseCase
from app.core.generatives_ai import GenerativeAIClient, GenerativeAIModel
from app.core.settings import get_settings
from app.domain.repositories.vectordb.repository import VectorDBRepository
from app.infrastructure.external_services.gemini.gemini_client import init_gemini_embeddings, GeminiClient
from app.infrastructure.repositories.chroma_repository import get_chroma_client, ChromaRepository


class AppContainer(containers.DeclarativeContainer):
    """Dependency injection container."""

    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.interfaces.api.documents_router",
            "app.interfaces.api.ai_router",
        ]
    )

    config = providers.Configuration()
    settings = get_settings()

    chroma_client = providers.Factory(
        get_chroma_client,
        chroma_host=settings.CHROMA_HOST,
        chroma_port=settings.CHROMA_PORT,
    )

    embeddings = providers.Factory(
        init_gemini_embeddings
    )

    vector_db_repository: VectorDBRepository = providers.Factory(
        ChromaRepository,
        chroma_client=chroma_client,
        embeddings=embeddings
    )

    new_document_use_case = providers.Factory(
        NewDocumentFromFileObjUseCases,
        vector_db=vector_db_repository
    )

    gemini_client: GenerativeAIClient = providers.Factory(
        GeminiClient,
        genai_model=GenerativeAIModel.GEMINI_2_5_FLASH
    )

    contextual_search_use_case = providers.Factory(
        ContextualSearchUseCase,
        vector_db=vector_db_repository,
        gen_ai_client=gemini_client,
    )
