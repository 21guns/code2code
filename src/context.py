class Context(object):
    
    def __init__(self):
        self._params = {}

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
        self._params['workspace'] = workspace

CONTEXT = Context()
