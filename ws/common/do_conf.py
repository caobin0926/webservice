import configparser
from webservice.ws.common import paths

"""
读取配置文件类
"""


class Config:
    def __init__(self, filename):
        self.conf = configparser.ConfigParser()
        self.conf.read(filename, encoding='utf-8')

    def reads_conf(self, section, options):
        return self.conf.get(section, options)


if __name__ == '__main__':
    conf = Config(paths.testdata_dir)
    print(conf.reads_conf('testdata', 'Register_cell'))
