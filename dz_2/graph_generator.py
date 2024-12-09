import os
import zlib
from graphviz import Digraph


def read_git_object(repo_path, object_hash):
    """Чтение и распаковка объекта Git."""
    object_dir = os.path.join(repo_path, ".git", "objects", object_hash[:2])
    object_file = os.path.join(object_dir, object_hash[2:])
    
    if not os.path.exists(object_file):
        raise FileNotFoundError(f"Git object {object_hash} not found.")
    
    with open(object_file, "rb") as f:
        compressed_data = f.read()
    
    decompressed_data = zlib.decompress(compressed_data)
    return decompressed_data.decode("utf-8", errors="replace")


def parse_commit_object(commit_data):
    """Парсинг содержимого коммита для извлечения родительских коммитов."""
    lines = commit_data.split("\n")
    parents = []
    message = None
    for line in lines:
        if line.startswith("parent "):
            parents.append(line.split(" ")[1])
        elif not line.startswith(("tree ", "author ", "committer ")) and line.strip():
            if message is None:
                message = line.strip()
    return parents, message


def list_git_objects(repo_path):
    """Получение списка всех объектов в репозитории."""
    objects_path = os.path.join(repo_path, ".git", "objects")
    objects = []
    
    for dirpath, _, filenames in os.walk(objects_path):
        for filename in filenames:
            if len(filename) == 38:  # Убедимся, что это объект Git (SHA-1 хэш)
                relative_path = os.path.relpath(os.path.join(dirpath, filename), objects_path)
                objects.append(relative_path.replace("\\", ""))
    return objects


def analyze_commits(repo_path):
    """Анализ всех объектов commit в репозитории."""
    objects = list_git_objects(repo_path)
    commit_dependencies = {}
    commit_messages = {}
    
    for object_hash in objects:
        try:
            data = read_git_object(repo_path, object_hash)
            if data.startswith("commit "):
                # Парсим объект коммита
                parents, message = parse_commit_object(data)
                commit_dependencies[object_hash] = parents
                commit_messages[object_hash] = message
        except Exception as e:
            # Игнорируем ошибки (например, если объект не является коммитом)
            continue
    
    return commit_dependencies, commit_messages


def generate_dependency_graph(commit_dependencies, commit_messages):
    """Создание графа зависимостей коммитов."""
    graph = Digraph(comment="Commit Dependency Graph", format="dot")
    
    for commit, parents in commit_dependencies.items():
        graph.node(commit, label=commit_messages.get(commit, "No message")[:50])
        for parent in parents:
            graph.edge(parent, commit)
    
    return graph.source


# Пример вызова функций
repository_path = "E:/dz_olesia/dz_2"  # Путь к репозиторию

commit_dependencies, commit_messages = analyze_commits(repository_path)
graph_source = generate_dependency_graph(commit_dependencies, commit_messages)
print(graph_source)

# Запись графа в файл
output_file_path = "E:/dz_olesia/output.dot"
with open(output_file_path, "w", encoding="utf-8") as f:
    f.write(graph_source)
