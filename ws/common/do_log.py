import logging
from webservice.ws.common import paths
from webservice.ws.common.do_conf import Config

"""
定义日志类
"""


class Log:
    def __init__(self, name):
        conf = Config(paths.logconf_dir)
        # 定义日志输出格式
        self.format = logging.Formatter(conf.reads_conf('log', 'format'))
        # 定义日志收集和级别
        self.myloger = logging.getLogger(name)
        self.myloger.setLevel(conf.reads_conf('log', 'setlevel'))
        # 定义文件输出渠道和级别、格式
        self.file_hanler = logging.FileHandler(paths.logs_dir, 'a', encoding='utf-8')
        self.file_hanler.setLevel(conf.reads_conf('log', 'outlevel'))
        self.file_hanler.setFormatter(self.format)
        # 定义控制台输出渠道和级别、格式
        self.hanler = logging.StreamHandler()
        self.hanler.setLevel(conf.reads_conf('log', 'outlevel'))
        self.hanler.setFormatter(self.format)


    # 选择文件输出渠道
    def filehandlers(self):
        self.myloger.addHandler(self.file_hanler)

    # 选择控制台输出渠道
    def hanlers(self):
        self.myloger.addHandler(self.hanler)

    # 收集各个级别的日志
    def get_log(self, level, msg):
        if level == 'info':
            # print('测试')
            self.myloger.info(msg)
        elif level == 'debug':
            self.myloger.debug(msg)
        elif level == 'warning':
            self.myloger.warning(msg)
        elif level == 'error':
            self.myloger.error(msg)
        else:
            self.myloger.critical(msg)


if __name__ == '__main__':
    log = Log('test')
    # print(log.format)
    log.hanlers()
    # log.myloger.info('测试')
    log.get_log('info', '测试001')
