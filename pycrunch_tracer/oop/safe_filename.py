class SafeFilename:
    possibly_unsafe_filename: str

    def __init__(self, possibly_unsafe_filename: str):
        self.possibly_unsafe_filename = possibly_unsafe_filename

    def __str__(self):
        return self._make_safe_filename()

    def _make_safe_filename(self):
        def safe_char(c):
            if c.isalnum():
                return c
            else:
                return "_"

        return "".join(safe_char(c) for c in self.possibly_unsafe_filename).rstrip("_")


