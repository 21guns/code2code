from . import module

class Engine(object):

    def config(self):
        self._config = Config(self)
        return self._config

    def reader_table(self):
        pass

    def generator(self, modules):
        """解析元数据生成模块信息
        """
        self._config._project.generator(modules)
        pass

class Config(object):
    _table_reader = None
    _interface_reader = None

    def __init__(self, engine):
        self._engine = engine
        self._project = None

    def project(self, project = module.Project()):
        self._project = project
        return self

    def module(self, module_name = module.Module):
        if (self._project is None):
            self._project = module.Project()
        self._project.set_module_name(module_name)
        return self

    def finsh(self):
        """完成配置
        """
        return self._engine
