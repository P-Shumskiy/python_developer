from pathlib import Path


class FileReader:
    def __init__(self, path):
        self.path = Path(path)

    def read(self):
        try:
            with open(self.path, "r") as f:
                content = f.read().strip()
                return content
        except FileNotFoundError:
            return ""
