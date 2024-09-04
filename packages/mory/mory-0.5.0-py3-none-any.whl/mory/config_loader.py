import os
import yaml
import logging
from .version import PROGRAM_NAME
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)

def load_config() -> Tuple[Dict[str, Any], str]:
    if is_development_mode():
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        config_dir = os.path.join(parent_dir, 'templates')
    else:
        config_dir = os.path.join(os.path.expanduser('~'), '.config', PROGRAM_NAME)

    config_path = os.path.join(config_dir, 'config.yml')
    if not os.path.exists(config_path):
        logger.error(f"Конфигурационный файл не найден по пути: {config_path}")
        raise FileNotFoundError(f"Конфигурационный файл не найден по пути: {config_path}")

    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config, config_path
    except Exception as e:
        logger.error(f"Ошибка при загрузке конфигурации: {e}", exc_info=True)
        raise

def open_config_file() -> None:
    _, config_path = load_config()

    if config_path:
        os.system(f'open "{config_path}"' if os.name == 'posix' else f'start "" "{config_path}"')
    else:
        logger.error("Файл конфигурации не найден.")

def is_development_mode() -> bool:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    return os.path.isfile(os.path.join(parent_dir, 'setup.py'))

config, config_path = load_config()

gpt_model = config['gpt_model']
role = config['role']
role_system_content = role['system']['developer']['content']
additional_user_content = role['user']['additional_content']
log_level = config['log_level']
