from ..language import Language, LanguageMapping
from ..module import Module, Project
from ..context import *
from ..utils import *

from mako.template import Template
from mako.runtime import Context
from io import StringIO
import os
from itertools import groupby
import difflib
import copy

path = os.path.dirname(os.path.abspath(__file__))# get this file path

def parse_type(otherType):
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
    else:
        print('\033[1;32;43m parse java type %s \033[0m' % type)
    return type

class Java(Language):
    def __init__(self):
        super(Java, self).__init__('java')

    def package(self):
        pass

    def class_name(self):
        pass

class JavaField(Java):
    def __init__(self, field_name, db_type, comment):
        super(JavaField, self).__init__()
        self._field_name = field_name
        self._db_type = db_type
        self._type = parse_type(db_type) 
        self._comment = comment
    def __str__(self):
        return 'JavaField:%s, %s ' % (self._filed_name, self._type)
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
        if (self._type in ['String', 'Byte', 'Integer','Long']):
            return '.'.join('java.lang', self._type)
        elif (self._type in ['LocalDateTime', 'LocalDate']):
            return '.'.join('java.time', self._type)
        elif (self._type == 'HashMap'):
            return 'java.util.HashMap'
        elif (self._type == 'BigDecimal'):
            return 'java.math.BigDecimal'
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
        self._fields = []
        self._id_field = None
        self._comment = comment


    def __str__(self):
        return 'fields = %s' % (self._fields)
    __repr__ = __str__

    # @workspace.setter
    # def workspace(self, workspace):
    #     self._params['workspace'] = workspace
    @property
    def class_name(self):
        return convert(self._class_name, '_', True) + self._class_name_suffix
    @property
    def original_class_name(self):
        return convert(self._class_name, '_', True)
    @property
    def metadata_name(self):
        return self._class_name
    @property
    def package(self):
        return '.'.join([self.project_package, self._package.replace('-',)])
    @property
    def project_package(self):
        return self._project.package
    @property
    def module_package(self):
        return self._project.module.package
              
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

    def add_fields(self, field):
        if field is not None :
            self._fields.append(field)
            if field.is_id:
                self._id_field = field
        return self
    def set_package(self, package):
        self._package = package
        return self

    def set_class_name_suffix(self, suffix):
        self._class_name_suffix = suffix
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

class JavaClassLanguageMapping(LanguageMapping):

    def mapping(self, modules):
        self._do_mapping = {}
        self._vo_mapping = {}
        self._dto_mapping = {}

        self._do_field_mapping = {}
        self._vo_field_mapping = {}

        for key, module in  modules.items():
            for t in module.tables:
                jc = JavaClass(t.name, t.comment)
                self._do_mapping[jc.class_name] = jc
                t.java_class = jc
                jc.class_metadata = t

                cf = ClassField(t.name)
                self._do_field_mapping[cf.name] = cf
                for f in t.fields:
                    otherType = f.type.split('(')[0]
                    f_name = convert(f.name,'_',False)
                    jf = JavaField(f.name, otherType, f.get_note())
                    jf.field_metadata = f
                    jc.add_fields(jf)

                    cf.add_field(f_name)
                pass

            for root_path, g in groupby(module.actions,key=lambda x:x.module_root):
                acs = list(g)
                print(root_path)
                for a in acs:
                    # jc = JavaClass(None, a)
                    # self._do_mapping[jc.class_name] = jc
                    # if url_path.after_module_name() == '' :
                        
                    # for g, p in groupby(a.request.params,key=lambda x:x.group):
                        # print(g,list(p))

                    #响应参数
                    jc = JavaClass(a.name, a.comment)
                    self._vo_mapping[a.name] = jc
                    a.response.java_class = jc
                    jc.class_metadata = a

                    cf = ClassField(a.name)
                    self._vo_field_mapping[a.name] = cf
                    for g, ps in groupby(a.response.params,key=lambda x:x.group):
                        for p in list(ps):
                            f_name = convert(p.name,'_',False)
                            jf = JavaField(p.name, p.type, p.comment)
                            jf.field_metadata = f
                            jc.add_fields(jf)

                            cf.add_field(f_name)
                        pass
            # print(self._do_mapping)
            # print(self._vo_mapping)
            # analytic(self._do_field_mapping, self._vo_field_mapping)

def analytic(do_field_mapping, vo_field_mapping):
    print(do_field_mapping, vo_field_mapping)
    # if url_path.after_module_name() == '' :
        # print(list(map(lambda s: difflib.SequenceMatcher(None, s.lower(), url_path.module_name().lower()).quick_ratio(), class_mapping.keys())))
    # for key,d_java in  do_field_mapping.items():
    #     print(d_java)

        

class JavaClassMako(object):
    def __init__(self, project, java_class, tl_file):
        self._template = Template(filename = tl_file,  input_encoding='utf-8')
        self._project = project
        self._java_class = java_class.set_project(project)

    @property
    def class_path(self):
        return self._project.java_src + CONTEXT.separator + self._java_class.package.replace('.', CONTEXT.separator)

    def generator(self):
        pass

    def write_file(self):
        if not os.path.exists(self.class_path):
            os.makedirs(self.class_path)
        buf = StringIO()
        ctx = Context(buf, java_class = self._java_class)
        self._template.render_context(ctx)
        with open(self.class_path + CONTEXT.separator + self._java_class.file_name, 'w') as f:
            f.write(buf.getvalue())
            f.close()

class ResourceMako(JavaClassMako):
    def __init__(self, project, java_class, tl_file):
        super(ResourceMako, self).__init__(project, java_class, tl_file)
        java_class.name = 'xml'
    
    @property
    def resource_path(self):
        return self._project.resource_src + CONTEXT.separator + self._java_class.package.replace('.', CONTEXT.separator)


    def write_file(self):
        if not os.path.exists(self.resource_path):
            os.makedirs(self.resource_path)
        buf = StringIO()
        ctx = Context(buf, java_class = self._java_class)
        self._template.render_context(ctx)
        with open(self.resource_path + CONTEXT.separator + self._java_class.file_name, 'w') as f:
            f.write(buf.getvalue())
            f.close()

class DOJavaClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(DOJavaClassMako, self).__init__(project, java_class, path + '/tl/service/do.tl')
        java_class.set_package('entity')
        java_class.set_class_name_suffix('DO')


class VOJavaClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(VOJavaClassMako, self).__init__(project, java_class, path + '/tl/api/vo.tl')
        java_class.set_package('vo')
        java_class.set_class_name_suffix('VO')

class MapperJavaClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(MapperJavaClassMako, self).__init__(project, java_class, path + '/tl/service/mapper.tl')
        java_class.set_package('repository.mapper')
        java_class.set_class_name_suffix('Mapper')

class MapperXmlMako(ResourceMako):
    def __init__(self, project, java_class):
        super(MapperXmlMako, self).__init__(project, java_class, path + '/tl/service/mapperXml.tl')
        java_class.set_package('repository.mapper')
        java_class.set_class_name_suffix('Mapper')

class JavaModule(Module):

    def __init__(self, name):
        super(JavaModule, self).__init__(name)
        ## add template project 
        self._projects.append(ServiceJavaProject(self))
        self._projects.append(ApiJavaProject(self))
        self._projects.append(AdminControllerJavaProject(self))
        self._projects.append(ControllerJavaProject(self))

    @property       
    def path(self):
        return '/'.join([CONTEXT.workspace, self.name])
    @property       
    def package(self):
        return '.'.join([CONTEXT.package, self.name])

    def generator(self, module):
        for p in self._projects:
            p.generator(module)

        pass
    
    def write_file(self):
         ## 1.mk dir
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        os.system('cp -r ' + path + '/template/module/* '+ self.path)
        ## 2.create pom
        template = Template(filename = path + '/tl/pom/module.tl', input_encoding='utf-8')
        buf = StringIO()
        ctx = Context(buf, package_name = CONTEXT.package, module_name=self.name)
        template.render_context(ctx)
        with open(self.path + CONTEXT.separator + 'pom.xml', 'w') as f:
            f.write(buf.getvalue())
            f.close()

        for p in self._projects:
            p.write_file()

class ParentModule(Module):
    def __init__(self):
        super(ParentModule, self).__init__('parent')

    @property       
    def path(self):
        return '/'.join([CONTEXT.workspace, self.name])
    
    def write_file(self):
         ## 1.mk dir
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        ## 2.create pom
        template = Template(filename = path + '/tl/pom/parent.tl', input_encoding='utf-8')
        buf = StringIO()
        ctx = Context(buf, package_name = CONTEXT.package)
        template.render_context(ctx)
        with open(self.path + CONTEXT.separator + 'pom.xml', 'w') as f:
            f.write(buf.getvalue())
            f.close()

class JavaProject(Project):
    java_src_root = '/src/main/java'
    resource_src_root = '/src/main/resources/'

    def __init__(self, name, module):
        super(JavaProject, self).__init__(name, module)
        self._class = []

    @property
    def package(self):
        return '.'.join([CONTEXT.package, self._module.name, self.name])

    @property
    def package_path(self):
        return self.java_src + CONTEXT.separator + self.package.replace('.', CONTEXT.separator)

    @property
    def path(self):
        return '/'.join([self._module.path, self.name])

    @property
    def java_src(self):
        return self.path + JavaProject.java_src_root

    @property
    def resource_src(self):
        return self.path + JavaProject.resource_src_root

    @property
    def module(self):
        return self._module

    def add_class(self, java_class):
        self._class.append(java_class)

    def _add_class(self, module):
        pass

    def generator(self, module):
        """解析元数据生成代码和项目相关信息
        """
        self._add_class(module)

        for c in self._class:
            c.generator()
                
    def write_file(self):
        if not os.path.exists(self.java_src):
            os.makedirs(self.java_src)
        if not os.path.exists(self.package_path):
            os.makedirs(self.package_path)
            
        self._write_prject();

        for c in self._class:
            c.write_file()
            pass

    def _write_prject(self):
        pass

class ServiceJavaProject(JavaProject):
    def __init__(self, module):
        super(ServiceJavaProject, self).__init__('service', module)

    def _add_class(self, module):
        """解析元数据生成代码
        """
        for t in module.tables:
            self.add_class(DOJavaClassMako(self, t.java_class.copy()))
            self.add_class(MapperJavaClassMako(self, t.java_class.copy()))
            self.add_class(MapperXmlMako(self, t.java_class.copy()))

        # for a in module.actions:
            # self.add_class(VOJavaClassMako(self, a.response.java_class.copy()))


    def _write_prject(self):
        ## 1.create pom
        template = Template(filename = path + '/tl/pom/service.tl', input_encoding='utf-8')
        buf = StringIO()
        ctx = Context(buf, package_name = CONTEXT.package, module_name=self._module.name)
        template.render_context(ctx)        
        with open(self.path + CONTEXT.separator + 'pom.xml', 'w') as f:
            f.write(buf.getvalue())
            f.close()

class ApiJavaProject(JavaProject):
    def __init__(self, module):
        super(ApiJavaProject, self).__init__('api', module)

    def _add_class(self, module):
        """解析元数据生成代码
        """
        for t in module.tables:
            self.add_class(VOJavaClassMako(self, t.java_class.copy()))

        for a in module.actions:
            self.add_class(VOJavaClassMako(self, a.response.java_class.copy()))


    def _write_prject(self):
        ## 1.create pom
        template = Template(filename = path + '/tl/pom/api.tl', input_encoding='utf-8')
        buf = StringIO()
        ctx = Context(buf, package_name = CONTEXT.package, module_name=self._module.name)
        template.render_context(ctx)        
        with open(self.path + CONTEXT.separator + 'pom.xml', 'w') as f:
            f.write(buf.getvalue())
            f.close()

class AdminControllerJavaProject(JavaProject):
    def __init__(self, module):
        super(AdminControllerJavaProject, self).__init__('admin-controller', module)

    def _add_class(self, module):
        """解析元数据生成代码
        """
        # for t in module.tables:

        # for a in module.actions:


    def _write_prject(self):
        ## 1.create pom
        template = Template(filename = path + '/tl/pom/admin.tl', input_encoding='utf-8')
        buf = StringIO()
        ctx = Context(buf, package_name = CONTEXT.package, module_name=self._module.name)
        template.render_context(ctx)        
        with open(self.path + CONTEXT.separator + 'pom.xml', 'w') as f:
            f.write(buf.getvalue())
            f.close()

class ControllerJavaProject(JavaProject):
    def __init__(self, module):
        super(ControllerJavaProject, self).__init__('Controller', module)

    def _add_class(self, module):
        """解析元数据生成代码
        """
        # for t in module.tables:

        # for a in module.actions:

    def _write_prject(self):
        ## 1.create pom
        template = Template(filename = path + '/tl/pom/controller.tl', input_encoding='utf-8')
        buf = StringIO()
        ctx = Context(buf, package_name = CONTEXT.package, module_name=self._module.name)
        template.render_context(ctx)        
        with open(self.path + CONTEXT.separator + 'pom.xml', 'w') as f:
            f.write(buf.getvalue())
            f.close()