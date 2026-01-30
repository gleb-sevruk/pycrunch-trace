import os
from pathlib import Path


class TracerConfig:
    absolute_path = '/pycrunch_tracer/samples/module_b.py'

    def __init__(self):
        self.engine_directory = None
        self.working_directory = Path('.')
        self.recording_directory = self.get_default_recording_directory()
        self.package_directory = None

        # S3 Settings
        self.s3_enabled = os.environ.get('PYCRUNCH_S3_ENABLED', 'False').lower() == 'true'
        self.s3_bucket = os.environ.get('PYCRUNCH_S3_BUCKET')
        self.s3_prefix = os.environ.get('PYCRUNCH_S3_PREFIX', '')

        # Builtin exclusion
        self.exclude_builtins = os.environ.get('PYCRUNCH_EXCLUDE_BUILTINS', 'True').lower() == 'true'

        # Session preservation
        self.keep_sessions = os.environ.get('PYCRUNCH_KEEP_SESSIONS', 'True').lower() == 'true'

        # Organization
        self.organize_by_date = os.environ.get('PYCRUNCH_ORGANIZE_BY_DATE', 'False').lower() == 'true'

    def get_default_recording_directory(self):
        return Path.joinpath(self.working_directory, 'pycrunch-recordings')

    def set_engine_directory(self, engine_directory: str):
        self.engine_directory = engine_directory

    def set_package_directory(self, package_directory: str):
        self.package_directory = package_directory


config = TracerConfig()

