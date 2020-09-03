from .metadata import *

class Paramter(Metadata):
    def __init__(self, name, type, comment):
        super(Paramter, self).__init__(name)
        self._type = type 
        self._require = False
        self._comment = comment
        self._note = ''
        self._group = 'default'

    @property
    def group(self):
        """参数嵌套时，使group进行分组关联"""
        return self._group
    @group.setter
    def group(self, value):   
        self._group = value

class UrlPath(Metadata):
    def __init__(self, name, url):
        super(UrlPath, self).__init__(name)
        self._url = url
        self._path = url.lstrip().rstrip().split('/')
        self._path_variable_name = []
        self._path_variable_index = []
        self._not_path_variable = []
        for i,p in enumerate(self._path):
            if p.startswith('{'):
                self._path_variable_name.append(p.replace('{','').replace('}',''))
                self._path_variable_index.append(i)
            else:
                self._not_path_variable.append(p)


ACTION_RESPONSE_TYPE = {
	'LIST':'LIST',
	'PAGE':'PAGE',
	'ENTITY':'ENTITY'
}
ACTION_REQUEST_TYPE = {
	'PATH':'PATH',
	'QUERY':'QUERY',
	'JSON':'JSON'
}

class Request(Metadata):
    def __init__(self, name = '', url = '', http_method = ''):
        super(Request, self).__init__(name)
        self._url = url
        self._eg = '' #请求示例
        self._http_method = http_method
        self._type = ACTION_REQUEST_TYPE['QUERY']
        self._params = []

    def check(self):
        if not self._url.startswith('/') :
            return False
        if self._http_method not in ['POST','GET','PUT','DELETE']:
            return False
        return True

    def http_method(self, http_method):
        self._http_method = http_method
        return self

    def url(self, url):
        self._url = url
        return self

    def add_params(self, name, type, comment):
        self._params.append(Paramter(name, type, comment))

class Response(Metadata):
    def __init__(self, name = '', url = ''):
        super(Response, self).__init__(name)
        self._type = ACTION_REQUEST_TYPE['QUERY']
        self._params = []
        self._eg = '' #响应示例

    def add_params(self, name, type, comment):
        self._params.append(Paramter(name, type, comment))

class Action(Metadata):
    def __init__(self, name, comment):
        super(Action, self).__init__(name)
        self._comment = comment
        self._request = Request()
        self._response = Response()
    def __str__(self):
        return 'Action: name = %s, comment = %s ' % (self.name, self._comment)
    __repr__ = __str__

    def url(self, url):
        self._url_path = UrlPath(self.name, url)
        self._request.url(url)

    def http_method(self, http_method):
        self._request.http_method(http_method)

    def add_request_params(self, name, type, comment):
        self._request.add_params(name, type, comment)

    def add_response_params(self, name, type, comment):
        self._response.add_params(name, type, comment)

def new_action(name, comment):
    return Action(name, comment)

