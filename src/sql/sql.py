from ..language import Language, LanguageMapping, MappingResult
from ..module import Module, Project
import os
from typing import List

from mako.template import Template
from mako.runtime import Context
from io import StringIO
from ..context import CONTEXT

path = os.path.dirname(os.path.abspath(__file__))# get this file path

class Sql(Language):
    def __init__(self,):
        super(Sql, self).__init__('sql')

class SqlLanguageMapping(LanguageMapping):
    def __init__(self):
        super(SqlLanguageMapping, self).__init__()

    def mapping(self, modules):
        tables = []
        for key, module in  modules.items():
            tables = tables + module.tables

        return tables

class SqlModule(Module):
    def __init__(self):
        super(SqlModule, self).__init__('sql')
        self._buf = None

    @property       
    def path(self):
        return '/'.join([CONTEXT.workspace, self.name])

    def generator(self, tables:List):
        # print(type(tables))
        if not isinstance(tables, list) :
            print('sql just support list, get type(%s)' % (type(tables)))
            return
        template = Template(filename = path + '/sql.tl', input_encoding='utf-8')
        self._buf = StringIO()
        ctx = Context(self._buf, tables = tables)
        template.render_context(ctx)

    def write_file(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        pomPath = self.path + CONTEXT.separator + 'database-init.sql'
        # if os.path.exists(pomPath):
        #     return   
        with open(pomPath, 'w') as f:
            f.write(self._buf.getvalue())
            f.close()