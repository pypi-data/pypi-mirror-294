import os
import sys
import logging
from typing import Any, Dict, List
from venv import logger
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from .config_loader import gpt_model
import tiktoken

def check_api_key() -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logging.error("Ошибка: Переменная окружения OPENAI_API_KEY не установлена.")
        sys.exit(1)
    return api_key

def get_string_size_kb(string: str) -> float:
    size_bytes = len(string.encode('utf-8'))
    size_kb = size_bytes / 1024
    return size_kb

def save_response_to_file(response: str, temp_dir: str) -> str:
    count = len(os.listdir(temp_dir)) + 1
    file_path = os.path.join(temp_dir, f"response_{count}.md")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response)
        logging.info(f"Ответ сохранен в {temp_dir}")
    except IOError as e:
        logging.error(f"Ошибка при сохранении ответа в файл: {file_path}: {e}", exc_info=True)
    return file_path

style = Style.from_dict({
    'prompt': 'ansiblue bold',
})

bindings = KeyBindings()

@bindings.add('c-c')
def _(event):
    exit()

@bindings.add('c-d')
def _(event):
    exit()

@bindings.add('enter')
def _(event):
    buffer = event.current_buffer
    if buffer.validate():
        buffer.validate_and_handle()

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except IOError as e:
        logger.error(f"Не удалось прочитать файл {file_path}: {e}", exc_info=True)
        return ""

def num_tousend_tokens_from_messages(messages: List[Dict[str, Any]], model: str = gpt_model):
    """Возвращает количество тысяч токенов в сообщениях."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning("Model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = 0

    for message in messages:
        if type(message) == dict:
            for _, value in message.items():
                num_tokens += len(encoding.encode(value))
        else:
            num_tokens += len(encoding.encode(message.to_json()))

    # Округление до ближайшей тысячи токенов
    tokens_per_thousand = (num_tokens + 999) // 1000
    logging.info(f"В сообщении ~{max(1, tokens_per_thousand)}K токенов")
