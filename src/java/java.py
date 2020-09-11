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

class JavaClassMako(Java):
    def __init__(self, project, tl_file):
        super(JavaClassMako, self).__init__()
        self._project = project
        self._class_metadata = None
        self._template = Template(filename = tl_file)
        self._package = ''
        self._class_name_suffix = ''
        self._project.add_class(self)

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

    def set_package(self, package):
        self._package = package
        return self

    def set_class_name_suffix(self, suffix):
        self._class_name_suffix = suffix
        return self
    # def has_id():
        
    def generator(self, module):
        buf = StringIO()
        ctx = Context(buf, java_class = self)
        self._template.render_context(ctx)
        f = open(self._project.java_src + self.file_name, 'w')
        # f.write(buf.getvalue())
        # f.close()

def DO(project):
    return JavaClassMako(project, path + '/tl/service/do.tl')\
            .set_package('service.entity')\
            .set_class_name_suffix('DO')


class JavaProject(Project):
    java_src = '/src/main/java'
    resource_src = '/src/main/resources/'

    def __init__(self, name, module):
        super(JavaProject, self).__init__(name, module)
        self._class = []

    @property
    def package(self):
        return '.'.join([CONTEXT.package, self.name])

    @property
    def java_src(self):
        return self.module.module_path + java_src

    def add_class(self, java_class):
        self._class.append(java_class)

    def generator(self, module):
        """解析元数据生成代码和项目相关信息
        """
        for c in self._class:
            c.generator(module)

#----java template project
def service(module):
    jp = JavaProject('service', module)
    DO(jp)
    return jp


class JavaModule(Module):

    def __init__(self, name):
        super(JavaModule, self).__init__(name)

    @property       
    def module_path(self):
        return  CONTEXT.workspace + self._name

    def generator(self, module):
        ## 1.mk dir
        if not os.path.exists(self.module_path):
            os.makedirs(self.module_path)
        os.system('cp -r ' + path + '/template/module/* '+ self.module_path)
        ## 2.add template project 
        sp = service(self)
        self._projects.append(sp)

        for p in self._projects:
            p.generator(module)

        pass
    