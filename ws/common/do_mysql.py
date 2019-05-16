import pymysql
from webservice.ws.common.do_conf import Config
from webservice.ws.common import paths

"""
定义读取数据库类
"""


class Mysql:
    def __init__(self, database):
        self.conf = Config(paths.db_dir)

        self.connect = pymysql.connect(host=self.conf.reads_conf('test', 'host'),
                                       port=int(self.conf.reads_conf('test', 'port')),
                                       user=self.conf.reads_conf('test', 'user'),
                                       password=self.conf.reads_conf('test', 'password'),
                                       database=database,
                                       charset='utf8')
        self.cursors = self.connect.cursor(pymysql.cursors.DictCursor)

    # 获取查询一行记录
    def read_one(self, sql):
        self.cursors.execute(sql)
        return self.cursors.fetchone()

    # 获取所有满足条件的记录
    def read_all(self, sql):
        self.cursors.execute(sql)
        return self.cursors.fetchall()

    def close_connect(self):
        self.cursors.close()
        self.connect.close()


if __name__ == '__main__':
    sql = "SELECT * FROM t_user_info where Fuser_id='鲁班5'"
    my = Mysql('user_db')
    reuslt=my.read_one(sql)
    my.close_connect()
    print(reuslt)
