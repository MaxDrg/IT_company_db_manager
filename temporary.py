import json

class Connection:
    def __init__(self):
        self.file = 'json/connection.json'

    def get(self):
        with open(self.file, "r") as data:
            return json.load(data)

    def set(self, login, passwd):
        saved_data: dict = self.get()
        new_data = { 
            'login': str(login),
            'password': str(passwd)
        }
        saved_data.update(new_data)
        with open(self.file, "w") as data:
            json.dump(saved_data, data, indent=2)