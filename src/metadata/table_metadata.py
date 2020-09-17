from .metadata import *

class Table(Metadata):
    def __init__(self, name, comment):
        super(Table, self).__init__(name)
        self._fields = []
        self._pk = []
        self._comment = comment
    def __str__(self):
        return 'Table: name = %s fields = %s' % (self.name, self.fields)
    __repr__ = __str__

    @property
    def fields(self):
        return self._fields

    @property
    def pk(self):
        return self._pk

    @property
    def comment(self):
        return self._comment

    def add_fields(self, field):
        if field is not None:
            self._fields.append(field)
            if (field.is_pk()):
                self._pk.append(field)

def new_table(name, comment):
	return Table(name, comment)

class Field(Metadata):
    def __init__(self, name, chinese_name, type):
        super(Field, self).__init__(name)
        self._chinese_name = chinese_name
        self._type = type 
        self._is_pk = False
        self._nullable = True
        #备注
        self._note = ''
    def __str__(self):
        return 'Field:%s %s' % (self.name, self._type)
    __repr__ = __str__

    def is_pk(self, pk = True):
        self._is_pk = pk
        return self

    def nullable(self, nullable):
        self._nullable = nullable
        return self
    def unique(self, unique):
        self._unique = unique
        return self
    def default_value(self, value):
        self._default_value = value
        return self
    def note(self, note):
        self._note = note
        return self
    @property
    def type(self):
        return self._type
    @property
    def comment(self):
        return self._note
def new_field(name, chinese_name, type):
    return Field(name, chinese_name, type)
       
    