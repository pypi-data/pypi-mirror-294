import logging
from openai import OpenAI, RateLimitError, AuthenticationError
from ..config_loader import gpt_model
from .functions import functions
from typing import List, Dict, Any

client = OpenAI()
logger = logging.getLogger(__name__)

def chat_completion_request(messages: List[Dict[str, Any]]) -> Dict:
    """Отправка запроса в OpenAI."""

    logger.info("Отправка запроса ...")

    try:
        response = client.chat.completions.create(
            model=gpt_model,
            messages=messages,
            tools=functions
        )
        logger.info("Запрос на завершение чата успешно выполнен.")
        return response

    except RateLimitError as rle:
        logger.critical(f"Превышение лимита запросов: {rle.message}")

    except AuthenticationError as ae:
        logger.critical("Ошибка аутентификации. Проверьте ключ API.")

    except Exception as e:
        logger.critical(f"Ошибка при генерации ответа от API: {e}")
        logger.debug("Stack trace:", exc_info=True)

    exit(1)