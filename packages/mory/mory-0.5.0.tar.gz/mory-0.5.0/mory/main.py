import argparse
import logging
import os
from rich import print
from prompt_toolkit import prompt
from typing import Union

from mory.run_tests import get_coverage
from .helpers import check_api_key, bindings, style
from .conversation import conversation
from .config_loader import log_level, open_config_file
from .version import PROGRAM_NAME, PROGRAM_VERSION

logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description="Сканирование папки и отправка в gpt")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    scan_parser = subparsers.add_parser("scan", help="Сканирование директории")
    scan_parser.add_argument("-p", "--path", type=str, help="Путь к сканируемой директории")
    scan_parser.add_argument("-f", "--save-to-file", action="store_true", help="Сохранить результат сканирования во временную папку перед отправкой")
    scan_parser.add_argument("-s", "--structure-only", action="store_true", help="Составить только структуру проекта")
    scan_parser.add_argument("-g", "--git-skip", action="store_true", help="Пропустить проверку на наличие git в проекте")

    subparsers.add_parser("config", help="Открыть файл конфигурации")

    parser.add_argument('-v', '--version', action='version', version=f"%(prog)s {PROGRAM_VERSION}")
    return parser.parse_args()

def get_root_folder(path: Union[str, None]) -> str:
    if path:
        root_folder = path.strip()
    else:
        root_folder = prompt([('class:prompt', 'Введите путь к папке для сканирования: ')], key_bindings=bindings, style=style)

    return root_folder or os.getcwd()

def handle_config_command():
    open_config_file()

def handle_scan_command(args: argparse.Namespace):
    try:
        root_folder = get_root_folder(args.path)

        if not os.path.isdir(root_folder):
            logger.error(f"Ошибка: Путь '{root_folder}' не является директорией.")
            exit()

        if not args.structure_only and not args.git_skip:
            git_path = os.path.join(root_folder, ".git")
            if not os.path.exists(git_path):
                print("[bold yellow]В проекте не найден git, файлы могут быть перезаписаны безвозвратно[/bold yellow]")
                try:
                    confirmation = prompt([('class:prompt', 'Уверены? (да/НЕТ): ')], key_bindings=bindings, style=style, default="НЕТ")
                    if confirmation.lower() != "да":
                        logger.info("Сканирование отменено пользователем.")
                        return
                except AttributeError:
                    logger.info("Сессия окончена")
                    exit()

        logger.info(f"Сканируем папку: {os.path.abspath(root_folder)}")
        conversation(True, root_folder, args.save_to_file, args.structure_only)
    except Exception as e:
        logger.error(f"Ошибка при выполнении команды сканирования: {e}", exc_info=True)

def main() -> None:
    args = parse_args()

    check_api_key()

    if not args.command:
        logger.error("Команда не распознана")
        return

    command_handlers = {
        "config": lambda args: handle_config_command(),
        "scan": handle_scan_command,
    }

    handler = command_handlers.get(args.command, None)
    if handler:
        handler(args)
    else:
        logger.error("Команда не распознана")

if __name__ == '__main__':
    # get_coverage()
    main()
