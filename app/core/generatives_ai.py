import json
from abc import ABC, abstractmethod
from enum import StrEnum


class GenerativeAIModel(StrEnum):
    GEMINI_2_5_FLASH = "gemini-2.5-flash"


class ContextType(StrEnum):
    JSON = "JSON"
    TOON = "TOON"


def _format_prompt_with_context_json(prompt: str, context: list[str]) -> str:
    context_json = json.dumps(context, ensure_ascii=False, indent=2)
    return f"Context (in JSON format):\n{context_json}\n\nQuestion: {prompt}"


TYPE_FORMATTERS = {
    ContextType.JSON: _format_prompt_with_context_json,
}


class ContextualPromptBuilder:

    @staticmethod
    def build(prompt: str, context: list[str], context_type: ContextType) -> str:
        context_formatter = TYPE_FORMATTERS.get(context_type, TYPE_FORMATTERS.get(ContextType.JSON))
        return context_formatter(prompt, context)


class GenerativeAIClient(ABC):

    @abstractmethod
    def generate_content(self, prompt: str) -> str:
        raise NotImplementedError
