class Metadata(object):
    def __init__(self, name):
        self._name = name
    def __str__(self):
        return 'Metadata: %s' % (self.name)

    @property
    def name(self):
        return self._name

class Module(Metadata):
    def __init__(self, name):
        super(Module, self).__init__(name)
        self._actions = []
        self._tables = []
    def __str__(self):
        return 'Module:%s actions=%s tables=%s' % (self.name, self.actions, self.tables)
    __repr__ = __str__

    @property
    def actions(self):
        return self._actions
    @property
    def tables(self):
        return self._tables
        
    def add_action(self, action):
        self._actions.append(action)

    def add_table(self, table):
        self._tables.append(table)