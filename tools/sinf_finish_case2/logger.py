import logging 


def get_logger(path):
    logging.basicConfig(filename=str(path.absolute()), 
                        format='%(asctime)s %(message)s', 
                        filemode='w') 
    logger=logging.getLogger() 
    logger.setLevel(logging.DEBUG) 
    return logger