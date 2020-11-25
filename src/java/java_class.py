from ..context import *

from mako.template import Template
from mako.runtime import Context
from io import StringIO
import os

path = os.path.dirname(os.path.abspath(__file__))# get this file path

class JavaClass(object):
    def __init__(self, project, java_class):
        self._project = project
        self._java_class = java_class.set_project(project)
    @property
    def class_path(self):
        return self._project.java_src + CONTEXT.separator + self._java_class.package.replace('.', CONTEXT.separator)

    def generator(self):
        pass

    def write_file(self):
        pass


class JavaClassMako(JavaClass):
    def __init__(self, project, java_class, tl_file):
        super(JavaClassMako, self).__init__(project, java_class)
        self._template = Template(filename = tl_file,  input_encoding='utf-8')
        self._buf = None

    @property
    def class_path(self):
        return self._project.java_src + CONTEXT.separator + self._java_class.package.replace('.', CONTEXT.separator)

    def generator(self):
        self._buf = StringIO()
        ctx = Context(self._buf, java_class = self._java_class)
        self._template.render_context(ctx)
        pass

    def write_file(self):
        if (self._buf is None):
            return
        if not os.path.exists(self.class_path):
            os.makedirs(self.class_path)
        with open(self.class_path + CONTEXT.separator + self._java_class.file_name, 'w') as f:
            f.write(self._buf.getvalue())
            f.close()

class ResourceMako(JavaClassMako):
    def __init__(self, project, java_class, tl_file):
        super(ResourceMako, self).__init__(project, java_class, tl_file)
        java_class.name = 'xml'
    
    @property
    def resource_path(self):
        return self._project.resource_src + CONTEXT.separator + self._java_class.package.replace('.', CONTEXT.separator)


    def write_file(self):
        if (self._buf is None):
            return
        if not os.path.exists(self.resource_path):
            os.makedirs(self.resource_path)
        with open(self.resource_path + CONTEXT.separator + self._java_class.file_name, 'w') as f:
            f.write(self._buf.getvalue())
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

class DTOJavaClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(DTOJavaClassMako, self).__init__(project, java_class, path + '/tl/api/dto.tl')
        java_class.set_package('dto')
        java_class.set_class_name_suffix('DTO')

class EnumJavaClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(EnumJavaClassMako, self).__init__(project, java_class, path + '/tl/api/enum.tl')
        java_class.set_package('enums')
        java_class.set_class_name_suffix('Enum')

    def generator(self):
        for field in self._java_class.fields:
            if field.name in ['type','status']:
                enums = []
                string_list = str(field.note).split(',')
                if len(string_list) > 0:
                    for n in string_list:
                        # if  len(n) >0:
                        # print(string_list)
                        string_list = str(n).split(':')
                        if len(string_list) == 2: 
                            f = enum(string_list[0],string_list[1])
                            if f is not None:
                                enums.append(f)
                        else:
                            print('enums error table(%s) field(%s), %s' % (self._java_class.metadata_name,field.name, string_list))
        pass

    def write_file(self):

        pass


class MapperJavaClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(MapperJavaClassMako, self).__init__(project, java_class, path + '/tl/service/mapper/mapper.tl')
        java_class.set_package('repository.mapper')
        java_class.set_class_name_suffix('Mapper')

class MapperXmlMako(ResourceMako):
    def __init__(self, project, java_class):
        super(MapperXmlMako, self).__init__(project, java_class, path + '/tl/service/mapper/mapperXml.tl')
        java_class.set_package('repository.mapper')
        java_class.set_class_name_suffix('Mapper')

class TableCommandServiceClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(TableCommandServiceClassMako, self).__init__(project, java_class, path + '/tl/service/table/commandService.tl')
        java_class.set_package('command')
        java_class.set_class_name_suffix('CommandService')

class TableCommandServiceImplClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(TableCommandServiceImplClassMako, self).__init__(project, java_class, path + '/tl/service/table/commandServiceImpl.tl')
        java_class.set_package('command.impl')
        java_class.set_class_name_suffix('CommandServiceImpl')

class TableQueryServiceClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(TableQueryServiceClassMako, self).__init__(project, java_class, path + '/tl/service/table/queryService.tl')
        java_class.set_package('query')
        java_class.set_class_name_suffix('QueryService')

class TableQueryServiceImplClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(TableQueryServiceImplClassMako, self).__init__(project, java_class, path + '/tl/service/table/queryServiceImpl.tl')
        java_class.set_package('query.impl')
        java_class.set_class_name_suffix('QueryServiceImpl')

class TableRepsoitoryClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(TableRepsoitoryClassMako, self).__init__(project, java_class, path + '/tl/service/table/repository.tl')
        java_class.set_package('repository')
        java_class.set_class_name_suffix('Repository')

class TableRspositoryImplClassMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(TableRspositoryImplClassMako, self).__init__(project, java_class, path + '/tl/service/table/repositoryImpl.tl')
        java_class.set_package('repository.impl')
        java_class.set_class_name_suffix('RepositoryImpl')

class TableAdminControllerMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(TableAdminControllerMako, self).__init__(project, java_class, path + '/tl/controller/table/adminController.tl')
        # java_class.set_package('admin.controller')
        java_class.set_class_name_suffix('Controller')
        java_class.set_class_name_prefix('Admin')


class AdminControllerMako(JavaClassMako):
    def __init__(self, project, java_class):
        super(AdminControllerMako, self).__init__(project, java_class, path + '/tl/controller/adminController.tl')
        # java_class.set_package('admin.controller')
        java_class.set_class_name_suffix('Controller')
        java_class.set_class_name_prefix('Admin')
