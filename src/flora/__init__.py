import logging 
import os

logdir ='logs'
os.makedirs(logdir,exist_ok=True)

logpath = os.path.join(logdir,'running_logs.log')

# logging.basicConfig(filename=logpath,level=logging.DEBUG, format='[%(asctime)s] : [%(name)s] : [%(levelname)s] : [%(message)s]')
# stream = logging.StreamHandler()
# log = logging.getLogger()
# log.addHandler(stream)

format = logging.Formatter('[%(asctime)s] : [%(name)s] : [%(levelname)s] : [%(message)s]')
filehandler = logging.FileHandler(logpath)
filehandler.setFormatter(format)

logger = logging.getLogger()
logger.addHandler(filehandler)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())