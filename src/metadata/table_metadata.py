from .metadata import *

class Table(Metadata):
    def __init__(self, name, comment):
        super(Table, self).__init__(name)
        self._fields = []
        self._pk = None
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
    @property
    def has_pk(self):
        return self._pk is not None

    def add_fields(self, field):
        if field is not None:
            self._fields.append(field)
            if (field.is_pk):
                # print(f"{field} : {field.is_pk}")
                self._pk = field

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

    def pk(self, pk = False):
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
    def get_note(self):
        return self._note
    def get_chinese_name(self):
        return self._chinese_name
    
    def note(self, note):
        self._note = note
        return self

    @property
    def type(self):
        return self._type
    @property
    def comment(self):
        return self._chinese_name
    @property
    def is_pk(self):
        return self._is_pk
    @property
    def nullable_str(self):
        return "DEFAULT NULL" if self._nullable else "NOT NULL"
def new_field(name, chinese_name, type):
    return Field(name, chinese_name, type)
       
    