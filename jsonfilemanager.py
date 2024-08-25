import json
import os


class JSONFIleManager:
    def __init__(self, filename):
        self.filename = filename

    def load_data(self) -> list:
        """ loads the data from the file and returns it"""
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as file:
                json.dump([], file, indent=4)
                return []
        else:
            with open(self.filename, 'r') as file:
                return json.load(file)

    def save_data(self, data) -> bool:
        """ receives data and saves it in the file"""
        try:
            with open(self.filename, 'w') as file:
                json.dump(data, file, indent=4)
                return True
        except Exception as e:
            print(e)
            return False

