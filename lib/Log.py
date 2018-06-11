import logging
from logging.handlers import RotatingFileHandler

# class Log
class Log(object):
    ## initial log files and set logrotate
    def __init__(self, config):
        # initial global val
        self.config = config
        self.config.logger = logging.getLogger("DDNS")

    # get logger
    def get_logger(self):
        try:
            log_level = getattr(logging, self.config.LOG_LEVEL)
        except:
            log_level = logging.NOTSET

        self.config.logger.setLevel(log_level)
        fh = RotatingFileHandler(self.config.LOG_FILE,
                mode='a',
                maxBytes=self.config.LOG_MAX_SIZE,
                backupCount=self.config.LOG_BACKUP_COUNT)
        fh.setLevel(log_level)
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]\
                        %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.config.logger.addHandler(fh)
        self.config.logger.addHandler(ch)
        return(self.config.logger)
