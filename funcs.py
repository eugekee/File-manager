import os
import shutil
import re
from datetime import datetime
from typing import List, Tuple


def create_folder(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return f"Папка создана: {path}"


def delete_path(path: str) -> str:
    if os.path.isdir(path):
        shutil.rmtree(path)
        return f"Папка удалена: {path}"
    elif os.path.isfile(path):
        os.remove(path)
        return f"Файл удалён: {path}"
    else:
        raise FileNotFoundError(f"Не найден файл/папка: {path}")


def find_files_by_regex(folder: str, pattern: str) -> List[str]:
    matches = []
    try:
        prog = re.compile(pattern)
        for root, _, files in os.walk(folder):
            for f in files:
                if prog.search(f):
                    matches.append(os.path.join(root, f))
    except re.error:
        raise ValueError("Неверное регулярное выражение")
    return matches


def add_date_to_filenames(path: str, recursive: bool = False) -> List[str]:
    def add_date(file_path: str) -> str:
        ctime = os.path.getctime(file_path)
        date_str = datetime.fromtimestamp(ctime).strftime("%Y%m%d")
        dirname, filename = os.path.split(file_path)
        new_filename = f"{date_str}_{filename}"
        new_path = os.path.join(dirname, new_filename)
        os.rename(file_path, new_path)
        return new_path

    results = []
    if os.path.isfile(path):
        results.append(add_date(path))
    elif os.path.isdir(path):
        if recursive:
            for root, _, files in os.walk(path):
                for f in files:
                    results.append(add_date(os.path.join(root, f)))
        else:
            for f in os.listdir(path):
                full = os.path.join(path, f)
                if os.path.isfile(full):
                    results.append(add_date(full))
    else:
        raise FileNotFoundError(f"Не найден файл/папка: {path}")
    return results


def get_info(path: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Объект не найден: {path}")

    info = []
    if os.path.isfile(path):
        info.append(f"Файл: {path}")
        info.append(f"Размер: {os.path.getsize(path)} байт")
    else:
        info.append(f"Папка: {path}")
        count = sum(len(files) for _, _, files in os.walk(path))
        info.append(f"Количество файлов: {count}")

    info.append(f"Создан: {datetime.fromtimestamp(os.path.getctime(path))}")
    info.append(f"Изменён: {datetime.fromtimestamp(os.path.getmtime(path))}")
    return "\n".join(info)


def sort_contents(path: str, reverse: bool = False) -> List[Tuple[str, bool]]:
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Не является папкой: {path}")

    items = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        items.append((item, os.path.isdir(full_path)))

    return sorted(items, key=lambda x: x[0], reverse=reverse)