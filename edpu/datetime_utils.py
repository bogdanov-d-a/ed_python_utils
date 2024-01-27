import datetime

def get_now_datetime_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
