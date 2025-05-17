# logging_config.py

import logging
import logging.config
import json

def setup_logging_from_json(json_path, default_level=logging.DEBUG):
    """
    Загружает и настраивает логирование из JSON-файла.
    """
    try:
        with open(json_path, 'r') as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    except Exception as e:
        print(f"Ошибка при загрузке конфигурации логирования: {e}")
        # В случае ошибки, настроим логирование с уровнем по умолчанию
        logging.basicConfig(level=default_level)
        print(f"Используется конфигурация по умолчанию (уровень: {default_level})")

