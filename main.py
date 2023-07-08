
import sys
import pywebio

from utils import config
from utils import books as ubooks
from views import home  as vhome

def init_env():
    cfg = dict(quiet=True)
    config.set(cfg)

    bsi = ubooks.BooksInfo()
    #bsi.scanImageFolderInPath("./books")
    #bsi.scanImagePackInPath("./packs-cn")
    bsi.scanImagePackInPath("./packs-safe")
    ubooks.setBooksInfo(bsi)

def main():
    vhome.view()

try:
    init_env()
    pywebio.start_server(main, port=8089, debug=True)

except KeyboardInterrupt:
    print("User Interrupt, exit.")
    ubooks.getBooksInfo().saveData()
    sys.exit(0)
