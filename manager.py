import argparse
from funcs import *

def main():
    parser = argparse.ArgumentParser(description='Менеджер файловой системы')
    subparsers = parser.add_subparsers(dest='command')


    parser_create = subparsers.add_parser('create', help='Создать папку')
    parser_create.add_argument('path', help='Путь к новой папке')


    parser_delete = subparsers.add_parser('delete', help='Удалить файл или папку')
    parser_delete.add_argument('path', help='Путь к файлу или папке')


    parser_find = subparsers.add_parser('find', help='Поиск файлов по регулярному выражению')
    parser_find.add_argument('folder', help='Папка для поиска')
    parser_find.add_argument('pattern', help='Регулярное выражение')


    parser_rename = subparsers.add_parser('adddate', help='Добавить дату создания к именам файлов')
    parser_rename.add_argument('path', help='Файл или папка')
    parser_rename.add_argument('--recursive', action='store_true', help='Рекурсивно проходить по папкам')

    args = parser.parse_args()

    try:
        if args.command == 'create':
            print(create_folder(args.path))
        elif args.command == 'delete':
            print(delete_path(args.path))
        elif args.command == 'find':
            result = find_files_by_regex(args.folder, args.pattern)
            print('\n'.join(result) if result else "Файлы не найдены.")
        elif args.command == 'adddate':
            results = add_date_to_filenames(args.path, recursive=args.recursive)
            print("Переименовано:\n" + '\n'.join(results))
        else:
            parser.print_help()
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()