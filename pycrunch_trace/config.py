from pathlib import Path


class TracerConfig:
    absolute_path = '/pycrunch_tracer/samples/module_b.py'
    def __init__(self):
        self.engine_directory = None
        self.working_directory = Path('.')
        self.recording_directory = self.get_default_recording_directory()
        self.package_directory = None

    def get_default_recording_directory(self):
        # return Path('/Volumes/WD_BLACK/pycrunch-trace')
        # return Path('/Volumes/Kingston/pycrunch-trace')
        return Path.joinpath(self.working_directory, 'pycrunch-recordings')

    def set_engine_directory(self, engine_directory: str):
        self.engine_directory = engine_directory

    def set_package_directory(self, package_directory: str):
        self.package_directory = package_directory

config = TracerConfig()

