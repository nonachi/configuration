import csv
import os
import sys
from graph_generator import generate_dependency_graph
import io

# Устанавливаем кодировку utf-8 для вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def read_config(config_path):
    """Чтение конфигурационного файла."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Конфигурационный файл {config_path} не найден.")
    
    with open(config_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader, None)  # Пропуск заголовков, если есть
        config = next(reader)
        return {
            "visualization_tool_path": config[0],
            "repository_path": config[1],
            "output_file_path": config[2],
            "file_hash": config[3]
        }

def main(config_path):
    config = read_config(config_path)
    
    # Проверка наличия репозитория
    if not os.path.isdir(config["repository_path"]):
        raise FileNotFoundError(f"Репозиторий {config['repository_path']} не найден.")
    
    # Генерация графа зависимостей
    graph_code = generate_dependency_graph(
        repository_path=config["repository_path"],
        file_hash=config["file_hash"]
    )
    
    # Сохранение результата
    with open(config["output_file_path"], mode='w', encoding='utf-8') as file:
        file.write(graph_code)
    
    print(f"Граф зависимостей сохранён в {config['output_file_path']}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python visualizer.py <путь_к_конфигурационному_файлу>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    main(config_path)
