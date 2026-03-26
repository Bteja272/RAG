from app.core.config import settings
from app.services.prompt_service import PromptService
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService


class RAGService:
    @staticmethod
    def query(query: str) -> dict:
        # Step 1 — retrieve context
        chunks = RetrievalService.retrieve(
            query=query,
            top_k=settings.retrieval_top_k,
        )

        # Step 2 — build prompt
        prompt = PromptService.build_prompt(query=query, context_chunks=chunks)

        # Step 3 — generate response
        answer = LLMService.generate_response(prompt)

        return {
            "query": query,
            "answer": answer,
            "sources": chunks,
        }