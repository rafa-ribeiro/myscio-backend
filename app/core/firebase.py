import firebase_admin
from firebase_admin import credentials

from app.core.settings import get_settings

settings = get_settings()


def init_firebase():
    if not firebase_admin._apps:
        cred_path = settings.FIREBASE_CREDENTIALS_PATH

        if not cred_path:
            raise ValueError("FIREBASE_CREDENTIALS_PATH environment variable is not set.")

        credential = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(credential)
