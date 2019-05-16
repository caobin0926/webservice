from suds.client import Client

"""
封装webservice接口请求类
"""


class WebServiceClient:
    def __init__(self, url):
        self.url = url
        self.client = Client(self.url)

    def wbService(self, method, data):
        results = eval("self.client.service.{0}({1})".format(method, data))
        return results