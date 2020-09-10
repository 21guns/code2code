from ..language import Language
from ..module import Module
from ..context import *
from mako.template import Template
from mako.runtime import Context
from io import StringIO
import os

java_src = '/src/main/java'
resource_src = '/src/main/resources/'

class Java(Language):
    def __init__(self, class_name):
        super(Java, self).__init__('java')
        self._class_name = class_name

    def get_package_name(self):
        pass

class JavaClassMako(Java):
    def __init__(self, class_name, tl_file):
        super(JavaClassMako, self).__init__(class_name)
        self._template = Template(filename = tl_file)


def DO(class_name):
    return JavaClassMako(class_name, './tl/service/do.tl')


class JavaModule(Module):
    def __init__(self, name, moudle_metadata):
        super(JavaModule, self).__init__(name, moudle_metadata)

    def generator(self):
        ## 1.mk dir
        workspace_root = CONTEXT.workspace + self._name
        if not os.path.exists(workspace_root):
            os.makedirs(workspace_root)
        path = os.path.dirname(os.path.abspath(__file__))# get this file path
        os.system('cp -r ' + path + '/template/module/* '+ workspace_root)

        print(self._moudle_metadata.tables)
        self._moudle_metadata.tables
        pass
    