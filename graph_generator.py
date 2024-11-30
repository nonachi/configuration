import subprocess
from graphviz import Digraph

def get_commits(repository_path, file_hash):
    """Получение списка коммитов, связанных с файлом."""
    try:
        # Запуск git log для получения коммитов
        result = subprocess.run(
            ["git", "-C", repository_path, "log", "--pretty=format:%H %s", "--all", "--", file_hash],
            capture_output=True,
            text=True,
            check=True
        )
        # Обработка вывода git log
        commits = result.stdout.strip().split("\n")
        
        # Парсим только строки с двумя частями (хэш и сообщение)
        parsed_commits = []
        for line in commits:
            if " " in line:
                commit_hash, message = line.split(" ", 1)
                parsed_commits.append((commit_hash, message))

        return parsed_commits
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ошибка при выполнении git log: {e}")

def get_commit_dependencies(repository_path, commit_hash):
    """Получение родительских коммитов для текущего коммита."""
    try:
        result = subprocess.run(
            ["git", "-C", repository_path, "log", "--pretty=%P", "-n", "1", commit_hash],
            capture_output=True,
            text=True,
            check=True
        )
        parents = result.stdout.strip().split()
        return parents if parents else []  # Возвращаем пустой список, если нет родителей
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ошибка при выполнении git log для коммита {commit_hash}: {e}")

def generate_dependency_graph(repository_path, file_hash):
    """Создание графа зависимостей на основе коммитов для заданного файла."""
    commits = get_commits(repository_path, file_hash)
    graph = Digraph(comment="Dependency Graph", format="dot")
    
    # Добавляем узлы для каждого коммита
    for commit_hash, message in commits:
        graph.node(commit_hash, label=message)
        
        # Получаем родительские коммиты
        parents = get_commit_dependencies(repository_path, commit_hash)
        
        # Добавляем ребра (зависимости) от родителей к текущему коммиту
        for parent in parents:
            graph.edge(parent, commit_hash)
    
    return graph.source

# Пример вызова функции
repository_path = "E:/dz_olesia/dz_2"
file_hash = "example.txt"

graph_source = generate_dependency_graph(repository_path, file_hash)
print(graph_source)

# Запись в файл, если необходимо
output_file_path = "E:/dz_olesia/output.dot"
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(graph_source)
