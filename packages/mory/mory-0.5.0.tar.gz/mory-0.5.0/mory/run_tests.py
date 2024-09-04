import subprocess
import sys
import pytest
import io
import logging
from contextlib import redirect_stdout


def run_tests():
    test_dir = "./tests"
    _output = io.StringIO()
    with redirect_stdout(_output):
        result = pytest.main([test_dir, "-v"])

    output = _output.getvalue()
    _output.close()

    logging.info(get_test_result_description(result))
    return result, output

def get_test_result_description(result):
    description = ""
    if result == pytest.ExitCode.OK:
        description ="Все тесты успешно пройдены."
    elif result == pytest.ExitCode.TESTS_FAILED:
        description = "Некоторые тесты завершились с ошибками."
    elif result == pytest.ExitCode.INTERRUPTED:
        description = "Тесты были прерваны."
    elif result == pytest.ExitCode.INTERNAL_ERROR:
        description = "Произошла внутренняя ошибка pytest."
    elif result == pytest.ExitCode.USAGE_ERROR:
        description ="Ошибка использования pytest."
    else:
        description = "Произошла неизвестная ошибка."
    return description

def get_coverage():
    test_dir = "./tests"
    command = ["pytest", test_dir, "--cov=mory", "--cov-report=term-missing"]

    # Запускаем pytest в отдельном процессе
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate()

    exit_code = process.returncode  # Код возврата
    output = stdout + stderr  # Комбинируем вывод и ошибки

    return exit_code, output