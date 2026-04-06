from __future__ import annotations
from dataclasses import dataclass, field
from document_loader import load_document
from llm_client import get_llm_response
from prompt_builder import build_messages_payload
from retriever import retrieve_relevant_chunks
from text_splitter import split_text


@dataclass
class SessionState:
    document_path: str | None = None
    document_text: str = ""
    chunks: list[str] = field(default_factory=list)
    last_question: str | None = None
    last_relevant_chunks: list[str] = field(default_factory=list)
    last_messages: list[dict[str, str]] = field(default_factory=list)
    last_answer: str | None = None


class QAService:
    def __init__(self) -> None:
        self.state = SessionState()

    def load_document(self, path: str) -> None:
        text = load_document(path)
        chunks = split_text(text)
        if not chunks:
            raise ValueError("Ошибка: после split_text получен пустой список чанков")

        self.state.document_path = path
        self.state.document_text = text
        self.state.chunks = chunks
        self.state.last_question = None
        self.state.last_relevant_chunks = []
        self.state.last_messages = []
        self.state.last_answer = None

    def ask(self, user_question: str) -> str:
        if not user_question or not user_question.strip():
            raise ValueError("Ошибка: пустой вопрос")
        if not self.state.chunks:
            raise ValueError("Ошибка: документ не загружен или не разбит на чанки")

        relevant_chunks = retrieve_relevant_chunks(user_question, self.state.chunks)
        if not relevant_chunks:
            answer = "В тексте нет информации об этом"
            self.state.last_question = user_question
            self.state.last_relevant_chunks = []
            self.state.last_messages = []
            self.state.last_answer = answer
            return answer

        messages = build_messages_payload(relevant_chunks, user_question)
        answer = get_llm_response(messages)

        self.state.last_question = user_question
        self.state.last_relevant_chunks = relevant_chunks
        self.state.last_messages = messages
        self.state.last_answer = answer

        return answer

    def clear_session(self) -> None:
        self.state = SessionState()

    def clear(self) -> None:
        self.clear_session()

    def get_chunks(self) -> list[str]:
        return list(self.state.chunks)

    def get_document_path(self) -> str | None:
        return self.state.document_path
