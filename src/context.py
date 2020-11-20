class Context(object):
    
    def __init__(self):
        self._params = {}
        self._params['separator'] = '/'

    def get(self, key, default = None):
        return self._params.get(key, default)

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

    @property
    def table_file(self):
        return self._params['table_file']
    @table_file.setter
    def table_file(self, table_file):
        self._params['table_file'] = table_file
    @property
    def has_table_file(self):
        return self.get('table_file') is not None and len(self._params['table_file']) > 0

    @property
    def interface_file(self):
        return self._params['interface_file']
    @interface_file.setter
    def interface_file(self, interface_file):
        self._params['interface_file'] = interface_file
    @property
    def has_interface_file(self):
        return self.get('interface_file') is not None and len(self._params['interface_file']) > 0

CONTEXT = Context()
