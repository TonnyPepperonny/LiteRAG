from pathlib import Path


def load_txt(path: str) -> str:
    """Читает текст из .txt-файла и возвращает строку."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    text = file_path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"Пустой текст в файле: {path}")

    return text


def load_pdf(path: str) -> str:
    """Извлекает текст из .pdf-файла и возвращает строку."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # type: ignore
        except ImportError as exc:
            raise ImportError(
                "Для поддержки PDF требуется 'pypdf' (или 'PyPDF2'). Установите: pip install pypdf"
            ) from exc

    reader = PdfReader(str(file_path))
    text_chunks = [(page.extract_text() or "") for page in reader.pages]
    text = "\n".join(text_chunks).strip()

    if not text:
        raise ValueError(f"Пустой текст в файле: {path}")

    return text


def load_document(path: str) -> str:
    """Загружает текст из поддерживаемого формата (.txt или .pdf)."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")

    extension = file_path.suffix.lower()
    if extension == ".txt":
        return load_txt(path)
    if extension == ".pdf":
        return load_pdf(path)

    raise ValueError(f"Неподдерживаемый формат файла: {extension or '<без расширения>'}")
