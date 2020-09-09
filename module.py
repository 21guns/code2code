class Project(object):
    def __init__(self, name = ''):
        self._name = name.lower()
        self._modules = []

    def parse(self, modules = {}):
        """解析元数据生成代码和项目相关信息
        """
        for key,values in  modules.items():
            print (key,values)
        
    def generator(self, parameter_list):
        pass
def new_project(name = ''):
    return Project(name)

class Module(object):
    pass