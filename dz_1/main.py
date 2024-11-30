import os
import zipfile
import tkinter as tk
from tkinter import scrolledtext
from pathlib import Path
from datetime import datetime

# Глобальные переменные для виртуальной файловой системы
vfs = {}
current_path = "/"

# Лог-файл
log_entries = []

def log_action(command, result=""):
    """Логирование действий."""
    timestamp = datetime.now().isoformat()
    log_entries.append(f"{timestamp} - Command: {command}, Result: {result}")


def save_log(log_path):
    """Сохранить лог в текстовый файл."""
    with open(log_path, "w") as f:
        f.write("\n".join(log_entries))


def load_vfs(zip_path):
    """Загрузка виртуальной файловой системы из ZIP-архива."""
    global vfs, current_path
    with zipfile.ZipFile(zip_path, 'r') as z:
        for file_name in z.namelist():
            if file_name.endswith('/'):
                vfs[file_name] = {"type": "dir", "permissions": "rwx"}
            else:
                vfs[file_name] = {
                    "type": "file",
                    "content": z.read(file_name),
                    "permissions": "rw"
                }

    # Установим корневую директорию как первую общую папку
    root_dirs = {key.split('/')[0] for key in vfs.keys() if key}
    if len(root_dirs) == 1:
        current_path = f"{root_dirs.pop()}/"
    else:
        current_path = "/"

    print("Loaded VFS structure:")
    for path, meta in vfs.items():
        print(f"{path}: {meta}")
    print(f"Current VFS root set to: {current_path}")



def list_directory():
    """Отображение содержимого текущей директории."""
    global current_path
    entries = [
        f[len(current_path):].split("/", 1)[0]
        for f in vfs
        if f.startswith(current_path) and f != current_path
    ]
    entries = sorted(set(entries))
    return "\n".join(entries) if entries else "No files or directories found."



def change_directory(path):
    global current_path
    if path == "..":
        if current_path == "/":
            return "Already at root."  # Корректный возврат при попытке выйти из корня
        current_path = "/".join(current_path.strip("/").split("/")[:-1]) + "/"
        if current_path == "":
            current_path = "/"
        return f"Changed directory to: {current_path}"
    elif path.startswith("/"):
        new_path = path if path.endswith("/") else path + "/"
    else:
        new_path = os.path.join(current_path, path).replace("\\", "/")
        if not new_path.endswith("/"):
            new_path += "/"

    if new_path in vfs and vfs[new_path]["type"] == "dir":
        current_path = new_path
        return f"Changed directory to: {current_path}"
    else:
        return "Directory does not exist."

def reverse_string(s):
    reversed_str = s[::-1]
    return f"Reversed: {reversed_str}"


def chmod_file(filename, mode):
    file_path = os.path.join(current_path, filename).replace("\\", "/")
    if file_path in vfs:
        vfs[file_path]["permissions"] = mode
        return f"Changed permissions of {filename} to {mode}."
    else:
        return "Error: File or directory not found."



def process_command(command):
    """Обработка пользовательских команд."""
    try:
        if command == "exit":
            app.quit()
        elif command == "ls":
            return list_directory()
        elif command.startswith("cd "):
            args = command.split()
            if len(args) != 2:
                return "Usage: cd <directory>"
            return change_directory(args[1])
        elif command.startswith("rev "):
            args = command.split()
            if len(args) != 2:
                return "Usage: rev <filename>"
            return reverse_string(args[1])
        elif command.startswith("chmod "):
            args = command.split()
            if len(args) != 3:
                return "Usage: chmod <filename> <mode>"
            return chmod_file(args[1], args[2])
        else:
            return "Command not recognized."
    except Exception as e:
        return f"Error: {e}"


def on_enter(event):
    """Обработка ввода пользователя."""
    command = entry.get().strip()
    entry.delete(0, tk.END)
    result = process_command(command)
    log_action(command, result)
    output_box.configure(state="normal")
    output_box.insert(tk.END, f"{current_path}:> {command}\n{result}\n")
    output_box.configure(state="disabled")
    output_box.see(tk.END)


# GUI-приложение
app = tk.Tk()
app.title("Virtual Shell Emulator")
app.geometry("600x400")

frame = tk.Frame(app)
frame.pack(pady=10)

output_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20)
output_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
output_box.configure(state="disabled")

entry = tk.Entry(frame, width=80)
entry.pack(side=tk.BOTTOM, pady=5)
entry.bind('<Return>', on_enter)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Virtual Shell Emulator")
    parser.add_argument("--vfs", required=True, help="Path to the virtual filesystem zip")
    parser.add_argument("--log", required=True, help="Path to save the log file")
    args = parser.parse_args()

    # Загрузка виртуальной файловой системы
    load_vfs(args.vfs)

    # Сохранение лога при выходе
    app.protocol("WM_DELETE_WINDOW", lambda: (save_log(args.log), app.destroy()))

    print("Welcome to the Virtual Shell Emulator!")
    app.mainloop()
