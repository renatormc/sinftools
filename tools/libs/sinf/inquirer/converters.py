from datetime import datetime

def str2datetime(value, format_):
    try:
        return datetime.strptime(value, format_)
    except:
        return None

def integer(value):
    try:
        return int(value)
    except:
        return None

def real(value):
    try:
        return float(value)
    except:
        return None

if __name__ == "__main__":
    data = str2date_without_seconds("12/12/2019 12:45")
    print(data)