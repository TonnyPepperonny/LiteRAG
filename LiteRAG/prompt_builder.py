from __future__ import annotations
from typing import Sequence
from config import SYSTEM_PROMPT


def build_messages_payload(relevant_chunks: Sequence[str], user_question: str) -> list[dict[str, str]]:
    if not user_question or not user_question.strip():
        raise ValueError("Ошибка: пустой вопрос")

    clean_chunks = [chunk.strip() for chunk in relevant_chunks if chunk and chunk.strip()]
    context = "\n\n".join(clean_chunks)

    user_content = f"Контекст:\n{context}\n\nВопрос пользователя:\n{user_question.strip()}"

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]
