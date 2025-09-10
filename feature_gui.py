import flet as ft
from funcs import *
import os
import re


def main(page: ft.Page):
    page.title = "File Manager"
    page.window.width = 900
    page.window.height = 700
    page.window.resizable = True
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = "adaptive"

    def show_snackbar(message: str, color: str = ft.Colors.RED):
        page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    def create_folder_click(e):
        try:
            if not path_input.value.strip():
                show_snackbar("Введите путь для создания папки")
                return

            result = create_folder(path_input.value)
            show_snackbar(result, ft.Colors.GREEN)
        except Exception as ex:
            show_snackbar(str(ex))

    def delete_path_click(e):
        try:
            if not path_input.value.strip():
                show_snackbar("Введите путь для удаления")
                return

            result = delete_path(path_input.value)
            show_snackbar(result, ft.Colors.GREEN)
        except Exception as ex:
            show_snackbar(str(ex))

    def find_files_click(e):
        try:
            if not path_input.value.strip():
                show_snackbar("Введите путь для поиска")
                return

            if not os.path.exists(path_input.value):
                show_snackbar("Указанная папка не существует")
                return

            if not os.path.isdir(path_input.value):
                show_snackbar("Указанный путь не является папкой")
                return

            if not pattern_input.value.strip():
                show_snackbar("Введите регулярное выражение")
                return

            try:
                re.compile(pattern_input.value)
            except re.error as e:
                show_snackbar(f"Ошибка в регулярном выражении: {e}")
                return

            results = find_files_by_regex(path_input.value, pattern_input.value, recursive_check.value)
            result_view.controls.clear()

            if results:
                result_view.controls.append(
                    ft.Row([
                        ft.Icon(ft.Icons.SEARCH, color=ft.Colors.BLUE),
                        ft.Text(f"Найдено {len(results)} элементов:",
                                weight="bold", size=16)
                    ])
                )

                for item_path in results:
                    is_dir = os.path.isdir(item_path)
                    icon = ft.Icons.FOLDER if is_dir else ft.Icons.DESCRIPTION
                    color = ft.Colors.AMBER if is_dir else ft.Colors.BLUE
                    item_card = ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(icon, color=color),
                                    title=ft.Text(os.path.basename(item_path),
                                                  weight="bold"),
                                    subtitle=ft.Text(item_path,
                                                     size=12,
                                                     color=ft.Colors.GREY),
                                ),
                                ft.Row([
                                    ft.TextButton(
                                        "Копировать путь",
                                        icon=ft.Icons.CONTENT_COPY,
                                        on_click=lambda e, path=item_path: page.set_clipboard(path)
                                    ),
                                ], alignment=ft.MainAxisAlignment.END)
                            ]),
                            padding=10,
                        ),
                        elevation=2,
                        margin=ft.margin.only(bottom=10)
                    )

                    result_view.controls.append(item_card)
            else:
                result_view.controls.append(
                    ft.Column([
                        ft.Icon(ft.Icons.SEARCH_OFF, size=48, color=ft.Colors.GREY),
                        ft.Text("Элементы, соответствующие шаблону, не найдены",
                                size=16, color=ft.Colors.GREY)
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )

            page.update()
        except Exception as ex:
            show_snackbar(f"Ошибка при поиске: {str(ex)}")

    def add_date_click(e):
        try:
            if not path_input.value.strip():
                show_snackbar("Введите путь для добавления даты")
                return

            results = add_date_to_filenames(path_input.value, recursive_check.value)
            show_snackbar(f"Обработано {len(results)} файлов", ft.Colors.GREEN)
        except Exception as ex:
            show_snackbar(str(ex))

    def get_info_click(e):
        try:
            if not path_input.value.strip():
                show_snackbar("Введите путь для получения информации")
                return

            result = get_info(path_input.value)
            result_view.controls.clear()

            info_card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.INFO, color=ft.Colors.BLUE),
                            title=ft.Text("Информация о пути", weight="bold"),
                        ),
                        ft.Divider(),
                        ft.Text(result, selectable=True)
                    ]),
                    padding=15,
                ),
                elevation=2
            )

            result_view.controls.append(info_card)
            page.update()
        except Exception as ex:
            show_snackbar(str(ex))

    def sort_click(e):
        try:
            if not path_input.value.strip():
                show_snackbar("Введите путь для сортировки")
                return

            reverse = sort_dropdown.value == "Убывание"
            items = sort_contents(path_input.value, reverse)
            result_view.controls.clear()
            result_view.controls.append(
                ft.Row([
                    ft.Icon(ft.Icons.SORT, color=ft.Colors.BLUE),
                    ft.Text("Содержимое папки:", weight="bold", size=16)
                ])
            )
            for name, is_dir in items:
                icon = ft.Icons.FOLDER if is_dir else ft.Icons.DESCRIPTION
                color = ft.Colors.AMBER if is_dir else ft.Colors.BLUE

                result_view.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(icon, color=color),
                        title=ft.Text(name),
                        subtitle=ft.Text("Папка" if is_dir else "Файл"),
                    )
                )

            page.update()
        except Exception as ex:
            show_snackbar(str(ex))

    def create_text_file_click(e):
        try:
            if not filename_input.value.strip():
                show_snackbar("Введите имя файла")
                return

            save_path = save_path_input.value.strip()
            if not save_path:
                save_path = path_input.value

            if not os.path.exists(save_path):
                show_snackbar("Указанная папка не существует")
                return

            filename = filename_input.value
            if not filename.endswith('.txt'):
                filename += '.txt'
            full_path = os.path.join(save_path, filename)
            content = file_content_input.value
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            show_snackbar(f"Файл создан: {full_path}", ft.Colors.GREEN)
            result_view.controls.clear()
            result_view.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN),
                                title=ft.Text("Файл успешно создан", weight="bold"),
                                subtitle=ft.Text(full_path),
                            ),
                            ft.Row([
                                ft.TextButton(
                                    "Копировать путь",
                                    icon=ft.Icons.CONTENT_COPY,
                                    on_click=lambda e: page.set_clipboard(full_path)
                                ),
                            ], alignment=ft.MainAxisAlignment.END)
                        ]),
                        padding=10,
                    )
                )
            )
            page.update()

        except Exception as ex:
            show_snackbar(f"Ошибка при создании файла: {str(ex)}")

    path_input = ft.TextField(
        label="Путь к папке",
        width=400,
        hint_text="Пример: C:/Users/Имя/Документы",
        prefix_icon=ft.Icons.FOLDER
    )

    pattern_input = ft.TextField(
        label="Регулярное выражение",
        hint_text="Пример: .*\\.txt$ для txt файлов",
        prefix_icon=ft.Icons.SEARCH
    )

    recursive_check = ft.Checkbox(label="Рекурсивно", value=True)

    sort_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Возрастание"),
            ft.dropdown.Option("Убывание")
        ],
        value="Возрастание",
        width=150
    )
    filename_input = ft.TextField(
        label="Имя файла",
        width=200,
        hint_text="Например: заметка",
        prefix_icon=ft.Icons.DESCRIPTION
    )

    save_path_input = ft.TextField(
        label="Путь для сохранения",
        width=300,
        hint_text="По умолчанию: путь к папке выше",
        prefix_icon=ft.Icons.FOLDER
    )

    file_content_input = ft.TextField(
        label="Содержимое файла",
        multiline=True,
        min_lines=3,
        max_lines=6,
        width=400
    )
    examples = ft.ExpansionTile(
        title=ft.Text("Примеры регулярных выражений"),
        leading=ft.Icon(ft.Icons.HELP),
        controls=[
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CODE),
                title=ft.Text(".*\\.txt$ - все txt файлы")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CODE),
                title=ft.Text("^report.* - файлы, начинающиеся с 'заметка'")
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.CODE),
                title=ft.Text(".*2023.* - файлы, содержащие '2025' в имени")
            ),
        ]
    )

    result_view = ft.Column(
        scroll="adaptive",
        expand=True,
        spacing=10
    )
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Управление файлами",
                icon=ft.Icons.FOLDER,
                content=ft.Column([
                    ft.Row([path_input]),
                    ft.Row([
                        ft.ElevatedButton("Создать папку", on_click=create_folder_click,
                                          icon=ft.Icons.CREATE_NEW_FOLDER),
                        ft.ElevatedButton("Удалить", on_click=delete_path_click, icon=ft.Icons.DELETE),
                        ft.ElevatedButton("Информация", on_click=get_info_click, icon=ft.Icons.INFO),
                    ]),
                    ft.Divider(),
                    ft.Row([pattern_input,
                            ft.ElevatedButton("Найти файлы", on_click=find_files_click, icon=ft.Icons.SEARCH)]),
                    ft.Row([recursive_check]),
                    examples,
                    ft.Row([ft.ElevatedButton("Добавить дату", on_click=add_date_click, icon=ft.Icons.DATE_RANGE)]),
                    ft.Row([sort_dropdown, ft.ElevatedButton("Сортировать", on_click=sort_click, icon=ft.Icons.SORT)]),
                ], scroll="adaptive")
            ),
            ft.Tab(
                text="Создание файла",
                icon=ft.Icons.NOTE_ADD,
                content=ft.Column([
                    ft.Text("Создание текстового файла:", weight="bold", size=16),
                    ft.Row([filename_input, save_path_input]),
                    file_content_input,
                    ft.Row([ft.ElevatedButton("Создать текстовый файл", on_click=create_text_file_click,
                                              icon=ft.Icons.CREATE)]),
                ], scroll="adaptive")
            )
        ],
        expand=1
    )

    page.add(
        tabs,
        ft.Divider(),
        ft.Text("Результаты:", weight="bold", size=18),
        ft.Container(
            content=result_view,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            padding=10,
            expand=True
        )
    )


if __name__ == "__main__":
    ft.app(target=main)