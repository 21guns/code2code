from .metadata import *
from ..utils import *

class Paramter(Metadata):
    DEFAULT_GROUP = 'default'
    def __init__(self, name, type, comment, group = 'default'):
        super(Paramter, self).__init__(name)
        self._type = type 
        self._require = False
        self._comment = comment
        self._note = ''
        self._group = group
    def __str__(self):
        return 'name = %s, type = %s, group = %s ' % (self.name, self._type, self._group)
    __repr__ = __str__

    @property
    def group(self):
        """参数嵌套时，使group进行分组关联"""
        return self._group
    @group.setter
    def group(self, value):   
        self._group = value
    @property
    def type(self):
        return self._type
    @property
    def comment(self):
        return self._comment

class UrlPath(Metadata):
    def __init__(self, name, url):
        super(UrlPath, self).__init__(name)
        self._url = url
        self._path = url.lstrip().rstrip().split('/')
        self._path_variable_name = []
        self._path_variable_index = []
        self._not_path_variable = []
        self._module_root = '/'.join(self._path[0:4])
        for i,p in enumerate(self._path):
            if p.startswith('{'):
                self._path_variable_name.append(p.replace('{','').replace('}',''))
                self._path_variable_index.append(i)
            else:
                self._not_path_variable.append(p)

    @property
    def url(self):
        return self._url
    @property
    def module_root(self):
        return self._module_root

    def module_name(self):
        return None if len(self._path) < 4 else self._path[3]
    def last_path(self):
        return self.path[-1]

    def last_path_name(self):
        if (self.last_path().startswith('{')):
            return self.path_variable_name[-1]
        else :
            return self.last_path()

    def path_name(self, begin, step):
        return ''.join(map(firstUpower, self._not_path_variable[begin:step]))

    def after_module_name(self):
        return self.path_name(4, len(self._path))

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
    def __init__(self, name = '', http_method = ''):
        super(Request, self).__init__(name)
        self._url = None
        self._eg = '' #请求示例
        self._http_method = http_method
        self._type = ACTION_REQUEST_TYPE['QUERY']
        self._params = []
    def __str__(self):
        return '%s, params = %s ' % (self._url, self._params)
    __repr__ = __str__

    def check(self):
        if not self._url.startswith('/') :
            return False
        if self._http_method not in ['POST','GET','PUT','DELETE']:
            return False
        return True
    @property
    def params(self):
        return self._params
    
    def get_method(self):
        return self._http_method

    def set_method(self, http_method):
        self._http_method = http_method
        return self

    def url(self, url):
        self._url = url
        return self

    def add_params(self, name, type, comment, group):
        self._params.append(Paramter(name, type, group))
        return self

class Response(Metadata):
    def __init__(self, name = ''):
        super(Response, self).__init__(name)
        self._type = ACTION_REQUEST_TYPE['QUERY']
        self._params = []
        self._eg = '' #响应示例
        self._url = None

    def __str__(self):
        return '%s, params = %s ' % (self._url, self._params)
    __repr__ = __str__

    @property
    def params(self):
        return self._params

    def url(self, url):
        self._url = url
        return self

    def add_params(self, name, type, comment, group):
        self._params.append(Paramter(name, type, comment, group))
        return self

class Action(Metadata):
    def __init__(self, name, comment):
        super(Action, self).__init__(name)
        self._comment = comment
        self._request = Request()
        self._response = Response()
        self._url_path = None

    def __str__(self):
        return 'name = %s, request = %s, response = %s ' % (self.name, self._request, self._response)
    __repr__ = __str__

    def url(self, url):
        self._url_path = UrlPath(self._name, url)
        self._request.url(self._url_path)
        self._response.url(self._url_path)
    
    def url_path(self):
        if self._url_path is None:
            print('\033[1;32;43m %s url is error \033[0m' % (self.name))
        return self._url_path

    @property
    def request(self):
        return self._request
    @property
    def response(self):
        return self._response
    @property
    def comment(self):
        return self._comment
    def module_name(self):
        return self._url_path.module_name();
    @property
    def module_root(self):
        return self._url_path._module_root
        
    def http_method(self, http_method):
        self._request.set_method(http_method)

    def add_request_params(self, name, type, comment, group = 'default'):
        self._request.add_params(name, type, comment, group)

    def add_response_params(self, name, type, comment, group = 'default'):
        self._response.add_params(name, type, comment, group)
    
    @property
    def name(self):
        if self._url_path.after_module_name() == '' :
            return self._request.get_method() + self._url_path.module_name()
        return self._request.get_method() + self._url_path.after_module_name()
    
def new_action(name, comment):
    return Action(name, comment)

