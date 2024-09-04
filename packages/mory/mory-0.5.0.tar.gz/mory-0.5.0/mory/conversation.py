import tempfile
import sys
import pytest
import os
import logging
import json
from venv import logger
from typing import Any
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Console
from prompt_toolkit import prompt
from colorama import init  # Добавлено для Windows поддержки
from .scan import scan, get_project_structure
from .run_tests import run_tests, get_coverage
from .helpers import get_string_size_kb, bindings, read_file_content, style, num_tousend_tokens_from_messages
from .config_loader import role_system_content, additional_user_content
from .chat.complection import chat_completion_request

# Инициализация colorama для Windows
init()

console = Console()

def crud_files(arguments: Any, project_abspath: str):
    arguments = json.loads(arguments)
    result = []
    skip_question = False
    operations = {
        'create': ('создан', 'w'),
        'read': ('прочитан', None),
        'update': ('обновлен', 'w'),
        'delete': ('удален', None)
    }

    for file in arguments['files']:
        filename = file['filename']
        file_path = os.path.join(project_abspath, filename)
        content = file.get('content', '')
        operation = file['operation']

        if operation in operations:
            action, mode = operations[operation]

            if operation == 'create':
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if operation == 'delete':
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:
                    action = "не существует"

            if mode:
                with open(file_path, mode, encoding='utf-8') as f:
                    f.write(content)

            if operation == 'read':
                content = read_file_content(file_path)
                result.append(f"{filename}: {content}")
                skip_question = True
            else:
                result.append(f"{filename}: {action}") ## не менять!!

            logger.info(f"{filename}: {action}")
    result_str = "\n".join(result)
    return result_str, skip_question

def scan_project(need_scan: bool, root_folder: str, save_to_file: bool, structure_only: bool) -> str:
    if not need_scan:
        return ""
    if structure_only:
        return get_project_structure(root_folder)
    else:
        scan_result = scan(root_folder)
        logging.info(f"Сканирование завершено. Размер в килобайтах: {get_string_size_kb(scan_result):.2f} KB.")
        if save_to_file:
            temp_dir = tempfile.mkdtemp()
            scan_file_path = os.path.join(temp_dir, f"{os.path.basename(root_folder)}.md")
            with open(scan_file_path, 'w', encoding='utf-8') as f:
                f.write(scan_result)
            logging.info(f"Результат сканирования сохранен в: {scan_file_path}")
        return scan_result

def initialize_messages(scan_result: str, root_folder: str) -> list:
    messages = []
    if role_system_content:
        messages.append({"role": "system", "content": role_system_content})
        console.print(Panel(role_system_content, title="[green]System Message[/green]"))

    if additional_user_content:
        messages.append({"role": "user", "content": additional_user_content})
        console.print(Panel(additional_user_content, title="[green]Additional User Message[/green]", subtitle="Будет добавляться перед каждым вашим запросом"))

    if scan_result:
        messages.append({"role": "system", "content": f"Работа ведется над проектом: {scan_result}."})
        console.print(Panel(f"Работа ведется над проектом: {os.path.abspath(root_folder)}", title="[green]Project Path[/green]"))

    return messages

def set_marker():
    sys.stdout.write('\x1b[s')

# Удаляем всё до маркера
def clear_to_marker():
    sys.stdout.write('\x1b[u')  # Вернуться к сохранённой позиции курсора
    sys.stdout.write('\x1b[J')  # Очистить всё ниже курсора

def handle_user_interaction(messages: list) -> str:
    set_marker()
    role_user_content = prompt([('class:prompt', 'Запрос: ')], multiline=True, key_bindings=bindings, style=style)
    clear_to_marker()
    console.print(Panel(f"{role_user_content}", title="[green]User Query[/green]"))
    messages.append({"role": "user", "content": role_user_content})
    return role_user_content

def process_tool_calls(messages, assistant_message: dict, project_abspath: str):
    if not assistant_message.tool_calls:
        return False

    skip_user_question = False

    def handle_crud_files(tool):
        result, skip = crud_files(tool.function.arguments, project_abspath)
        messages.append({
            "tool_call_id": tool.id,
            "role": "tool",
            "name": 'save_files',
            "content": result,
        })
        return skip

    def handle_run_test(tool):
        logging.info("Запускаем тесты")
        tests_exit_code, test_output = run_tests()
        messages.append({
            "tool_call_id": tool.id,
            "role": "tool",
            "name": 'run_test',
            "content": test_output,
        })
        return tests_exit_code != pytest.ExitCode.OK

    def handle_skip_user_question(tool):
        logging.info("Пропускаем запрос пользователя")
        messages.append({
            "tool_call_id": tool.id,
            "role": "tool",
            "name": 'run_test',
            "content": "ок, пользователя ни очем не спросили",
        })
        return True

    handlers = {
        'crud_files': handle_crud_files,
        'save_files': handle_crud_files,
        'run_test': handle_run_test,
        'skip_user_question': handle_skip_user_question,
    }

    for tool in assistant_message.tool_calls:
        if tool.function.name in handlers:
            skip_user_question += handlers[tool.function.name](tool)

    for tool in assistant_message.tool_calls:
        if tool.function.name == 'multi_tool_use':
            tool_uses = json.loads(tool.function.arguments)['tool_uses']
            for use in tool_uses:
                func_name = use['recipient_name'].replace("functions.", "")
                if func_name in handlers:
                    skip_user_question += handlers[func_name](tool_uses)

    return skip_user_question

def conversation(need_scan: bool, root_folder: str, save_to_file: bool, structure_only: bool) -> None:
    try:
        scan_result = scan_project(need_scan, root_folder, save_to_file, structure_only)
        project_abspath = os.path.abspath(root_folder)
        messages = initialize_messages(scan_result, root_folder)
        skip_user_question = False

        while True:
            num_tousend_tokens_from_messages(messages)

            if not skip_user_question:
                handle_user_interaction(messages)
            else:
                skip_user_question = False

            chat_response = chat_completion_request(messages)
            assistant_message = chat_response.choices[0].message
            messages.append(assistant_message)

            if assistant_message.content:
                console.print(Panel(Markdown(assistant_message.content), title="[green]GPT answer[/green]"))

            skip_user_question = process_tool_calls(messages, assistant_message, project_abspath)
    except KeyboardInterrupt:
        logging.info("Закончили")
    finally:
        logging.info("Сессия завершена")
