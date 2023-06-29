
import os
from os.path import isfile, join

import yaml
import re

class ImageInfo:
    def __init__(self, dir_path, fname):
        self.path = join(dir_path, fname)
        self.file_name = fname
        self.dir_path  = dir_path

    def read(self):
        if (not isfile(self.path)):
            print("bad path: " + self.path)
        else:
            print("read file: " + self.path)
        return open(self.path, 'rb').read()


class BookInfo:
    def __init__(self, path):
        self.orig_path = path
        if (os.path.isfile(path)):
            tryUnpackBook()
        elif (os.path.isdir(path)):
            self.dir_path = path

        self.name = os.path.basename(path)
        self.scanDir()

    def scanDir(self):
        _dir  = self.dir_path
        files = [f for f in os.listdir(_dir) if isfile(join(_dir, f)) ]
        re_ext = re.compile("(jpg|jpeg|png)$")
        imgs  = [f for f in files if re_ext.search(f) ]
        imgs.sort()
        self.images = [ ImageInfo(_dir, img) for img in imgs ]

        self.url = None
        self.title = self.name
        self.tags = None
        info_file = join(_dir, "info.yaml")
        if (isfile(info_file)):
            with open(info_file) as stream:
                info = yaml.safe_load(stream)
                self.url   = info[':url']
                self.title = info[':title']
                self.tags  = info[':tags']

    def tryUnpackBook(self):
        raise "to be done"


class BooksInfo:
    def __init__(self):
        self.books = []

    def scanImageFolderInPath(self, path):
        dirs = [d for d in os.listdir(path) if os.path.isdir(join(path, d)) ]
        books = [ BookInfo(join(path, d)) for d in dirs ]
        print(str(len(books)) + " books found in " + path)
        books.sort(key=lambda b: b.name)
        self.books += books

