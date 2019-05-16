from webservice.ws.common.clients import Client
import suds
url='http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
t={"uid": "100010533", "true_name": "蓝讯澄", "cre_id": '130324197507114516'}
client = Client(url)

{'retCode': 19001, 'retInfo': '身份证号错误'}
try:
    results = client.dict(client.service.verifyUserAuth(t))
except suds.WebFault as e:
    results=e.fault
    a={}
    a['faultcode']=str(results.faultcode)
    a['faultstring']=str(results.faultstring)
print(results)