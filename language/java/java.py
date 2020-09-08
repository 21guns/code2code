from .. import language
from mako.template import Template
from mako.runtime import Context
from io import StringIO

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


def dto(class_name):
    return JavaClassMako(class_name, './tl/service/do.tl')
    