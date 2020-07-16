import logging 
from pathlib import Path


def get_logger(path: Path):
    logging.basicConfig(filename=str(path), 
                        format='%(asctime)s %(message)s', 
                        filemode='w') 

    logger=logging.getLogger() 
    logger.setLevel(logging.DEBUG) 
    return logger