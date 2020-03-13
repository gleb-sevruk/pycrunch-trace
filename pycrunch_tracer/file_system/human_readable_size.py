class HumanReadableByteSize:
    def __init__(self, total_bytes: int):
        self.total_bytes = total_bytes

    def __str__(self):
        return self.human_readable_size(self.total_bytes)

    @staticmethod
    def human_readable_size(size, decimal_places=1):
        if size < 1024:
            return f"{round(size)} bytes"
        for unit in ['B', 'Kb', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                break
            size /= 1024.0
        return f"{size:.{decimal_places}f} {unit}"
