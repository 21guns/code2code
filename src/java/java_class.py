from ..language import Language
from ..utils import *
import copy

def parse_type(otherType):
    if otherType is None:
        return None
    type = otherType
    if "VARCHAR" in otherType:
        type = "String"
    elif "TINYINT" in otherType:
        type = "Byte"
    elif "DATETIME" in otherType:
        type = "LocalDateTime"
    elif "DATE" in otherType:
        type = "LocalDate"
    elif "DECIMAL" in otherType:
        type = "BigDecimal"
    elif "INT" == otherType:
        type = "Integer"
    elif "BIGINT UNSIGNED" == otherType:
        type = "Long"
    elif "BIGINT" == otherType:
        type = "Long"
    elif "JSON" == otherType:
        type = "HashMap"

    elif type.lower() == 'string':
        type = "String"
    elif type.lower() == 'int':
        type = "Integer"
    elif type.lower() == 'date':
        type = "LocalDateTime"
    elif type.lower() == 'number':
        type = "Integer"
    elif type.lower() == 'boolean':
        type = "Boolean"
    elif type.lower() == 'long':
        type = "Long"
    elif type.lower() == 'array':
        type = "List"
    else:
        type = type
        # print('\033[1;32;43m parse java type(%s) error \033[0m' % type)
    return type

class Java(Language):
    def __init__(self):
        super(Java, self).__init__('java')

    def package(self):
        pass

    def class_name(self):
        pass

class JavaMethod(Java):
    def __init__(self, method_name, comment):
        super(JavaMethod, self).__init__()
        self._annotations = []
        self._method_name = method_name
        self._return = None
        self._params = []
        self._comment = comment
    @property
    def method_name(self):
        return self._method_name
    @property
    def annotations(self):
        return '/n'.join(self._annotations)
    @property
    def params(self):
        return ','.join(self._params)
    @property
    def comment(self): 
        return self._comment
    def add_annotations(self, annotation):
        self._annotations.append(annotation)
        return self
    def add_params(self, param):
        if (len(param) > 0):
            if (isinstance(self._params, list)):
                self._params.extend(param)
            else :
                self._params.append(param)
        return self
    def set_return(self, re):
        self._return = re
        return self
    
class JavaField(Java):
    def __init__(self, field_name, db_type, comment):
        super(JavaField, self).__init__()
        self._field_name = field_name
        self._db_type = db_type
        self._type = parse_type(db_type) 
        if (self._type is None) :
            print('\033[1;32;43m parse java type(%s) error for field(%s) \033[0m' % (self._type, self._field_name))
        self._comment = comment

    def __str__(self):
        return 'JavaField:%s, %s ' % (self._field_name, self._type)
    __repr__ = __str__

    @property
    def name(self):
        return convert(self._field_name,'_',False)

    @property
    def field(self):
        return self._field_name
    @property
    def type(self):
        return self._type

    @property
    def comment(self):
        return self._comment
    @property
    def note(self):
        return ''
    @property
    def is_id(self):
        return self.name == 'id'
    @property
    def full_type(self):
        if self._type is None:
            return ''
        if (self._type in ['String', 'Byte', 'Integer','Long', 'Boolean']):
            return '.'.join(['java.lang', self._type])
        elif (self._type in ['LocalDateTime', 'LocalDate']):
            return '.'.join(['java.time', self._type])
        elif (self._type == 'HashMap'):
            return 'java.util.HashMap'
        elif (self._type == 'BigDecimal'):
            return 'java.math.BigDecimal'
        elif self._type.startswith('List'):
            return 'java.util.List'
        elif self._type == 'Object':
            return ''
        else:
            return self._type
    @property
    def jdbc_type(self):
        if (self._db_type == "INT") :
            return "INTEGER"
        elif (self._db_type == "BIGINT UNSIGNED"):
            return "BIGINT"
        elif (self._db_type == "DATETIME"):
            return "TIMESTAMP"
        return self._db_type

class JavaClass(Java):
    def __init__(self, class_name, comment):
        super(JavaClass, self).__init__()
        self._project = None
        self._package = ''
        self._class_name = class_name
        self._class_name_suffix = ''
        self._class_name_prefix = ''
        self._fields = []
        self._id_field = None
        self._comment = comment
        self._methods = []
        self._annotations =[]
        self._imports = []

    def __str__(self):
        return 'fields = %s' % (self._fields)
    __repr__ = __str__

    @property
    def class_name(self):
        return self._class_name_prefix + self.original_class_name + self._class_name_suffix
    @property
    def original_class_name(self):
        # 如果名称里包含_ 进行驼峰转换，反之不包含返回首字符大写
        return convert(self._class_name,'_', True) if self._class_name.find('_') != -1 else firstUpowerOnly(self._class_name)
    @property
    def metadata_name(self):
        return self._class_name
    @property
    def package(self):
        return '.'.join(filter(lambda x: len(x) >0 ,[self.project_package, self._package]))
    @property
    def project_package(self):
        return self._project.package
    @property
    def module_package(self):
        return self._project.module.package
    @property
    def module_name(self):
        return self._project.module.name         
    @property
    def file_name(self):
        return self.class_name + '.' + self.name
    @property
    def id_field(self):
        return self._id_field
    @property
    def has_id(self):
        return self._id_field is not None
    @property
    def fields(self):
        return self._fields
    @property
    def comment(self):
        return self._comment
    @property
    def annotations(self):
        return '/n'.join(self._annotations)
    @property
    def imports(self):
        return '\n'.join(set(self._imports))
    @property
    def methods(self):
        return self._methods
    def add_fields(self, field):
        if field is not None :
            self._fields.append(field)
            if field.is_id:
                self._id_field = field
            if (not field.full_type.startswith('java.lang')
                and len(field.full_type) > 0) :
                self._imports.append('import ' +field.full_type + ';')
        return self

    def add_method(self, method):
        if method is not None :
            self._methods.append(method)
        return self

    def add_annotations(self, annotation):
        if annotation is not None :
            self._annotations.append(annotation)
        return self
    def add_imports(self, ipo):
        if ipo is not None :
            self._imports.append(ipo)

    def set_package(self, package):
        self._package = package
        return self

    def set_class_name_suffix(self, suffix):
        self._class_name_suffix = suffix
        return self
    def set_class_name_prefix(self,prefix):
        self._class_name_prefix = prefix
        return self

    def set_project(self, project):
        self._project = project
        return self

    def generator(self):
        pass

    def copy(self):
        return copy.deepcopy(self)

class ClassField(object):
    def __init__(self, name):
        self._name = convert(name, '_', True)
        self._fields = []
    def __str__(self):
        return '%s, %s ' % (self._name, self._fields)
    __repr__ = __str__

    def add_field(self, field):
        self._fields.append(field)
        return self
    @property
    def name(self):
        return self._name

