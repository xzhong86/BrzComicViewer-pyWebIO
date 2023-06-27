import os
import pywebio
from pywebio.output import  *

from utils.books import BooksInfo

all_books = BooksInfo()
all_books.scanImageFolderInPath("./books")

def view():
    pywebio.session.set_env(output_max_width="80%")
    put_column([put_scope("head"), put_scope("main")],
               size="100px minmax={800px}")

    with use_scope("head"):
        put_row([
            put_button("Home", onclick=lambda: home_page(0)),
            #put_button("Download", onclick=self.dl_page),
            #put_text("Home"),
            put_text("Previous Book"),
            put_text("Next Book"),
            None
        ], size="2fr 3fr 3fr 5fr")

    home_page(0)

@use_scope("main", clear=True)
def home_page(page_index):
    books = all_books.books
    items = []
    for idx in range(page_index * 8, page_index * 8 + 8):
        if (idx >= len(books)):
            break
        book = books[idx]
        def view_act(b=book):
            view_page(b, 0)
        but = put_button(book.name, onclick=view_act)
        items += [ but ]
    put_column(items)

@use_scope("main", clear=True)
def view_page(book, index):
    if index < 0:
        index = 0
    if index >= len(book.images):
        index = len(book.images) - 3

    images = book.images[index : index+2]
    it_imgs = [put_image(img.read()) for img in images]
    it_imgs.insert(1, None)

    it_buts = [
        put_button("Previous Page", onclick=lambda: view_page(book, index - 2)),
        None,
        put_button("Next Page", onclick=lambda: view_page(book, index + 2)),
    ]
    put_column([ put_row(it_imgs, size="48% 4% 48%"),
                 put_row(it_buts, size="2fr 8fr 2fr") ],
               size="9fr 1fr")

