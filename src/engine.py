from . import module

class Engine(object):
    def __init__(self):
        self._modules = []

    def config(self):
        self._config = Config(self)
        return self._config

    def reader_table(self):
        pass

    def generator(self, modules):
        """解析元数据生成模块信息
        """
        for key, module in  modules.items():
            _module = self._config._module(key)
            self._modules.append(_module)
            _module.generator(module)

        pass

class Config(object):
    _table_reader = None
    _interface_reader = None

    def __init__(self, engine):
        self._engine = engine
        self._module = None

    def module(self, module_name = module.Module):
        self._module = module_name
        return self

    def finsh(self):
        """完成配置
        """
        return self._engine
