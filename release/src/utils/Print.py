def print_status(tag: str, message: str):
    COLORS = {
        "INF": "\033[94m",  # синий
        "ERR": "\033[91m",  # красный
        "WRN": "\033[93m",  # жёлтый
        "OK":  "\033[92m",  # зелёный
        "ASK": "\033[96m",  # бирюзовый (вопрос/ввод)
        "INI": "\033[95m",  # фиолетовый (инициализация)
        "RST": "\033[0m",   # сброс цвета
    }

    tag = tag.upper()[:3]
    color = COLORS.get(tag, "\033[90m")  # серый по умолчанию
    reset = COLORS["RST"]
    print(f"{color}[{tag:<3}]{reset} {message}")
