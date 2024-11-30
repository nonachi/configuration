# Задание 3
# Учебный конфигурационный язык
Инструмент командной строки для учебного конфигурационного
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из
входного формата в выходной. Синтаксические ошибки выявляются с выдачей
сообщений.
Входной текст на языке toml принимается из стандартного ввода. Выходной
текст на учебном конфигурационном языке попадает в файл, путь к которому
задан ключом командной строки.
## Возможности
* Объявление и использование констант
* Поддержка вложенных структур произвольной глубины
* Комментарии в формате (comment текст комментария)
* Преобразование в формат TOML
* Проверка синтаксиса и типов данных
## Использование
```
python main.py output.txt "[section]" "key = 42"
```
## Тестирование
```
python -m unittest test_translator.py
```