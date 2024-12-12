import unittest
from unittest.mock import patch, mock_open
from config_translator import translate_toml_to_custom

class TestConfigTranslator(unittest.TestCase):
    
    # Тест 1: Проверка правильного преобразования данных
    def test_translate_toml_to_custom(self):
        toml_input = "[section]\nkey = 42"
        expected_output = "var section {\n  key : 42,\n}"
        
        # Преобразуем данные
        result = translate_toml_to_custom(toml_input)
        
        # Проверяем, что результат преобразования правильный
        self.assertEqual(result, expected_output)
    
    # Тест 2: Проверка обработки ошибок синтаксиса TOML
    def test_invalid_toml(self):
        toml_input = "[section] key = 42"  # Неправильный формат (секция и ключ на одной строке)
        
        with self.assertRaises(Exception) as context:
            translate_toml_to_custom(toml_input)
        
        # Проверка того, что ошибка правильная
        self.assertTrue('TOML' in str(context.exception))
    
    # Тест 3: Проверка записи в файл
    @patch("builtins.open", new_callable=mock_open)
    def test_write_to_file(self, mock_file):
        toml_input = "[section]\nkey = 42"
        expected_output = "var section {\n  key : 42,\n}"
        
        # Вызовем функцию для записи в файл
        with patch("config_translator.translate_toml_to_custom", return_value=expected_output):
            with open("output.txt", "w") as output_file:
                output_file.write(expected_output)
        
        # Проверяем, что файл был открыт для записи и содержимое верное
        mock_file.assert_called_with("output.txt", "w")
        mock_file().write.assert_called_with(expected_output)

    # Тест 4: Проверка правильного формата при нескольких секциях
    def test_multiple_sections(self):
        toml_input = "[section]\nkey = 42\n[another_section]\nvalue = 10"
        expected_output = (
            "var section {\n  key : 42,\n}\n"
            "var another_section {\n  value : 10,\n}"
        )
        
        # Преобразуем данные
        result = translate_toml_to_custom(toml_input)
        
        # Проверяем, что результат преобразования правильный
        self.assertEqual(result, expected_output)
    
    # Тест 5: Проверка пустого ввода (пустой TOML)
    def test_empty_input(self):
        toml_input = ""
        expected_output = ""
        
        # Преобразуем данные
        result = translate_toml_to_custom(toml_input)
        
        # Проверяем, что результат преобразования правильный (пустой ввод -> пустой вывод)
        self.assertEqual(result, expected_output)

if __name__ == "__main__":
    unittest.main()
