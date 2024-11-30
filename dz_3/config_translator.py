import toml

def translate_toml_to_custom(toml_data):
    """
    Преобразует входные данные TOML в формат учебного конфигурационного языка.
    """
    try:
        parsed_data = toml.loads(toml_data)
    except toml.TomlDecodeError as e:
        raise ValueError(f"Ошибка синтаксиса TOML: {e}")

    result = []
    
    for key, value in parsed_data.items():
        # Обработка значений словаря
        if isinstance(value, dict):
            result.append(f"{key} : {translate_dict(value)}")
        else:
            result.append(f"{key} : {value}")

    return "\n".join(result)

def translate_dict(d):
    """
    Рекурсивно переводит словарь в нужный формат.
    """
    dict_result = ["{"]
    for key, value in d.items():
        if isinstance(value, dict):
            dict_result.append(f"  {key} : {translate_dict(value)}")
        else:
            dict_result.append(f"  {key} : {value}")
    dict_result.append("}")
    return "\n".join(dict_result)
