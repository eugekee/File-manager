import os
import shutil
import re
from datetime import datetime

def create_folder(path):
    os.makedirs(path, exist_ok=True)
    return f"Папка создана: {path}"

def delete_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
        return f"Папка удалена: {path}"
    elif os.path.isfile(path):
        os.remove(path)
        return f"Файл удалён: {path}"
    else:
        raise FileNotFoundError(f"Не найден файл/папка: {path}")

def find_files_by_regex(folder, pattern):
    matches = []
    prog = re.compile(pattern)
    for root, _, files in os.walk(folder):
        for f in files:
            if prog.search(f):
                matches.append(os.path.join(root, f))
    return matches

def add_date_to_filenames(path, recursive=False):
    def add_date(file_path):
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