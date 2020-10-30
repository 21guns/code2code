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
        self._mapping_result = None

    def mapping(self, modules):
        if (self._cfg_mapping is not None):
            self._mapping_result = self._cfg_mapping().mapping(modules)
        return self

    def config_module(self, cfg_module = module.Module):
        """配置模板类，模板类用于生产模块代码
        """
        self._cfg_module = Module(self, self._engine, cfg_module)
        return self._cfg_module
    @property
    def result(self):
        return self._mapping_result

class Module(object):

    def __init__(self, mapping, engine, cfg_module):
        self._engine = engine
        self._cfg_module = cfg_module
        self._modules = []
        self._mapping  = mapping

    def add_module(self, module):
        """添加自定义模块
        """
        self._modules.append(module)
        return self

    def generator(self):
        """解析元数据生成模块信息
        """

        ##生成内容
        for key, module in  self._mapping.result.items():
            _module = self._cfg_module(key)
            self._modules.append(_module)
            _module.generator(module)

        ##写入文件
        for m in self._modules:
            m.write_file()
        pass    
