import io
import json
import pickle
from pathlib import Path


class Snapshot:
    def __init__(self):
        self.snapshot_directory = Path.joinpath(Path(__file__).parent, 'snapshots')

    def save(self, name: str, data):
        self.ensure_snapshot_folder_created()
        file_to_save = self.filename_for_snapshot(name)
        with io.FileIO(file_to_save, mode='w') as file:
            result = self.get_snapshot_bytes(data)
            file.write(result)

    def filename_for_snapshot(self, name):
        return self.snapshot_directory.joinpath(f'{name}.pycrunch-trace')

    def load(self, name: str):
        self.ensure_snapshot_folder_created()
        file_to_load = self.filename_for_snapshot(name)
        with io.FileIO(file_to_load, mode='r') as file:
            buffer = file.readall()
            # try:
                # result = json.loads(buffer)
            # except:
            result = pickle.loads(buffer)
            return result

    def get_snapshot_bytes(self, data):
        # if isinstance(data, dict):
        #     return json.dumps(data, indent=2).encode('utf-8')
        return pickle.dumps(data)


    def ensure_snapshot_folder_created(self):
        if not self.snapshot_directory.exists():
            self.snapshot_directory.mkdir(exist_ok=True)

snapshot = Snapshot()