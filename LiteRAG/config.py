MODEL_NAME = 'deepseek-chat'
BASE_URL = 'https://api.deepseek.com'
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
K_REL_CHUNKS = 3
MODEL_NAME_RETR = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
SYSTEM_PROMPT = "Ты — AI ассистент, который отвечает на вопросы по документу. Используй только предоставленный контекст. Если ответа нет — скажи, что информации нет. Не выдумывай ничего от себя."

messages = [
        ]
