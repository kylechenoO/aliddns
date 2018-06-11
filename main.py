import os
import sys
from lib.Log import Log
from lib.DDNS import DDNS
from lib.Config import Config

if __name__ == '__main__':
    # initial val
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))

    # read config
    configObj = Config(BASE_PATH)
    logObj = Log(configObj)
    logger = logObj.get_logger()

    #debug print
    logger.debug('DOMAIN_DOMAIN {}'.format(configObj.DOMAIN_DOMAIN))
    logger.debug('DOMAIN_PREFIX {}'.format(configObj.DOMAIN_PREFIX))
    logger.debug('DOMAIN_TYPE {}'.format(configObj.DOMAIN_TYPE))
    logger.debug('DOMAIN_TTL {}'.format(configObj.DOMAIN_TTL))
    logger.debug('LOG_PATH {}'.format(configObj.LOG_PATH))
    logger.debug('LOG_FILE {}'.format(configObj.LOG_FILE))
    logger.debug('LOG_MAX_SIZE {}'.format(configObj.LOG_MAX_SIZE))
    logger.debug('LOG_BACKUP_COUNT {}'.format(configObj.LOG_BACKUP_COUNT))

    # initial ddnsObj
    ddnsObj = DDNS(configObj, logger)
    ddnsObj.run()

    # success exit
    sys.exit(configObj.SUCCESS_EXIT)
