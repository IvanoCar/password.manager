from manager import encryption
import json


class Database:
    storage = None

    def __init__(self):
        self. storage = {}
        self.location = None

    def save_database(self):
        with open(self.location, 'w') as f:
            f.write(encryption.encrypt(json.dumps(self.storage)).decode('utf-8'))
