
import sys
import pywebio

from views import mainView
from utils import books as ubooks
from utils import config

def init_env():
    cfg = dict(quiet=True)
    config.set(cfg)

    bsi = ubooks.BooksInfo()
    #bsi.scanImageFolderInPath("./books")
    #bsi.scanImagePackInPath("./packs-cn")
    bsi.scanImagePackInPath("./packs-safe")
    ubooks.setBooksInfo(bsi)

def main():
    mainView.view()

try:
    init_env()
    pywebio.start_server(main, port=8089, debug=True)

except KeyboardInterrupt:
    print("User Interrupt, exit.")
    mainView.clean_up()
    ubooks.getBooksInfo().saveData()
    sys.exit(0)
