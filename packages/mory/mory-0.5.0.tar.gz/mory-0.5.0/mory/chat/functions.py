functions = [
    {
        "type": "function",
        "function": {
            "name": "crud_files",
            "description": "Функция для сохранения нескольких файлов на диск",
            "parameters": {
                "type": "object",
                "properties": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "filename": {
                                    "type": "string",
                                    "description": "Название файла"
                                },
                                "content": {
                                    "type": "string",
                                    "description": "Содержимое файла"
                                },
                                "operation": {
                                    "type": "string",
                                    "enum": ["create", "read", "update","delete"],
                                    "description": """Тип операции с файлом:
                                    - create: Создание файла.
                                    - read: Чтение файла.
                                    - update: Обновление файла.
                                    - delete: Удаление файла."""
                                }
                            },
                            "required": ["filename", "content", "operation"]
                        },
                        "description": "Массив объектов, каждый из которых представляет файл с названием и содержимым"
                    }
                },
                "required": ["files"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_test",
            "description": "Функция для запуска тестов в проекте",
            "parameters": {
                "type": "object",
                "properties": {
                    "results": {
                        "type": "string",
                        "description": "Результаты выполения тестов"
                    },
                },
                "required": ["results"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "skip_user_question",
            "description": "Функция для пропуска запроса от пользоватея, например когда тебе надо обновить файлы и запустить тесты несколько раз",
            "parameters": {
                "type": "object",
                "properties": {
                    "skip": {
                        "type": "string",
                        "enum": ["True", "False"],
                        "description": "Нужно ли пользователю что-то писать или можно пропустить диалог с ним для получения результата"
                    },
                },
                "required": ["skip"]
            }
        }
    }
]