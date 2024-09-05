import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler


class LoggingHandler(logging.Logger):
    """logging 日志轮询二次封装，工具类

    Doc: https://docs.python.org/3/howto/logging-cookbook.html
    """

    FORMAT = (
        '%(asctime)8s | %(levelname)8s | %(name)5s - '
        '%(threadName)8s:%(filename)5s:%(funcName)s:%(lineno)d - %(message)s')

    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

    def __init__(self,
            name='defaultLogger',
            stream=True,
            file=True,
            size_rollback=False,
            max_bytes=10*1024*1024,
            rotating_time="D",
            encoding="utf-8",
            level="DEBUG",
            backup_count=5):
        """
        stream:是否输出到控制台
        file:是否保存到文件
        size_rollback: 为False的时候，默认启用时间回滚；为True的时候，默认是文件大小存储
        max_bytes： 如果开启文件大小回滚时，则该值生效
        rotating_time：  如果开启按照时间回滚时，则该值生效。S - Seconds/M - Minutes/
        H - Hours/ D - Days / W{0-6} - roll over on a certain day; 0 - Monday
        level：日志级别；CRITICAL/FATAL/ERROR/WARN/WARNING/INFO/DEBUG/NOTSET
        """
        super().__init__(name, level)
        self.encoding = encoding
        self.stream = stream
        self.file = file
        self.max_bytes = max_bytes
        self.rotating_time = rotating_time
        self.backup_count = backup_count
        self.size_rollback = size_rollback
        if self.stream:
            self._set_stream_handler(self.FORMAT)
        if self.file:
            self._set_file_handler('default.log', self.FORMAT)

    def set_name(self, filename='default.log', name='', log_format=None, log_datefmt=None):
        """
        filename：保存的文件名
        name:日志名字
        log_format: 日志格式
        log_datefmt： 时间格式
        """
        if name:
            super().set_name(name)
        fmt = log_format if log_format else self.FORMAT
        datefmt = log_datefmt if log_datefmt else self.DATE_FORMAT
        self.handlers.clear()  # Clear existing handlers
        if self.stream:
            self._set_stream_handler(fmt)
        if self.file:
            self._set_file_handler(filename, fmt)

    def _set_file_handler(self, filename, fmt):
        """
        设置输出文件
        """
        formatter = logging.Formatter(fmt=fmt, datefmt=self.DATE_FORMAT)
        if self.size_rollback:
            handler = RotatingFileHandler(filename, maxBytes=self.max_bytes, backupCount=self.backup_count, encoding=self.encoding)
        else:
            handler = TimedRotatingFileHandler(filename, when=self.rotating_time, backupCount=self.backup_count, encoding=self.encoding)
        handler.setLevel(self.level)
        handler.setFormatter(formatter)
        self.addHandler(handler)

    def _set_stream_handler(self, fmt):
        """
        设置控制台输出
        """
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        handler.setLevel(self.level)
        self.addHandler(handler)


class LoggingFileHandler:
    """logging 日志轮询二次封装，工具类 """
    def __init__(self, level=logging.INFO, backup_count=5, log_format=None,
                 log_encoding=None, log_datefmt=None, use_stream_handler=True):
        """
        初始化LoggingFileHandler对象

        :param level: int - 日志级别，默认为 logging.INFO。
        :param backup_count: int - 最多保存的日志文件个数，默认为 5。
        :param log_format: str - 日志格式，默认为 '%(asctime)-8s - %(name)5s: %(filename)5s  %(levelname)-8s %(message)s'。
        :param log_encoding: str - 日志文件的编码方式，默认为 None。
        :param log_datefmt: str - 时间格式，默认为 '%Y-%m-%d %H:%M:%S'。
        :param use_stream_handler: bool - 是否使用控制台处理器，默认为 True（是）。
        """
        # 设置日志级别、备份数量、日志格式、编码方式、时间格式、是否使用控制台处理器
        self.level = level
        self.backup_count = backup_count
        self.log_format = log_format or '%(asctime)-8s - %(name)5s: %(filename)5s  %(levelname)-8s %(message)s'
        self.log_encoding = log_encoding
        self.log_datefmt = log_datefmt or '%Y-%m-%d %H:%M:%S'
        self.use_stream_handler = use_stream_handler

    def get_logger(self, username, logfile, method='size', rotating_time='midnight', new_log_format=None,
                   new_level=None, new_logfile=None, use_stream_handler=None):
        """
        获取logger对象

        :param username: str - logger的名字。
        :param logfile: str - 日志文件名。
        :param method: str - 日志文件的轮换方式，'size' 表示按照日志大小轮换，'time' 表示按照时间轮换，默认为 'size'。
        :param rotating_time: str - 当方法为按时间轮换时，指定轮换时间，可以是 'S', 'M', 'H', 'D', 'W0'-'W6', 'midnight' 中的任何一个，默认为 'midnight'。
        :param new_log_format: str - 自定义日志格式，如果不指定，则使用初始化函数时设定的默认值。
        :param new_level: int - 记录日志的级别，如果不指定，则使用初始化函数时设定的默认值。
        :param new_logfile: str - 更改日志文件名，如果不指定，则使用初始日志文件名。
        :param use_stream_handler: bool - 是否使用控制台处理器，如果不指定，则使用初始化函数时设定的默认值。
        :return: logging.Logger 对象
        """
        logger = logging.getLogger(username)
        if new_level is not None:
            logger.setLevel(new_level)
        else:
            logger.setLevel(self.level)

        if new_log_format is not None:
            formatter = logging.Formatter(fmt=new_log_format, datefmt=self.log_datefmt)
        else:
            formatter = logging.Formatter(fmt=self.log_format, datefmt=self.log_datefmt)

        if use_stream_handler is None:
            use_stream_handler = self.use_stream_handler
        if use_stream_handler:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        if new_logfile is not None:
          logfile = new_logfile

        if method == 'size':
            rthandler = RotatingFileHandler(logfile, maxBytes=10*1024*1024, backupCount=self.backup_count,
                                            encoding=self.log_encoding)
            rthandler.setFormatter(formatter)
            logger.addHandler(rthandler)
        elif method == 'time':
            trthandler = TimedRotatingFileHandler(logfile, when=rotating_time, backupCount=self.backup_count,
                                                  encoding=self.log_encoding)
            trthandler.setFormatter(formatter)
            logger.addHandler(trthandler)

        return logger
