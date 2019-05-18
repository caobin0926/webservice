import pytest
import allure
from webservice.ws.common.do_execl import Excel
from webservice.ws.common import paths
from webservice.ws.common.do_replace import replace
from webservice.ws.common.do_log import Log
from webservice.ws.common.do_mysql import Mysql
import suds
from webservice.ws.common.do_replace import TestData
from webservice.ws.common.clients import WebServiceClient
from webservice.ws.common.do_testdata import phone

"""
发送短信测试类
"""


@allure.feature('发送短信接口')
class TestSendMcode:
    ex = Excel(paths.case_dir, 'sendMCode')
    data = ex.reads_case()
    mysqls = None

    def setup_class(self):
        # self.mysql=Mysql('')
        self.log = Log('sendmcode')  # 初始化收集日志log对象
        self.log.filehandlers()  # 选择文件输出渠道
        self.client = WebServiceClient(TestSendMcode.data[0].url)  # 初始化
        moblie=phone()
        setattr(TestData,'Register_cell',moblie)
        # print(TestData.Register_cell)

    @pytest.mark.parametrize('case', data)
    def test_sendmcode(self, case):
        allure.attach('请求参数：{}'.format(case.data))
        self.log.get_log('info', '测试场景:{}'.format(case.title))
        case.data = eval(replace(case.data))  # 替换参数
        self.log.get_log('debug', '请求参数:{}'.format(case.data))
        try:
            case.actual = {}
            # results = self.client.service.sendMCode(case.data)  # 发送webservice请求
            results = self.client.wbService(case.method,case.data)
            case.actual['retCode'] = str(results.retCode)
            case.actual['retInfo'] = str(results.retInfo)
            allure.attach('预期结果：{}'.format(case.expected))
            allure.attach('实际结果：{}'.format(case.actual))
            # print(case.actual)
            assert eval(case.expected) == case.actual
            if case.issql == 'yes':
                database = 'sms_db_' + case.data['mobile'][-2] + case.data['mobile'][-1]
                TestSendMcode.mysqls = Mysql(database)  # 连接数据库
                sql = "select * from t_mvcode_info_{} where Fmobile_no='{}'".format(case.data['mobile'][-3],
                                                                                    case.data['mobile'])  # 查询sql
                sqldata = TestSendMcode.mysqls.read_one(sql)  # 查询结果
                self.log.get_log('info', '查询结果:{}'.format(sqldata))
                if int(case.case_id) == 5:
                    assert sqldata['Fverify_code'] != None  # 校验数据库中是否生成记录
                    setattr(TestData, 'code', sqldata['Fverify_code'])
                    setattr(TestData,'Register_cell',case.data['mobile'])
                    case.result = 'PASS'
                    self.log.get_log('info', '测试结果:{}'.format(case.result))
                    allure.attach('测试结果：{}'.format(case.result))
                else:
                    try:
                        assert sqldata == None
                        case.result = 'PASS'
                        self.log.get_log('info', '测试结果:{}'.format(case.result))
                        allure.attach('测试结果：{}'.format(case.result))
                    except AssertionError as b:
                        case.result = 'FAIL'
                        self.log.get_log('info', '测试结果:{}'.format(case.result))
                        allure.attach('测试结果：{}'.format(case.result))
                        raise b
            else:
                case.result = 'PASS'
                self.log.get_log('info', '测试结果:{}'.format(case.result))
                allure.attach('测试结果：{}'.format(case.result))
        except AssertionError as e:
            self.log.get_log('error', '错误原因:{}'.format(e))
            case.result = 'FAIL'
            self.log.get_log('info', '测试结果:{}'.format(case.result))
            allure.attach('测试结果：{}'.format(case.result))
            raise e
        except suds.WebFault as e:
            a = e.fault
            # print(a)
            case.actual['faultcode'] = str(a.faultcode)
            case.actual['faultstring'] = str(a.faultstring)
            self.log.get_log('debug', '响应参数:{}'.format(case.actual))
            # TestSendMcode.ex.write_case(case.case_id, str(case.actual), case.result)
            try:
                assert eval(case.expected) == case.actual
                case.result = 'PASS'
            except AssertionError as y:
                case.result = 'FAIL'
                raise y
            # finally:
            # TestSendMcode.ex.write_case(case.case_id, str(case.actual), case.result)

        finally:
                self.log.get_log('info', '断言结果:{}'.format(case.result))
                allure.attach('{}'.format(case.result), '断言结果')
                TestSendMcode.ex.write_case(case.case_id, str(case.actual), case.result)

    def teardown_class(self):
        TestSendMcode.mysqls.close_connect()
        self.ex.close_excel()
