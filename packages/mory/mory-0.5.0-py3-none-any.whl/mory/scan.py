import os
import fnmatch
import logging
from pathlib import Path
from .config_loader import load_config, is_development_mode
from .helpers import read_file_content
from typing import List

logger = logging.getLogger(__name__)

config, _ = load_config()
text_extensions = set(config['text_extensions'])

def get_ignore_patterns_paths(root_folder: str) -> List[str]:
    """Возвращает пути к файлам игнорирования."""
    ignore_pattern_files = config['ignore_pattern_files']
    ignore_files_paths = []

    for file in ignore_pattern_files:
        expanded_path = os.path.expanduser(file)
        root_path = os.path.join(root_folder, file)

        if os.path.exists(root_path):
            ignore_files_paths.append(root_path)
        elif os.path.exists(expanded_path):
            ignore_files_paths.append(expanded_path)

    if is_development_mode():
        dev_ignore_path = os.path.join(os.getcwd(), 'templates', '.gptignore')
        ignore_files_paths.append(dev_ignore_path)

    return ignore_files_paths

def read_ignore_file(ignore_files_paths: List[str]) -> List[str]:
    """Читает файлы паттернов игнорирования и возвращает список паттернов."""
    ignore_patterns = []
    for path in ignore_files_paths:
        try:
            with open(path, 'r') as file:
                ignore_patterns.extend(file.read().splitlines())
        except IOError as e:
            logger.error(f"Не удалось прочитать файл {path}: {e}", exc_info=True)
    return ignore_patterns

def should_ignore(path: str, patterns: List[str]) -> bool:
    """Определяет, следует ли игнорировать файл на основе заданных паттернов."""
    # Преобразуем путь в объект Path
    path_obj = Path(path)
    # Получаем имя родительской папки или текущей папки, если родительская папка пустая
    check_obj = path_obj.parent.name or path_obj.name

    # Проверка совпадения родительской папки или полного пути с любым из шаблонов
    for pattern in patterns:
        if fnmatch.fnmatch(check_obj, pattern) or fnmatch.fnmatch(path_obj.name, pattern):
            return True

        # Дополнительная проверка для директорий
        if path_obj.is_relative_to(Path.cwd()):  # Если путь относительный и в текущей директории
            if any(fnmatch.fnmatch(check_obj, f"{pattern}*") for pattern in patterns):
                return True

    return False

def is_text_file(file_path: str) -> bool:
    """Проверяет, является ли файл текстовым на основе его расширения и содержимого."""
    _, ext = os.path.splitext(file_path)
    if ext in text_extensions:
        return True

    try:
        with open(file_path, 'rb') as file:
            chunk = file.read(1024)
            if b'\0' in chunk:
                return False

            try:
                chunk.decode('utf-8', errors='ignore')
                return True
            except (UnicodeDecodeError, IOError) as e:
                logger.error(f"Ошибка при чтении файла {file_path}: {e}", exc_info=True)
                return False
    except IOError as e:
        logger.error(f"Файл не может быть открыт: {file_path}: {e}", exc_info=True)
        return False

def get_text_files(root: str, ignore_patterns: List[str]) -> List[str]:
    """Возвращает список текстовых файлов, исключая игнорируемые."""
    text_files = []
    try:
        for dirpath, dirnames, filenames in os.walk(root):
            new_dirnames = [d for d in dirnames if not should_ignore(os.path.relpath(os.path.join(dirpath, d), root), ignore_patterns)]
            for dirname in list(dirnames):  # Клонируем оригинальный dirnames и удаляем содержимое из копии
                if dirname not in new_dirnames:
                    dirnames.remove(dirname)
            for filename in filenames:
                relpath = os.path.relpath(os.path.join(dirpath, filename), root)
                full_path = os.path.join(root, relpath)
                if not should_ignore(relpath, ignore_patterns) and is_text_file(full_path):
                    text_files.append(relpath)
    except Exception as e:
        logger.error(f"При сканировании возникла ошибка: {e}", exc_info=True)
    return text_files

def scan(root_folder: str) -> str:
    """Сканирует папку и возвращает содержимое всех текстовых файлов."""
    ignore_files_paths = get_ignore_patterns_paths(root_folder)
    logger.info(f"Файлы для для поиска паттернов игнорирования: {ignore_files_paths}")
    ignore_patterns = read_ignore_file(ignore_files_paths)
    logger.info(f"Паттерны для игнорирования: {ignore_patterns}")

    text_files = get_text_files(root_folder, ignore_patterns)
    logger.info(f"Файлы для сканирования: {text_files}")

    scan_result = "\n".join(
        f"{file}\n```\n{read_file_content(os.path.join(root_folder, file))}\n```"
        for file in text_files
    )

    return scan_result

def get_project_structure(root_folder: str) -> str:
    """Возвращает структуру проекта."""
    ignore_files_paths = get_ignore_patterns_paths(root_folder)
    logger.info(f"Файлы для для поиска паттернов игнорирования: {ignore_files_paths}")
    ignore_patterns = read_ignore_file(ignore_files_paths)
    logger.info(f"Паттерны для игнорирования: {ignore_patterns}")

    project_structure = []

    try:
        for dirpath, dirnames, filenames in os.walk(root_folder):
            new_dirnames = [d for d in dirnames if not should_ignore(os.path.relpath(os.path.join(dirpath, d), root_folder), ignore_patterns)]

            for dirname in list(dirnames):  # Клонируем оригинальный dirnames и удаляем содержимое из копии
                if dirname not in new_dirnames:
                    dirnames.remove(dirname)

            for filename in filenames:
                relpath = os.path.relpath(os.path.join(dirpath, filename), root_folder)
                if not should_ignore(relpath, ignore_patterns):
                    project_structure.append(relpath)

    except Exception as e:
        logger.error(f"При сканировании структуры возникла ошибка: {e}", exc_info=True)

    return "\n".join(project_structure)
