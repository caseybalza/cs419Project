import logging
import os
from datetime import datetime

DEBUGLEVEL = logging.INFO

def get_logger(prefix):
    logger = logging.getLogger(prefix)
    if not os.path.exists('{}/logs/'.format(os.getcwd())):
        os.makedirs('{}/logs/'.format(os.getcwd()))
    hdlr = logging.FileHandler('{}/logs/cursesSQL{}.log'.format(os.getcwd(), datetime.now().hour))
    formatter = logging.Formatter('%(asctime)s %(levelname)s {}: %(message)s'.format(prefix))
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(DEBUGLEVEL)
    return logger
