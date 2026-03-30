import requests

from app.core.config import settings


class LLMService:
    @classmethod
    def generate_response(cls, prompt: str) -> str:
        if settings.llm_provider.lower() == "ollama":
            response = requests.post(
                f"{settings.ollama_base_url}/api/chat",
                json={
                    "model": settings.llm_model_name,
                    "messages": [
                        {"role": "system", "content": "You are a helpful AI assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    "stream": False,
                },
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]

        raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")