#!/usr/env python3

import json

class DataBase:
    def __init__(self, path, user):
        self.file_path = path
        self.user = user
        with open(path, 'r', encoding='utf-8') as fh:
            self.all_data  = json.load(fh)
            self.user_data = self.all_data.get(user) or {}

    def lookup(self, book):
        data = self.user_data
        return data.get(book.hash_id) or data.get(book.name) or None

    def saveData(self, bsi):
        books_data = {}
        for book in bsi.books:
            data = book.getDataToSave()
            if data:
                books_data[book.hash_id] = data

        for key, value in books_data.items():
            self.user_data[key] = value

        self.all_data[self.user] = self.user_data
        with open(self.file_path, 'w', encoding='utf-8') as fh:
            json.dump(self.all_data, fh, indent=4, sort_keys=True, ensure_ascii=False)


def init(datafile, user):
    return DataBase(datafile, user)


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


