class TracerConfig:
    absolute_path = '/pycrunch_tracer/samples/module_b.py'
    def __init__(self):
        self.engine_directory = None

    def set_engine_directory(self, engine_directory: str):
        self.engine_directory = engine_directory

config = TracerConfig()

