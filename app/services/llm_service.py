from openai import OpenAI

from app.core.config import settings


class LLMService:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = OpenAI(api_key=settings.openai_api_key)
        return cls._client

    @classmethod
    def generate_response(cls, prompt: str) -> str:
        try:
            client = cls.get_client()

            response = client.chat.completions.create(
                model=settings.llm_model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"[Mock Response] LLM unavailable. Retrieved context used.\n\nError: {str(e)}"