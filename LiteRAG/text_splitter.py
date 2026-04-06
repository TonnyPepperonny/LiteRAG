from __future__ import annotations
from nltk.tokenize import sent_tokenize
from config import CHUNK_OVERLAP, CHUNK_SIZE
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')

def split_text(text: str) -> list[str]:
    if not text or not text.strip():
        return []

    sentences = sent_tokenize(text, language="russian")

    chunks: list[str] = []
    current_sentences: list[str] = []
    current_len = 0

    def join_sentences(items: list[str]) -> str:
        return " ".join(items).strip()

    def tail_with_overlap(items: list[str], max_tail_len: int) -> list[str]:
        if not items or max_tail_len <= 0:
            return []
        tail: list[str] = []
        tail_len = 0
        for sentence in reversed(items):
            sentence_len = len(sentence)
            separator = 1 if tail else 0
            if tail and tail_len + separator + sentence_len > max_tail_len:
                break
            if not tail and sentence_len > max_tail_len:
                tail.insert(0, sentence[-max_tail_len:])
                break
            tail.insert(0, sentence)
            tail_len += separator + sentence_len
        return tail

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        sentence_len = len(sentence)

        if sentence_len > CHUNK_SIZE:
            if current_sentences:
                chunks.append(join_sentences(current_sentences))
                current_sentences = []
                current_len = 0

            start = 0
            step = max(CHUNK_SIZE - CHUNK_OVERLAP, 1)
            while start < sentence_len:
                end = start + CHUNK_SIZE
                chunk = sentence[start:end].strip()
                if chunk:
                    chunks.append(chunk)
                if end >= sentence_len:
                    break
                start += step
            continue

        separator = 1 if current_sentences else 0
        if current_len + separator + sentence_len <= CHUNK_SIZE:
            current_sentences.append(sentence)
            current_len += separator + sentence_len
            continue

        chunks.append(join_sentences(current_sentences))
        current_sentences = tail_with_overlap(current_sentences, CHUNK_OVERLAP)
        current_len = len(join_sentences(current_sentences))

        separator = 1 if current_sentences else 0
        if current_len + separator + sentence_len <= CHUNK_SIZE:
            current_sentences.append(sentence)
            current_len += separator + sentence_len
        else:
            chunks.append(sentence)
            current_sentences = []
            current_len = 0

    if current_sentences:
        chunks.append(join_sentences(current_sentences))

    return chunks
