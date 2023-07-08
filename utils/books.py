
import os
import re
from os.path import isfile, join

import hashlib
import humanize
import yaml

from utils import config
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
            if not config.opt.quiet:
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
        self.data_items = dict(
            like=0, view=0, style=0, quality=0, sotry=0, desc="", tags=[]
        )
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
        self.orig_tags = [ ]
        info_file = join(_dir, "info.yaml")
        if (isfile(info_file)):
            with open(info_file) as stream:
                info = yaml.safe_load(stream)
                self.url   = info[':url']
                self.title = info[':title']
                self.orig_tags  = info[':tags']

        self.hash_id = get_str_hash(self.title, 12)

    def updateInfo(self):
        data = self.db.lookup(self) or {}

        for item, val in self.data_items.items():
            if not item in data:
                data[item] = val

        self.data = data
        for item, value in data.items():
            setattr(self, item, value)

    def getDataToSave(self):
        data  = { item : getattr(self, item) for item in self.data_items }
        valid_cnt = len([ v for v in data.values() if v ])
        return data if valid_cnt > 0 else None
        #return data

    def tryUnpackBook(self):
        raise "to be done"


class BooksInfo:
    def __init__(self):
        self.books = []
        self.user = config.opt.default_user
        data_file = config.opt.json_data_file
        self.db = database.init(data_file, self.user)

    def saveData(self):
        print("Save data of books.")
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
        unpack_root = config.opt.unpack_dir
        files = self.scanPacks(dirpath)
        files.sort()

        for item_path in files:
            bkdir = unpack.unpack_file(item_path, unpack_root)
            if (bkdir != None):
                book  = BookInfo(bkdir, self.db)
                self.books.append(book)
                

glb_books_info = None
def setBooksInfo(bsi):
    global glb_books_info
    glb_books_info = bsi

def getBooksInfo():
    return glb_books_info
