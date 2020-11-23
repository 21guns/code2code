from ..language import Language, LanguageMapping
from ..module import Module, Project
from ..context import *
from ..utils import *
from ..metadata import *
from .java_class import *

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
        self._class_name_prefix = ''
        self._fields = []
        self._id_field = None
        self._comment = comment
        self._methods = []
        self._annotations =[]

    def __str__(self):
        return 'fields = %s' % (self._fields)
    __repr__ = __str__

    @property
    def class_name(self):
        return self._class_name_prefix + self._class_name + self._class_name_suffix
    @property
    def original_class_name(self):
        return self._class_name
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
    def methods(self):
        return self._methods
    def add_fields(self, field):
        if field is not None :
            self._fields.append(field)
            if field.is_id:
                self._id_field = field
        return self

    def add_method(self, method):
        if method is not None :
            self._methods.append(method)
        return self

    def add_annotations(self, annotation):
        if annotation is not None :
            self._annotations.append(annotation)
        return self
    
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

class MappingResult(object):
    def __init__(self, name,):
        self._name = name
        self._entity =[]
        self._request = []
        self._response = []
        self._action = []
    @property
    def entity(self):
        return self._entity
    @property
    def request(self):
        return self._request
    @property
    def response(self):
        return self._response
    @property
    def action(self):
        return self._action
    def add_entity(self, entity):
        self._entity.append(entity)  
    def add_request(self, request):
        self._request.append(request)
    def add_response(self, response):
        self._response.append(response)
    def add_action(self, action):
        self._action.append(action)

class JavaClassLanguageMapping(LanguageMapping):

    def mapping(self, modules):

        mapping_result = {}
        for key, module in  modules.items():
            mr = MappingResult(key)
            mapping_result[key] = mr
            for t in module.tables:
                jc = JavaClass(convert(t.name, '_', True), t.comment)
                for f in t.fields:
                    otherType = f.type.split('(')[0]
                    f_name = convert(f.name,'_',False)
                    jf = JavaField(f.name, otherType, f.get_note())
                    jf.metadata = f
                    jc.add_fields(jf)
                mr.add_entity(jc)

            for root_path, g in groupby(module.actions,key=lambda x:x.module_root):
                acs = list(g)
                cj = JavaClass(convert(root_path.split('/')[3], '_', True),'')
                cj.add_annotations('@RequestMapping("' + root_path + '")')
                mr.add_action(cj)
                for a in acs:
                    jm = JavaMethod(self.get_method_name(a), '')
                    cj.add_method(jm)
                    jm.add_annotations(self.get_controller_mapping(a))
                    jm.add_params(self.get_controller_method_params(a))
                    # jc = JavaClass(None, a)
                    # self._do_mapping[jc.class_name] = jc
                    # if url_path.after_module_name() == '' :
                    for g, ps in groupby(a.request.params,key=lambda x:x.group):
                        jc = None
                        if (g == action_metadata.Paramter.DEFAULT_GROUP):
                            jc = JavaClass(a.request.path_name, '')
                        else :
                            jc = JavaClass(g, '')
                        mr.add_request(jc)
                        for p in list(ps):
                            f_name = convert(p.name,'_',False)
                            jf = JavaField(p.name, p.type, p.comment)
                            jc.add_fields(jf)

                    for g, ps in groupby(a.response.params,key=lambda x:x.group):
                        jc = None
                        if (g == action_metadata.Paramter.DEFAULT_GROUP):
                            jc = JavaClass(a.response.path_name, '')
                        else :
                            jc = JavaClass(g, '')
                        mr.add_response(jc)
                        for p in list(ps):
                            f_name = convert(p.name,'_',False)
                            jf = JavaField(p.name, p.type, p.comment)
                            jc.add_fields(jf)
                        pass
        # print(mapping_result)
        analytic(modules)
        return mapping_result

    def get_controller_mapping(self, action):
        mapping = '@' + firstUpower(action.http_method) + 'Mapping'
        url = action.url.replace(action.module_root,'')
        if len(url) > 0:
            mapping += '("'+url+'")'
        return mapping
    def get_controller_method_params(self, action):
        params = []
        for n in action.get_path_variable_name():
            params.append('@PathVariable Long ' + n )
            
        if action.has_request_params():
            _p = ''
            if action.http_method != 'GET':
                _p= '@RequestBody '
            params.append(_p + action.request.path_name + 'DTO dto')

        if action.response_type == action_metadata.ACTION_RESPONSE_TYPE['PAGE']:
            params.append('PageData pagination')
        return params

    def get_method_name(self, action):
        method_name = action.url_path.last_path_name()
        if method_name in ['id','no']:
            method_name = action.url_path.after_module_name() + "By" + firstUpower(method_name)
        else:
            method_name = action.url_path.after_module_name()

        if method_name == '':
            method_name = firstUpower(action.module_name)
        return action.http_method.lower() + method_name

def analytic(modules):
    # for key, module in  modules.items():       
    #     jces = list(map(lambda x:x.java_class, module.tables))
    #     print(key, jces)

    # if url_path.after_module_name() == '' :
        # print(list(map(lambda s: difflib.SequenceMatcher(None, s.lower(), url_path.module_name().lower()).quick_ratio(), class_mapping.keys())))
    # for key,d_java in  do_field_mapping.items():
    #     print(d_java)

    pass

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
        return '.'.join([CONTEXT.package, self._module.name, self.name.replace('-', '.')])

    @property
    def package_path(self):
        return self.java_src + CONTEXT.separator + self.package.replace('.', CONTEXT.separator).replace('-', CONTEXT.separator)

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
        for t in module.entity:
            self.add_class(DOJavaClassMako(self, t.copy()))
            self.add_class(MapperJavaClassMako(self, t.copy()))
            self.add_class(MapperXmlMako(self, t.copy()))
            #没有接口文档时
            if not CONTEXT.has_interface_file :
                self.add_class(TableCommandServiceClassMako(self, t.copy()))
                self.add_class(TableCommandServiceImplClassMako(self, t.copy()))
                self.add_class(TableQueryServiceClassMako(self, t.copy()))
                self.add_class(TableQueryServiceImplClassMako(self, t.copy()))
                self.add_class(TableRepsoitoryClassMako(self, t.copy()))
                self.add_class(TableRspositoryImplClassMako(self, t.copy()))

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
        for t in module.entity:
            #没有接口文档时
            if not CONTEXT.has_interface_file :
                self.add_class(VOJavaClassMako(self, t.copy()))
                self.add_class(DTOJavaClassMako(self, t.copy()))
            # self.add_class(VOJavaClassMako(self, t.java_class.copy()))
            pass

        for jc in module.response:
            self.add_class(VOJavaClassMako(self, jc.copy()))
        for jc in module.request:
            self.add_class(DTOJavaClassMako(self, jc.copy()))

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
        for t in module.entity:
            #没有接口文档时
            if not CONTEXT.has_interface_file :
                self.add_class(TableAdminControllerMako(self, t.copy()))

        for jc in module.action:
            self.add_class(AdminControllerMako(self, jc.copy()))                


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
        super(ControllerJavaProject, self).__init__('controller', module)

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
