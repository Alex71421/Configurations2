import argparse                                                 # Импорт модуля для разбора аргументов командной строки
import sys                                                      # Импорт системного модуля для работы с выходом из программы


def main():
    """Основная функция приложения"""
    parser = argparse.ArgumentParser()                          # Создание парсера аргументов

                                                                # Добавление всех необходимых параметров командной строки
    parser.add_argument('--package')                            # Имя анализируемого пакета.
    parser.add_argument('--source')                             # URL-адрес репозитория или путь к файлу тестового репозитория
    parser.add_argument('--test-mode')                          # Режим работы с тестовым репозиторием.
    parser.add_argument('--version')                            # Версия пакета.
    parser.add_argument('--output')                             # Имя сгенерированного файла с изображением графа.
    parser.add_argument('--filter')                             # Подстрока для фильтрации пакетов.

    args = parser.parse_args()                                  # Разбор аргументов командной строки


    print("Настроенные параметры:")                             # Вывод всех параметров в формате ключ-значение
    for key, value in vars(args).items():                       # Итерация по всем аргументам
        print(f"{key}: {value}")


if __name__ == "__main__":
    try:
        main()                                                  # Вызов основной функции
    except Exception as e:                                      # Если есть ошибка
        print(f"Ошибка: {e}")                                   # Вывод сообщения об ошибке
        sys.exit(1)                                             # Завершение программы с кодом ошибки