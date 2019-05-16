import os

# 项目路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 测试用例路径
case_dir = os.path.join(base_dir, 'data', 'cases.xlsx')
# 测试数据路径
testdata_dir = os.path.join(base_dir, 'config', 'testdata.cfg')
# 数据库连接信息路径
db_dir = os.path.join(base_dir, 'config', 'db.cfg')
# 日志输出文件路径
logs_dir = os.path.join(base_dir, 'log', 'logs.txt')
# 日志输出配置文件路径
logconf_dir = os.path.join(base_dir, 'config', 'log.cfg')

if __name__ == '__main__':
    print(logconf_dir)
