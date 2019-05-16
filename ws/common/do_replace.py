import re
from webservice.ws.common.do_conf import Config
import configparser
from webservice.ws.common import paths

"""
定义将字符串中特定的字符替换函数
"""


def replace(data):
    # conf = Config(filename)
    p = '%(.*?)%'
    while re.search(p, data):
        reuslt = re.search(p, data)
        options = reuslt.group(1)
        # try:
        #     a = conf.reads_conf(section, options)
        # except configparser.NoOptionError as e:
        a = str(getattr(TestData, options))
        # finally:
        data = re.sub(p, a, data, count=1)
    return data


class TestData:
    pass


if __name__ == '__main__':
    data = '{"client_ip": "127.0.0.1", "mobile": "%Register_cell%", "tmpl_id": "1"}'
    new_data = replace(paths.testdata_dir, 'testdata', data)
    print(new_data)
