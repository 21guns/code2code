class Language(object):
    def __init__(self, name):
        self._name = name.lower()

    def __str__(self):
        return 'Language: %s' % (self.name)

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name 
class Xml(Language):
    def __init__(self,):
        super(Xml, self).__init__('xml')



class LanguageMapping(object):

    """映射meteadata到具体语言
    """
    def __init__(self):
        pass

    def mapping(self, moudles = {}):
        
        return moudles

class MappingResult(object):
  
    """映射后的结果集
    """
    def __init__(self):
        pass  