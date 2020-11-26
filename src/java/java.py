from ..language import Language, LanguageMapping
from ..module import Module, Project
from ..context import *
from ..utils import *
from ..metadata import *
from .java_class_file import *
from .java_class import *

from mako.template import Template
from mako.runtime import Context
from io import StringIO
import os
from itertools import groupby
import difflib

path = os.path.dirname(os.path.abspath(__file__))# get this file path

class MappingResult(object):
    def __init__(self, name,):
        self._name = name
        self._entity =[]
        self._request = []
        self._response = []
        self._action = []
        self._enums = []
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
    @property
    def enum(self):
        return self._enums
    def add_entity(self, entity):
        self._entity.append(entity)  
    def add_request(self, request):
        self._request.append(request)
    def add_response(self, response):
        self._response.append(response)
    def add_action(self, action):
        self._action.append(action)
    def add_enum(self, enum):
        self._enums.append(enum)

class JavaClassLanguageMapping(LanguageMapping):
    def __init__(self):
        super(JavaClassLanguageMapping, self).__init__()

    def mapping(self, modules):

        mapping_result = {}
        for key, module in  modules.items():
            mr = MappingResult(key)
            mapping_result[key] = mr
            for t in module.tables:
                jc = JavaClass(t.name, t.comment)
                for f in t.fields:
                    otherType = f.type.split('(')[0]
                    jf = JavaField(f.name, otherType, f.get_note())
                    jf.metadata = f
                    jc.add_fields(jf)

                    #enums
                    if f.name in ['type','status']:
                        enums_split = ',' if f.comment.find(',') != -1 else '、'
                        enums_value_split = ':' if f.comment.find(':') != -1 else '：'
                        string_list = str(f.comment).split(enums_split)
                        if len(string_list) > 0:
                            cn = t.name + '_' + f.name 
                            enum = JavaClass(cn, f.comment)
                            mr.add_enum(enum)
                            for n in string_list:
                                string_list = str(n).split(enums_value_split)
                                if len(string_list) == 2: 
                                    ejf = JavaField(string_list[0], 'String', string_list[1])
                                    ejf.metadata = f
                                    enum.add_fields(ejf)
                                else:
                                    print('enums error table(%s) field(%s), %s' % (jc.metadata_name,f.name, string_list))
                                
                mr.add_entity(jc)

            for root_path, g in groupby(module.actions,key=lambda x:x.module_root):
                acs = list(g)
                cj = JavaClass(root_path.split('/')[3],'')
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

class JavaWorkspaceModule(Module):
    def __init__(self):
        super(JavaWorkspaceModule, self).__init__('workspace')
        self._modules = []
    
    def _init_modules(self, mapping_result):
        self._modules.append(ParentModule())
        for key, mr in mapping_result.items():
            self._modules.append(JavaModule(key, mr))

    def generator(self, mapping_result):
        self._init_modules(mapping_result)

        for module in self._modules:
            module.generator()
    
    def write_file(self):
        for module in self._modules:
            module.write_file()

class JavaModule(Module):

    def __init__(self, name, module):
        super(JavaModule, self).__init__(name)
        ## add template project 
        self._projects.append(ServiceJavaProject(self))
        self._projects.append(ApiJavaProject(self))
        self._projects.append(AdminControllerJavaProject(self))
        self._projects.append(ControllerJavaProject(self))
        self._module = module

    @property       
    def path(self):
        return '/'.join([CONTEXT.workspace, self.name])
    @property       
    def package(self):
        return '.'.join([CONTEXT.package, self.name])

    def generator(self, module= {}):
        for p in self._projects:
            p.generator(module if len(module) > 0 else self._module)

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
        pomPath = self.path + CONTEXT.separator + 'pom.xml'
        if os.path.exists(pomPath):
            return   
        with open(pomPath, 'w') as f:
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
            pass
        
        for e in module.enum:
            self.add_class(EnumJavaClassMako(self, e.copy()))

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
