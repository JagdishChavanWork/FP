from datetime import datetime


def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def calculate_duration(start_time, end_time):
    fmt = "%Y-%m-%d %H:%M:%S"

    start = datetime.strptime(start_time, fmt)
    end = datetime.strptime(end_time, fmt)

    return (end - start).total_seconds()