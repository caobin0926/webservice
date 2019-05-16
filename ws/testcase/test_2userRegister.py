import pytest
import allure
from webservice.ws.common.clients import WebServiceClient
from webservice.ws.common.do_execl import Excel
from webservice.ws.common import paths
from webservice.ws.common.do_replace import replace
from webservice.ws.common.do_log import Log
import suds
from webservice.ws.common.do_mysql import Mysql
from webservice.ws.common.do_replace import TestData
from webservice.ws.common.do_testdata import UserBase

"""
定义测试注册接口
"""


class TestUserRegister:
    ex = Excel(paths.case_dir, 'userRegister')
    datas = ex.reads_case()
    # mysqls = None

    def setup_class(self):
        self.logs = Log('UserRegister')
        self.logs.filehandlers()
        self.logs.get_log('info', '-----测试开始-----')
        self.client = WebServiceClient(TestUserRegister.datas[0].url)
        user=UserBase()
        setattr(TestData,'name',user.name)
    @allure.story('注册接口')
    @pytest.mark.parametrize('case', datas)
    def test_userregister(self, case):
        self.logs.get_log('info','测试场景:{}'.format(case.title))
        # case.actual = {}
        try:
            case.actual = {}
            case.data = replace(case.data)
            # print(case.data)
            self.logs.get_log('debug', '请求参数:{}'.format(case.data))
            allure.attach('{}'.format(case.data), '请求参数')
            resp = self.client.wbService(case.method,case.data)
            case.actual['retCode'] = str(resp.retCode)
            case.actual['retInfo'] = str(resp.retInfo)
            self.logs.get_log('debug','预期结果:{}'.format(eval(case.expected)))
            self.logs.get_log('debug', '实际结果:{}'.format(case.actual))
            allure.attach('{}'.format(eval(case.expected)), '预期结果')
            allure.attach('{}'.format(case.actual), '实际结果')
            print(case.actual)
            assert eval(case.expected) == case.actual
            # 判断是否需要进行数据库中数据校验
            if case.issql == 'yes':
                sql = "SELECT * FROM t_user_info where Fuser_id='{}'".format(eval(case.data)['user_id'])
                mysqls = Mysql('user_db')
                # sqldata = mysqls.read_one(sql)
                # print(sql)
                # print(sqldata)
                if int(case.case_id) == 2:
                    # 判断注册成功的情况下数据库是否有生成一条记录
                    try:
                        sqldata = mysqls.read_one(sql)
                        # print(sqldata)
                        assert sqldata['Fuser_id'] == eval(case.data)['user_id']
                        setattr(TestData, 'uid', sqldata['Fuid'])
                        case.result = 'PASS'
                        # print(sqldata['Fuser_id'])
                    except AssertionError as e:
                        case.result = 'FAIL'
                        raise e
                        # 异常用例注册失败情况下载数据库中没有生成记录
                else:
                    case.result='PASS'
            else:
                case.result = 'PASS'
        except AssertionError as e:
            case.result = 'FAIL'
            raise e
        except suds.WebFault as e:
                case.actual['retCode'] = str(e.fault.retCode)
                case.actual['retInfo'] = str(e.fault.retInfo)
                try:
                    assert eval(case.expected) == case.actual
                    case.result = 'PASS'
                    raise e
                except AssertionError as e:
                    case.result = 'FAIL'
                    raise e
        finally:
            self.logs.get_log('info','断言结果:{}'.format(case.result))
            allure.attach('{}'.format(case.result),'断言结果')
            TestUserRegister.ex.write_case(case.case_id,str(case.actual),case.result)
            print(case.result)

    def teardown_class(self):
        self.logs.get_log('info','-----测试完成-----')
        TestUserRegister.ex.close_excel()
        # self.mysqls.close_connect()
        # TestUserRegister.mysqls.close_connect()
