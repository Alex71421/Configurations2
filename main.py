import argparse                                                         # Импорт модуля для разбора аргументов командной строки
import sys                                                              # Импорт системного модуля для работы с выходом из программы
import urllib.request                                                   # Модуль для загрузки данных по URL

def load_cargo_toml(url):
    """
    Загружает файл Cargo.toml по-указанному URL. Возвращает содержимое файла как строку.
    """
    try:                                                                # Пытаемся выполнить сетевой запрос
        with urllib.request.urlopen(url) as response:                   # Открываем URL как поток
            return response.read().decode("utf-8")                      # Читаем содержимое и декодируем в строку
    except Exception as e:                                              # Ловим любые ошибки (сетевые, неправильный URL и др.)
        raise RuntimeError(f"Не удалось загрузить Cargo.toml: {e}")


def parse_dependencies(cargo_text):
    """
    Извлекает секцию [dependencies] из текста Cargo.toml.
    Возвращает словарь зависимостей.
    """
    dependencies = {}                                                   # Создаём пустой словарь под зависимости
    lines = cargo_text.splitlines()                                     # Разбиваем весь текст на строки

    in_deps = False                                                     # Флаг: сейчас мы внутри секции [dependencies]

    for line in lines:                                                  # Перебираем каждую строку Cargo.toml
        stripped = line.strip()                                         # Убираем пробелы по краям строки

        if stripped == "[dependencies]":                                # Если строка — начало секции зависимостей
            in_deps = True                                              # Включаем флаг режима чтения зависимостей
            continue                                                    # Переходим к следующей строке

        if stripped.startswith("[") and stripped.endswith("]") and stripped != "[dependencies]":  # Если встретили новую секцию
            in_deps = False                                             # Значит, секция зависимостей закончилась

        if in_deps and "=" in stripped:                                 # Если мы внутри секции зависимостей и строка содержит "="
            try:                                                        # Пытаемся разобрать строку
                name, version = stripped.split("=", 1)                  # Разделяем по "=", но только один раз
                name = name.strip()                                     # Убираем пробелы у названия зависимости
                version = version.strip().strip('"')                    # Убираем пробелы и кавычки у версии
                dependencies[name] = version                            # Сохраняем зависимость в словарь
            except ValueError:                                          # Если строка повреждена или неправильная
                pass                                                    # Просто пропускаем её

    return dependencies                                                 # Возвращаем словарь зависимостей

def main():
    """Основная функция приложения"""
    parser = argparse.ArgumentParser()                                  # Создание парсера аргументов

                                                                        # Добавление всех необходимых параметров командной строки
    parser.add_argument('--package')                                    # Имя анализируемого пакета.
    parser.add_argument('--source')                                     # URL-адрес репозитория или путь к файлу тестового репозитория
    parser.add_argument('--test-mode')                                  # Режим работы с тестовым репозиторием.
    parser.add_argument('--version')                                    # Версия пакета.
    parser.add_argument('--output')                                     # Имя сгенерированного файла с изображением графа.
    parser.add_argument('--filter')                                     # Подстрока для фильтрации пакетов.

    args = parser.parse_args()                                          # Разбор аргументов командной строки

    if not args.source:                                                 # Проверяем, что указан URL
        print("Ошибка: параметр --source обязателен.")                  # Выводим ошибку
        sys.exit(1)

    if not args.version:                                                # Проверяем, что указана версия
        print("Ошибка: параметр --version обязателен.")                 # Сообщаем об ошибке
        sys.exit(1)

    cargo_text = load_cargo_toml(args.source)                           # Загружаем файл по URL

    if args.version not in cargo_text:                                  # Проверяем, есть ли заявленная версия в файле
        print(f"Предупреждение: версия {args.version} не найдена в Cargo.toml")  # Просто предупреждение, не ошибка

    deps = parse_dependencies(cargo_text)                               # Получаем словарь зависимостей

    print("Настроенные параметры:")                                     # Вывод всех параметров в формате ключ-значение
    for key, value in vars(args).items():                               # Итерация по всем аргументам
        print(f"{key}: {value}")

    print("\nПрямые зависимости пакета:")
    if not deps:                                                        # Проверяем, есть ли зависимости вообще
        print("Зависимостей нет.")
    else:                                                               # Если зависимости есть:
        for name, version in deps.items():                              # Перебираем все зависимости
            print(f"{name}: {version}")


if __name__ == "__main__":
    try:
        main()                                                          # Вызов основной функции
    except Exception as e:                                              # Если есть ошибка
        print(f"Ошибка: {e}")                                           # Вывод сообщения об ошибке
        sys.exit(1)                                                     # Завершение программы с кодом ошибки