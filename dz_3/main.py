import argparse
import sys
from config_translator import translate_toml_to_custom

def main():
    # Настроим парсер командной строки
    parser = argparse.ArgumentParser(description="Транслятор TOML в учебный конфигурационный язык")
    parser.add_argument('output_file', help="Путь к выходному файлу")
    parser.add_argument('input_data', help="Входные данные в формате TOML (многострочные данные через аргументы)", nargs='+')
    args = parser.parse_args()

    # Объединяем все части входных данных в одну строку
    input_data = '\n'.join(args.input_data)

    try:
        # Преобразуем данные
        translated_data = translate_toml_to_custom(input_data)
        
        # Запишем результат в выходной файл
        with open(args.output_file, 'w') as output_file:
            output_file.write(translated_data)
        
        print(f"Результат успешно записан в {args.output_file}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
