import json
import os

class JsonTaskStore:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)
            return []
        
        with open(self.file_path, "r") as f:
            return json.load(f)
        
    def save(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)
            