import logging 

logging.basicConfig(filename="hash.log", 
                    format='%(asctime)s %(message)s', 
                    filemode='w') 
  

logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 