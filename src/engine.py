from . import module
from . import language

class Engine(object):
    def __init__(self):
        self._modules = []

    def reader(self):
        self._reader = Reader(self)
        return self._reader


class Reader(object):
    def __init__(self, engine):
        self._engine = engine

    def reader_table(self):
        
        return self

    def reader_interface(self):
        
        return self

    def config_mapping(self, cfg_mapping = language.LanguageMapping):
        self._cfg_mapping = Mapping(self._engine, cfg_mapping)
        return self._cfg_mapping

class Mapping(object):
    def __init__(self, engine, cfg_mapping):
        self._engine = engine
        self._cfg_mapping = cfg_mapping

    def mapping(self, modules):
        if (self._cfg_mapping is not None):
            self._cfg_mapping().mapping(modules)
        return self

    def config_module(self, cfg_module = module.Module):
        """配置模板类，模板类用于生产模块代码
        """
        self._cfg_module = Module(self._engine, cfg_module)
        return self._cfg_module

class Module(object):

    def __init__(self, engine, cfg_module):
        self._engine = engine
        self._cfg_module = cfg_module
        self._modules = []

    def add_module(self, module):
        """添加自动以模块
        """
        self._modules.append(module)
        return self

    def generator(self, modules):
        """解析元数据生成模块信息
        """

        ##生产内容
        for key, module in  modules.items():
            _module = self._cfg_module(key)
            self._modules.append(_module)
            _module.generator(module)

        ##写入文件
        for m in self._modules:
            m.write_file()
        pass    
