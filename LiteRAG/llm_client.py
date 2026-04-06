from __future__ import annotations
import os
from typing import Sequence
from dotenv import load_dotenv
from openai import OpenAI
from config import BASE_URL, MODEL_NAME

load_dotenv()


def get_llm_response(messages: Sequence[dict[str, str]], max_tokens: int = 300) -> str:
    if not messages:
        raise ValueError("Ошибка: messages пуст")

    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=BASE_URL)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=list(messages),
        max_tokens=max_tokens,
        stream=False,
    )

    content = response.choices[0].message.content
    return (content or "").strip()
