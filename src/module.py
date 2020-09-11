from . import language
class Module(object):

    def __init__(self, name):
        self._name = name
        self._projects = []

    @property
    def name(self):
        return self._name
        
    def generator(self, module ):
        pass

class Project(object):
    def __init__(self, name, module = Module):
        self._name = name.lower()
        self._module = module

    @property
    def name(self):
        return self._name
        
    def generator(self, module ):
        """解析元数据生成代码和项目相关信息
        """
        pass
