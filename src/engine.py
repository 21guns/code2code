from . import module, context
from . import language

class Reader(object):
    def __init__(self, engine):
        self._engine = engine

    def reader(self, context = context.Context()):
        pass

class EngineBuilder(object):
    def __init__(self):
        self._engine = None
        self._context = None
        self._reader_cfg = None 
        self._pipeline_cfg = []

    def reader(self, reader = Reader):
        self._reader_cfg = reader
        return self

    def pipleline(self) :
        pip = PipelineBuilder(self)
        self._pipeline_cfg.append(pip)
        return pip

    def build(self):
        self._engine = Engine()
        self._engine.reader = self._reader_cfg(self._engine)
        for pip in self._pipeline_cfg:
            pass

        return self._engine
             
class PipelineBuilder(object):
    def __init__(self, engine_builder):
        self._language_mapping_cfg = None
        self._modules_cfg = []
        self._engine_builder = engine_builder

    def mapping(self, language_mapping = language.LanguageMapping):
        self._language_mapping_cfg = language_mapping
        return self

    def modules(self, *modules ):
        self._modules_cfg = modules
        return self

    def end(self):
        return self._engine_builder

    def get_mapping(self):
        return self._language_mapping_cfg
    
    def get_modules(self):
        return self._modules_cfg

class Pipeline(object):
    def __init__(self, engine):
        self._language_mapping = None
        self._modules = []
        self._engine = engine

    def mapping(self, language_mapping = language.LanguageMapping):
        self._language_mapping = language_mapping
        return self

    def modules(self, *modules ):
        self._modules = modules
        return self

    def run(self, **modules):
        mapping_result = self._language_mapping.mapping(modules)

        ##生成内容
        for key, module in  mapping_result.items():
            _module.generator(module)

        ##写入文件
        for m in self._modules:
            m.write_file()
        pass    

    @property
    def mapping(self):
        return self._language_mapping
    @property
    def modules(self):
        return self._modules

class Engine(object):
    def __init__(self):
        self._reader = None
        self._pipeline = []

    def run(self, context):
        modules = self._reader.reader(context)
        print(modules)
        for pipeline in self._pipeline:
            pipeline.run(modules) 

    @property
    def reader(self):
        return self._reader
    @reader.setter
    def reader(self, reader):
        self._reader = reader

class MdReader(Reader):
    def __init__(self, engine):
        super(MdReader, self).__init__(engine)

    def reader(self, context = context.Context()):
        pass
