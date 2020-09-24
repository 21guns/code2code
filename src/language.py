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


class Sql(Language):
    def __init__(self,):
        super(Sql, self).__init__('sql')

class LanguageMapping(object):

    """映射meteadata到具体语言
    """
    def __init__(self):
        pass

    def mapping(self, moudles):
        pass