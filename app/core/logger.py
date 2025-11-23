import logging

from app.core.settings import get_settings

settings = get_settings()

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(settings.name)
