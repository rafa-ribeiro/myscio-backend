from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.infrastructure.dependency_injector.container import AppContainer
from app.core.settings import get_settings
from app.interfaces.api.routes import router as api_router
from contextlib import asynccontextmanager
from app.core.firebase import init_firebase

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup code can be added here
    init_firebase()
    yield
    # Shutdown code can be added here


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    :return: Configured FastAPI application instance.
    """
    settings = get_settings()

    _app = FastAPI(
        debug=settings.DEBUG,
        title=settings.name,
        version=settings.version,
        root_path=settings.root_path,
        description="A system to help you to manage all the knowledge in one place.",
        lifespan=lifespan,
    )

    _app.container = AppContainer()

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app

app = create_app()
app.include_router(api_router)
