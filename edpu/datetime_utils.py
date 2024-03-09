def get_now_datetime_str() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
