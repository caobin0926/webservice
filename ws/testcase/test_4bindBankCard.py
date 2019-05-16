import pytest
import allure
from webservice.ws.common.do_execl import Excel
from webservice.ws.common import paths
from webservice.ws.common.do_replace import replace
from webservice.ws.common.do_log import Log
import suds
from webservice.ws.common.do_mysql import Mysql
from webservice.ws.common.clients import WebServiceClient

"""
定义测试注册接口
"""


class TestBindBankCard:
    ex = Excel(paths.case_dir, 'bindBankCard')
    datas = ex.reads_case()
    # mysqls = None

    def setup_class(self):

        self.logs = Log('bindBankCard')
        self.logs.filehandlers()
        self.logs.get_log('info', '-----测试开始-----')
        # self.mysqls = Mysql('user_db')
        self.client = WebServiceClient(TestBindBankCard.datas[0].url)

    @allure.story('注册接口')
    @pytest.mark.parametrize('case', datas)
    def test_verifyuserAuth(self, case):
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
            self.logs.get_log('debug', '响应参数:{}'.format(case.actual))
            allure.attach('{}'.format(case.actual), '响应参数')
            assert eval(case.expected) == case.actual
            # 判断是否需要进行数据库中数据校验  user_db_xx. t_bind_card_x
            if case.issql == 'yes':
                sql = "select * from t_bind_card_{} where Fmobile_no='{}'".format(case.data['mobile'][-3],
                                                                                    case.data['mobile'])  # 查询sql
                database = 'user_db_' + case.data['mobile'][-2] + case.data['mobile'][-1]
                mysqls = Mysql(database)
                if int(case.case_id) == 1:
                    # 判断注册成功的情况下数据库是否有生成一条记录
                    try:
                        sqldata = mysqls.read_one(sql)
                        # print(sqldata)
                        assert str(sqldata['Fuid']) == eval(case.data)['uid']
                        # setattr(TestData, 'uid', sqldata['Fuid'])
                        case.result = 'PASS'
                    except AssertionError as e:
                        case.result = 'FAIL'
                        print('哈哈哈')
                        raise e
                else:
                    case.result='PASS'
            else:
                case.result = 'PASS'
        except AssertionError as e:
            case.result = 'FAIL'
            # print('测试1')
            # raise e
        except suds.WebFault as e:
                case.actual['retCode'] = str(e.fault.retCode)
                case.actual['retInfo'] = str(e.fault.retInfo)
                try:
                    assert eval(case.expected) == case.actual
                    case.result = 'PASS'
                except AssertionError as e:
                    case.result = 'FAIL'
        finally:
                self.logs.get_log('info','断言结果:{}'.format(case.result))
                allure.attach('{}'.format(case.result),'断言结果')
                TestBindBankCard.ex.write_case(case.case_id,str(case.actual),case.result)

    def teardown_class(self):
        self.logs.get_log('info','-----测试完成-----')
        TestBindBankCard.ex.close_excel()
        # self.mysqls.close_connect()
        # TestUserRegister.mysqls.close_connect()
