from datetime import datetime

def convert_time(created_time: datetime) -> str:
    now = datetime.now()
    diff = now - created_time

    seconds = diff.total_seconds()
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    weeks = days // 7

    if seconds < 60:
        return f"{int(seconds)} detik"
    elif minutes < 60:
        return f"{int(minutes)} menit"
    elif hours < 24:
        return f"{int(hours)} jam"
    elif days < 7:
        return f"{int(days)} hari"
    else:
        return f"{int(weeks)} minggu"
