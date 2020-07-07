import logging
import config
import os

logging.basicConfig(filename=str(config.logfile), filemode='a', format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S')


def get_log_tail(size=3000):
    try:
        path = config.logfile
        file_size = path.stat().st_size
        offset = size if size <= file_size else file_size
        with path.open("rb") as f:
            f.seek(-offset, os.SEEK_END)
            data = f.read()
        text = data.decode("utf-8")
        return text
    except FileNotFoundError:
        return ""
