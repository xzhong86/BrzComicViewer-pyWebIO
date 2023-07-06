
import os
import re
from os.path import isfile, join

import hashlib
import humanize
import yaml

from utils import unpack
from utils import database
from utils import thumbnail

class ImageInfo:
    def __init__(self, dir_path, fname):
        self.path = join(dir_path, fname)
        self.file_name = fname
        self.dir_path  = dir_path

    def read(self, thumb=False):
        if (not isfile(self.path)):
            print("bad path: " + self.path)
            return None
        else:
            if (thumb):
                path = thumbnail.get_thumbnail(self.path)
            else:
                path = self.path
            fh = open(path, 'rb')
            content = fh.read()
            fh.close()
            size = humanize.naturalsize(len(content))
            print(f"read file: {size} " + self.path)
            return content

def get_str_hash(_str, len = 8):
    hash_str = hashlib.md5(_str.encode('utf-8')).hexdigest()
    len = 16 if len > 16 else len
    len = 8  if len < 8  else len
    return hash_str[0:len]

class BookInfo:
    def __init__(self, path, database):
        self.orig_path = path
        self.db = database
        if (os.path.isfile(path)):
            tryUnpackBook()
        elif (os.path.isdir(path)):
            self.dir_path = path
            self.dir_name = os.path.basename(path)
        else:
            raise "what happened?"

        self.name = os.path.basename(path)
        self.scanDir()
        self.updateInfo()

    def scanDir(self):
        _dir  = self.dir_path
        files = [f for f in os.listdir(_dir) if isfile(join(_dir, f)) ]
        re_ext = re.compile("(jpg|jpeg|png)$")
        imgs  = [f for f in files if re_ext.search(f) ]
        imgs.sort()
        self.images = [ ImageInfo(_dir, img) for img in imgs ]

        self.url = None
        self.title = self.name
        self.tags = [ ]
        info_file = join(_dir, "info.yaml")
        if (isfile(info_file)):
            with open(info_file) as stream:
                info = yaml.safe_load(stream)
                self.url   = info[':url']
                self.title = info[':title']
                self.tags  = info[':tags']

        self.hash_id = get_str_hash(self.title, 8)

    def updateInfo(self):
        data = self.db.lookup(self)
        if (data == None):
            data = dict(like=0, view=0)
        self.data = data
        self.like = data['like']
        self.view = data['view']
        # style, quality, story

    def getDataToSave(self):
        data = dict(like=self.like,
                    view=self.view)
        return data

    def tryUnpackBook(self):
        raise "to be done"


class BooksInfo:
    def __init__(self):
        self.books = []
        self.user = 'zpzhong'
        self.db = database.init(self.user)

    def saveData(self):
        self.db.saveData(self)

    def scanImageFolderInPath(self, path):
        dirs = [d for d in os.listdir(path) if os.path.isdir(join(path, d)) ]
        books = [ BookInfo(join(path, d), self.db) for d in dirs ]
        print(str(len(books)) + " books found in " + path)
        books.sort(key=lambda b: b.name)
        self.books += books

    def scanPacks(self, dirpath):
        files = []
        zip_re = re.compile("\.(zip|rar|cbz|cbr)$")
        for item in os.listdir(dirpath):
            path = join(dirpath, item)
            if (os.path.isfile(path) and zip_re.search(item)):
                files.append(path)
            elif (os.path.isdir(path)):
                files = files + self.scanPacks(path)

        return files
        
    def scanImagePackInPath(self, dirpath):
        unpack_root = "books"
        files = self.scanPacks(dirpath)
        files.sort()

        for item_path in files:
            bkdir = unpack.unpack_file(item_path, unpack_root)
            if (bkdir != None):
                book  = BookInfo(bkdir, self.db)
                self.books.append(book)
                

