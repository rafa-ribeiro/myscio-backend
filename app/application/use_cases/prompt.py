from typing import Optional

from app.core.generatives_ai import GenerativeAIClient, ContextType, ContextualPromptBuilder
from app.domain.repositories.vectordb.repository import VectorDBRepository


class ContextualSearchUseCase:

    def __init__(self, vector_db: VectorDBRepository, gen_ai_client: GenerativeAIClient):
        self.vector_db = vector_db
        self.gen_ai_client = gen_ai_client

    def search(self, prompt: str, context_type: Optional[ContextType] = ContextType.JSON) -> str:
        results = self.vector_db.similarity_search(query=prompt, k=3)
        contexts = [doc.page_content for doc in results]

        contextual_prompt = ContextualPromptBuilder.build(
            prompt=prompt,
            context=contexts,
            context_type=context_type
        )

        response = self.gen_ai_client.generate_content(prompt=contextual_prompt)
        return response
