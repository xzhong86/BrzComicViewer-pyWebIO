
import os
import re
import hashlib
import glob
import zipfile
import yaml

NAME_PATTERN = "book-u{index}-{hash}"

def unpack_file(filename, outdir=""):
    unpack_dir = get_unpack_dir(filename, outdir)
    if (unpack_dir == None):
        return None
    if (os.path.isdir(unpack_dir)):
        return unpack_dir

    if (zipfile.is_zipfile(filename)):
        unpack_zip(filename, unpack_dir)
    else:
        print("unknown file type")
        return None

    gen_book_info(filename, unpack_dir)
    return unpack_dir

def gen_book_info(filename, unpack_dir):
    title = os.path.basename(filename)
    info = { ":title" : title, ":url" : "", ":tags" : [] }
    fh = open(os.path.join(unpack_dir, "info.yaml"), 'w')
    yaml.safe_dump(info, fh)
    fh.close()

def get_filename_hash(filename):
    basename = os.path.basename(filename)
    hash_str = hashlib.md5(filename.encode('utf-8')).hexdigest()
    return hash_str[0:8]

def get_unpack_dir(filename, outdir):
    if (not os.path.isdir(outdir)):
        print(f'path {outdir} not exists!')
        return None

    hash_id = get_filename_hash(filename)

    max_idx = 0
    name_re = re.compile("book-u([0-9]+)-([0-9a-f]+)")
    for item in glob.glob(os.path.join(outdir, "book-u*")):
        m = name_re.search(item)
        if (m != None):
            idx, hid = int(m[1]), m[2]
            if (hid == hash_id):
                print(f"book {item} possiblly is {filename}")
                return item
            if (idx > max_idx):
                max_idx = idx

    book_idx = "%03d" % (max_idx + 1)
    dir_name = NAME_PATTERN.format(index=book_idx, hash=hash_id)
    return os.path.join(outdir, dir_name)

def unpack_zip(filename, unpack_dir):
    print(f'unpack {filename} into {unpack_dir} ...')

    zfile = zipfile.ZipFile(filename, 'r')
    os.mkdir(unpack_dir)   # must not exists
    zfile.extractall(unpack_dir)
    zfile.close()
    
