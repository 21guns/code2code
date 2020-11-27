from . import module, context, logging
from . import language, reader


class EngineBuilder(object):
    def __init__(self):
        self._engine = None
        self._context = None
        self._reader_cfg = None 
        self._pipeline_cfg = []

    def reader(self, reader = reader.Reader):
        self._reader_cfg = reader
        return self

    def pipleline(self) :
        pip = PipelineBuilder(self)
        self._pipeline_cfg.append(pip)
        return pip

    def build(self):
        self._engine = Engine()

        self._engine.reader(self._reader_cfg(self._engine))\
            .pipeline(list(map(lambda p:p.build(self._engine), self._pipeline_cfg)))

        return self._engine
             
class PipelineBuilder(object):
    def __init__(self, engine_builder):
        self._language_mapping_cfg = None
        self._modules_cfg = []
        self._engine_builder = engine_builder
        self._pipeline = None

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

    def build(self, engine):
        self._pipeline = Pipeline(engine)
        self._pipeline.mapping(self._language_mapping_cfg())\
            .modules(list(map(lambda m: m(), self._modules_cfg)))
        return self._pipeline
            
class Pipeline(object):
    def __init__(self, engine):
        self._language_mapping = None
        self._modules = []
        self._engine = engine

    def mapping(self, language_mapping = language.LanguageMapping):
        self._language_mapping = language_mapping
        return self

    def modules(self, modules ):
        self._modules = modules
        return self

    def run(self, modules):
        mapping_result = self._language_mapping.mapping(modules)
        ##生成内容
        for module in self._modules:
            module.generator(mapping_result)

        ##写入文件
        for m in self._modules:
            m.write_file()
        pass    

    def get_mapping(self):
        return self._language_mapping
    
    def get_modules(self):
        return self._modules

class Engine(object):
    def __init__(self):
        self._reader = None
        self._pipeline = []
        self._context = None

    def run(self, context):
        modules = self._reader.reader(context)
        for pipeline in self._pipeline:
            pipeline.run(modules) 

    @property
    def reader(self):
        return self._reader

    def reader(self, reader):
        self._reader = reader
        return self
    def pipeline(self, pipeline):
        self._pipeline = pipeline
        return self
    def add_pipeline(self, pipeline):
        self._pipeline.append(pipeline)
        return self
