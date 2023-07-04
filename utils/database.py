#!/usr/env python3

import json

DATA_FILE = "data/comic-data.json"

class DataBase:
    def __init__(self, path, user):
        self.file_path = path
        self.user = user
        with open(path, 'r') as fh:
            self.all_data  = json.load(fh)
            self.user_data = self.all_data[user]

    def lookup(self, book):
        data = self.user_data
        if (book.hash_id in data):
            return data[book.hash_id]
        if (book.name in data):
            return data[book.name]
        return None

    def saveData(self, books):
        data = {}
        for book in books.books:
            data[book.hash_id] = book.getDataToSave()
        self.all_data[self.user] = data

        with open(self.file_path, 'w') as fh:
            json.dump(self.all_data, fh, indent=4, sort_keys=True)


def init(user):
    return DataBase(DATA_FILE, user)


if __name__ == "__main__":
    # transform old data
    import yaml
    import sys
    filename = sys.argv[1]
    data = yaml.safe_load(open(filename, "r"))
    for book, info in data.items():
        ninfo = { 'like' : info[':like'], 'view' : info[':view'] }
        data[book] = ninfo
    new = { "zpzhong" : data }
    json.dump(new, open(DATA_FILE, "w"))


