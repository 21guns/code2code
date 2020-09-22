class Context(object):
    
    def __init__(self):
        self._params = {}
        self._params['separator'] = '/'

    def get(self, key, default = None):
        self._params.get(key, default)
        return self

    def set(self, key, value):
        self._params[key] = value
        return self

    @property
    def workspace(self):
        return self._params['workspace']

    @workspace.setter
    def workspace(self, workspace):
        if workspace.endswith('/'):
            workspace = workspace[:-1]
        self._params['workspace'] = workspace

    @property
    def package(self):
        return self._params['package']

    @package.setter
    def package(self, package):
        self._params['package'] = package

    @property
    def separator(self):
        return self._params['separator']

CONTEXT = Context()
