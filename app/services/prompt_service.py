from typing import List


class PromptService:
    @staticmethod
    def build_prompt(query: str, context_chunks: List[dict]) -> str:
        context_text = "\n\n".join(
            [f"[Source {i+1}] {chunk['text']}" for i, chunk in enumerate(context_chunks)]
        )

        prompt = f"""
You are an AI assistant that answers questions using the provided context.

Instructions:
- Use ONLY the information from the context below
- If the answer is not in the context, say "I don't know based on the provided documents"
- Cite relevant sources when possible

Context:
{context_text}

Question:
{query}

Answer:
"""
        return prompt.strip()