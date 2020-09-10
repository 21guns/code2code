from . import language

class Project(object):
    def __init__(self, name = ''):
        self._name = name.lower()
        self._modules = []
        self._module_name = Module

    def set_module_name(self, module_name):
        self._module_name = module_name

    def generator(self, modules = {}):
        """解析元数据生成代码和项目相关信息
        """
        for key,values in  modules.items():
            _module = self._module_name(key, values)
            self._modules.append(_module)
            _module.generator()
        

class Module(object):

    def __init__(self, name, moudle_metadata):
        self._name = name
        self._moudle_metadata = moudle_metadata

    def generator(self):
        pass