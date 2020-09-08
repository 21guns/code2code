class Language(object):
    def __init__(self, name):
        self._name = name.lower()
    def __str__(self):
        return 'Metadata: %s' % (self.name)
    @property
    def name(self):
        return self._name

    def get_file_name(self):
        pass
    
    def content(self):
        """
            返回代码内容
        """
        pass
    
class Code(object):
    pass

]class Xml(Language):
    def __init__(self,):
        super(Xml, self).__init__('xml')


class Sql(Language):
    def __init__(self,):
        super(Sql, self).__init__('sql')