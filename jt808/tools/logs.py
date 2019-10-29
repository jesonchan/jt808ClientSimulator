import logging
from logging.handlers import RotatingFileHandler
import threading
import configparser


class Log(object):

    def __init__(self, log_config):
        pass

    def __new__(cls, log_config):
        mutex = threading.Lock()
        mutex.acquire()  # 上锁，防止多线程下出问题

        if not hasattr(cls, 'instance'):
            cls.instance = super(Log, cls).__new__(cls)
            config = configparser.ConfigParser()
            config.read(log_config, encoding='UTF-8')
            cls.instance.log_filename = config.get('LOGGING', 'log_file')
            cls.instance.max_bytes_each = int(
                config.get('LOGGING', 'max_bytes_each'))
            cls.instance.backup_count = int(
                config.get('LOGGING', 'backup_count'))
            cls.instance.format = config.get('LOGGING', 'format')
            cls.instance.log_level_in_console = int(
                config.get('LOGGING', 'log_level_in_console'))
            cls.instance.log_level_in_logfile = int(
                config.get('LOGGING', 'log_level_in_logfile'))
            cls.instance.logger_name = config.get('LOGGING', 'logger_name')
            cls.instance.console_log_on = int(
                config.get('LOGGING', 'console_log_on'))
            cls.instance.logfile_log_on = int(
                config.get('LOGGING', 'logfile_log_on'))
            cls.instance.logger = logging.getLogger(cls.instance.logger_name)
            cls.instance.__config_logger()
        mutex.release()
        return cls.instance

    def get_logger(self):
        return self.logger

    def __config_logger(self):
        # 设置日志格式
        fmt = self.format.replace('|', '%')
        formatter = logging.Formatter(fmt)
        if self.console_log_on == 1:  # 如果开启控制台日志
            console = logging.StreamHandler()
            # console.setLevel(self.log_level_in_console)
            console.setFormatter(formatter)
            self.logger.addHandler(console)
            self.logger.setLevel(self.log_level_in_console)
        if self.logfile_log_on == 1:  # 如果开启文件日志
            rt_file_handler = RotatingFileHandler(
                self.log_filename,
                maxBytes=self.max_bytes_each,
                backupCount=self.backup_count)

            rt_file_handler.setFormatter(formatter)
            self.logger.addHandler(rt_file_handler)
            self.logger.setLevel(self.log_level_in_logfile)


if __name__ == '__main__':
    # path = './log.conf'.decode("utf-8").encode("gbk")
    log = Log('../../config/log.ini')
    logger = log.get_logger()
    # logger = logging.getLogger('test_logger') # 在其它模块中时，可这样获取该日志实例
    logger.debug('this is a debug level message')
    logger.info('this is info level message')
    logger.warning('this is warning level message')
    logger.error('this is error level message')
    logger.critical('this is critical level message')
