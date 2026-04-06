from qa_service import QAService


def print_help() -> None:
    print("Доступные команды:")
    print("load - загрузить документ")
    print("ask - задать вопрос по документу")
    print("chunks - показать текущие чанки")
    print("clear - очистить текущую сессию")
    print("help - показать список команд")
    print("exit - выйти из программы")


def main() -> None:
    service = QAService()

    print("Document Reader CLI")
    print_help()

    while True:
        command = input("\nВведите команду: ").strip().lower()

        if command == "load":
            path = input("Введите путь к файлу: ").strip()
            try:
                service.load_document(path)
                chunks = service.get_chunks()
                print("Документ загружен")
                print(f"Путь: {service.get_document_path()}")
                print(f"Количество чанков: {len(chunks)}")
            except Exception as exc:
                print(f"Ошибка: {exc}")
            continue

        if command == "ask":
            question = input("Введите вопрос: ")
            try:
                answer = service.ask(question)
                print("Ответ:")
                print(answer)
            except Exception as exc:
                print(f"Ошибка: {exc}")
            continue

        if command == "chunks":
            try:
                chunks = service.get_chunks()
                if not chunks:
                    print("Чанки отсутствуют. Сначала загрузите документ.")
                    continue
                print(f"Количество чанков: {len(chunks)}")
                for i, chunk in enumerate(chunks, start=1):
                    print(f"\n--- CHUNK #{i} ---")
                    print(chunk)
            except Exception as exc:
                print(f"Ошибка: {exc}")
            continue

        if command == "clear":
            service.clear()
            print("Сессия очищена")
            continue

        if command == "help":
            print_help()
            continue

        if command == "exit":
            print("Выход из программы")
            break

        print("Неизвестная команда. Введите help для списка команд.")


if __name__ == "__main__":
    main()
