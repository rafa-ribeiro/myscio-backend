import os

import google.generativeai as genai

from app.core.generatives_ai import GenerativeAIModel, GenerativeAIClient
from app.core.settings import get_settings

settings = get_settings()
os.environ["GOOGLE_API_KEY"] = settings.GEMINI_API_KEY
os.environ["GEMINI_API_KEY"] = settings.GEMINI_API_KEY


def get_gemini_client(genai_model: GenerativeAIModel):
    genai.configure(api_key=settings.GEMINI_API_KEY)

    gemini = genai.GenerativeModel(model_name=genai_model.value)
    return gemini


def init_gemini_embeddings():
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return embeddings


class GeminiClient(GenerativeAIClient):

    def __init__(self, genai_model: GenerativeAIModel):
        self.client = get_gemini_client(genai_model)

    def generate_content(self, prompt: str) -> str:
        response = self.client.generate_content(prompt)
        return response.text
