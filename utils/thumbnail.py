
import os
from PIL import Image

THUMB_DIR = ".thumbnail"

def get_thumbnail(img_path):
    dir_  = os.path.dirname(img_path)
    name  = os.path.basename(img_path)
    thumb = os.path.join(dir_, THUMB_DIR, name)
    if (os.path.isfile(thumb)):
        return thumb
    else:
        create_thumbnail(img_path, thumb)
        return thumb
        
def create_thumbnail(img_path, thumb):
    thumb_dir = os.path.dirname(thumb)
    if (not os.path.exists(thumb_dir)):
        os.mkdir(thumb_dir)

    with Image.open(img_path) as img:
        size = 400, 400
        img.thumbnail(size)
        img.save(thumb)

