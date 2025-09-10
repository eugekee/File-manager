import os
import re
import shutil
from datetime import datetime


def create_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
        return f"Папка создана: {path}"
    except Exception as e:
        raise Exception(f"Ошибка при создании папки: {str(e)}")


def delete_path(path):
    try:
        if not os.path.exists(path):
            return "Указанный путь не существует"

        if os.path.isfile(path):
            os.remove(path)
            return f"Файл удален: {path}"
        else:
            shutil.rmtree(path)
            return f"Папка удалена: {path}"
    except Exception as e:
        raise Exception(f"Ошибка при удалении: {str(e)}")


def find_files_by_regex(path, pattern, recursive=False):
    try:
        regex = re.compile(pattern)
        found_items = []

        if recursive:
            for root, dirs, files in os.walk(path):
                for name in dirs + files:
                    if regex.search(name):
                        full_path = os.path.join(root, name)
                        found_items.append(full_path)
        else:
            for item in os.listdir(path):
                if regex.search(item):
                    full_path = os.path.join(path, item)
                    found_items.append(full_path)

        return found_items
    except re.error as e:
        raise Exception(f"Ошибка в регулярном выражении: {str(e)}")
    except Exception as e:
        raise Exception(f"Ошибка при поиске: {str(e)}")


def add_date_to_filenames(path, recursive=False):
    try:
        processed_files = []

        if recursive:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    dir_name = os.path.dirname(file_path)
                    file_name, file_ext = os.path.splitext(file)
                    new_name = f"{file_name}_{datetime.now().strftime('%d_%m_%Y')}{file_ext}"
                    new_path = os.path.join(dir_name, new_name)
                    os.rename(file_path, new_path)
                    processed_files.append(new_path)
        else:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    dir_name = os.path.dirname(item_path)
                    file_name, file_ext = os.path.splitext(item)
                    new_name = f"{file_name}_{datetime.now().strftime('%d_%m_%Y')}{file_ext}"
                    new_path = os.path.join(dir_name, new_name)
                    os.rename(item_path, new_path)
                    processed_files.append(new_path)

        return processed_files
    except Exception as e:
        raise Exception(f"Ошибка при добавлении даты: {str(e)}")


def get_info(path):
    try:
        if not os.path.exists(path):
            return "Путь не существует"

        if os.path.isfile(path):
            size = os.path.getsize(path)
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            return f"Файл: {path}\nРазмер: {size} байт\nПоследнее изменение: {mtime.strftime('%d-%m-%Y')}"
        elif os.path.isdir(path):
            num_files = 0
            num_dirs = 0
            total_size = 0

            for root, dirs, files in os.walk(path):
                num_dirs += len(dirs)
                num_files += len(files)
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        total_size += os.path.getsize(file_path)

            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            return f"Папка: {path}\nРазмер: {total_size} байт\nПодпапок: {num_dirs}\nФайлов: {num_files}\nПоследнее изменение: {mtime.strftime('%d-%m-%Y')}"
        else:
            return "Неизвестный тип объекта"
    except Exception as e:
        raise Exception(f"Ошибка при получении информации: {str(e)}")


def sort_contents(path, reverse=False):
    try:
        if not os.path.exists(path):
            raise Exception("Путь не существует")
        if not os.path.isdir(path):
            raise Exception("Указанный путь не является папкой")

        items = []
        for name in os.listdir(path):
            full_path = os.path.join(path, name)
            is_dir = os.path.isdir(full_path)
            items.append((name, is_dir))
        items.sort(key=lambda x: (not x[1], x[0].lower()), reverse=reverse)
        return items
    except Exception as e:
        raise Exception(f"Ошибка при сортировке: {str(e)}")