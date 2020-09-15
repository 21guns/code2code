from ..language import Language
from ..module import Module, Project
from ..context import *
from mako.template import Template
from mako.runtime import Context
from io import StringIO
import os
from ..utils import *


path = os.path.dirname(os.path.abspath(__file__))# get this file path

class Java(Language):
    def __init__(self):
        super(Java, self).__init__('java')

    def package(self):
        pass

    def class_name(self):
        pass

class JavaField(Java):
    def __init__(self, filed_name, type, comment):
        super(JavaField, self).__init__()
        self._filed_name = filed_name
        self._type = type 
        self._comment = comment
    def __str__(self):
        return '%s, %s ' % (self._filed_name, self._type)
    __repr__ = __str__

    @property
    def name(self):
        return self._filed_name

    @property
    def type(self):
        return self._type

    @property
    def comment(self):
        return self._comment
    @property
    def note(self):
        return ''

class JavaClass(Java):
    def __init__(self, project, class_metadata):
        super(JavaClass, self).__init__()
        self._project = project
        self._class_metadata = class_metadata
        self._package = ''
        self._class_name_suffix = ''
        self._fields = []
        self._id_field = None

    # @workspace.setter
    # def workspace(self, workspace):
    #     self._params['workspace'] = workspace
    @property
    def class_name(self):
        return convert(self._class_metadata.name, '_', True) + self._class_name_suffix
        
    @property
    def package(self):
        return '.'.join([self._project.package, self._package])
    @property
    def file_name(self):
        return self.class_name + '.' + self.name
    @property
    def id_field(self):
        return self._id_field
    @property
    def has_id(self):
        return not self._id_field is None
    @property
    def fields(self):
        return self._fields
    @property
    def comment(self):
        return self._class_metadata.comment

    def set_package(self, package):
        self._package = package
        return self

    def set_class_name_suffix(self, suffix):
        self._class_name_suffix = suffix
        return self

    def parse_type(self, filed_name, dbType):
        type = None
        javaType = None
        if "VARCHAR" in dbType:
            type = "String"
            javaType = "java.lang.String"
        elif "TINYINT" in dbType:
            type = "Byte"
            javaType = "java.lang.Byte"
        elif "DATETIME" in dbType:
            type = "LocalDateTime"
            javaType = "java.time.LocalDateTime"
        elif "DATE" in dbType:
            type = "LocalDate"
            javaType = "java.time.LocalDate"
        elif "DECIMAL" in dbType:
            type = "BigDecimal"
            javaType = "java.math.BigDecimal"
        elif "INT" == dbType:
            type = "Integer"
            javaType = "java.lang.Integer"
        elif "BIGINT UNSIGNED" == dbType:
            type = "Long"
            javaType = "java.lang.Long"
        elif "BIGINT" == dbType:
            type = "Long"
            javaType = "java.lang.Long"
        elif "JSON" == dbType:
            type = "HashMap"
            javaType = "java.util.HashMap"
        else:
            type = None
            print(filed_name, javaType)
        return type, javaType

    def generator(self):
        pass

class JavaClassMako(JavaClass):
    def __init__(self, project, class_metadata, tl_file):
        super(JavaClassMako, self).__init__(project, class_metadata)
        self._template = Template(filename = tl_file)
        
    # def generator(self, module):
    #     super().generator(module)
        # buf = StringIO()
        # ctx = Context(buf, java_class = self)
        # self._template.render_context(ctx)
        # f = open(self._project.java_src + self.file_name, 'w')
        # f.write(buf.getvalue())
        # f.close()
    def write_file(self):
        buf = StringIO()
        ctx = Context(buf, java_class = self)
        self._template.render_context(ctx)
        print(buf.getvalue())

class DOJavaClassMako(JavaClassMako):
    def __init__(self, project, class_metadata):
        super(DOJavaClassMako, self).__init__(project, class_metadata, path + '/tl/service/do.tl')
        self._package = 'entity'
        self._class_name_suffix = 'DO'

    def generator(self):
        for t in self._class_metadata.fields:
            dbType = t.type.split('(')[0]
            type, _ = self.parse_type(t.name, dbType)
            if type is not None :
                self._fields.append(JavaField(convert(t.name,'_',False), type, t.comment))
            if (t.name == 'id'):
                self._id_field = t 

class VOJavaClassMako(JavaClassMako):
    def __init__(self, project, class_metadata):
        super(VOJavaClassMako, self).__init__(project, class_metadata, path + '/tl/api/vo.tl')
        self._package = 'vo'
        self._class_name_suffix = 'VO'

    def generator(self):
        for t in self._class_metadata.fields:
            dbType = t.type.split('(')[0]
            type, _ = self.parse_type(t.name, dbType)
            if type is not None :
                self._fields.append(JavaField(convert(t.name,'_',False), type, t.comment))
            if (t.name == 'id'):
                self._id_field = t 

class JavaModule(Module):

    def __init__(self, name):
        super(JavaModule, self).__init__(name)

    @property       
    def path(self):
        return '/'.join([CONTEXT.workspace, self.name])

    def generator(self, module):
        ## add template project 
        self._projects.append(service(self))
        self._projects.append(api(self))

        for p in self._projects:
            p.generator(module)

        pass
    
    def write_file(self):
         ## 1.mk dir
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        os.system('cp -r ' + path + '/template/module/* '+ self.path)

        for p in self._projects:
            p.write_file()

class JavaProject(Project):
    java_src = '/src/main/java'
    resource_src = '/src/main/resources/'

    def __init__(self, name, module):
        super(JavaProject, self).__init__(name, module)
        self._class = []
        self._table_template_class = []
        self._action_template_class = []

    @property
    def package(self):
        return '.'.join([CONTEXT.package, self._module.name, self.name])

    @property
    def path(self):
        return '/'.join([self._module.path, self.name])

    @property
    def java_src(self):
        return self.module.path + java_src

    def add_class(self, java_class):
        self._class.append(java_class)

    def add_table_template_class(self, tm_class):
        self._table_template_class.append(tm_class)
        return self
    def add_action_template_class(self, tm_class):
        self._action_template_class.append(tm_class)
        return self
    def generator(self, module):
        """解析元数据生成代码和项目相关信息
        """
        # for c in self._class:
        #     c.generator(module)
        
        for t in module.tables:
            for c in self._table_template_class:
                cl = c(self, t)
                # self.add_class(cl)
                cl.generator()
            
        for a in module.actions:
            for c in self._action_template_class:
                cl = c(self, t)
                self.add_class(cl)
                cl.generator()
                
    def write_file(self):
        # if not os.path.exists(self.path):
        #     os.makedirs(self.path)
        for c in self._class:
            c.write_file()
            pass
#----java template project
def service(module):
    jp = JavaProject('service', module)
    jp.add_table_template_class(DOJavaClassMako)
    return jp

def api(module):
    jp = JavaProject('api', module)
    jp.add_action_template_class(VOJavaClassMako)
    return jp


class ServiceJavaProject(JavaProject):


    def generator(self, module):
        """解析元数据生成代码和项目相关信息
        """
        # for t in module.tables:

        # for a in module.actions: