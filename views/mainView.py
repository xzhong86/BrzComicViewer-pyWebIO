import os
import pywebio
from pywebio.output import  *

from functools import partial
from more_itertools import batched

from utils.books import BooksInfo

all_books = BooksInfo()
all_books.scanImageFolderInPath("./books")

def view():
    pywebio.session.set_env(output_max_width="90%")
    #put_column([put_scope("head"), put_scope("main")],
    #           size="100px minmax={800px}")
    # 
    #with use_scope("head"):
    #    put_row([
    #        put_button("Home", onclick=lambda: home_page(0)),
    #        #put_button("Download", onclick=self.dl_page),
    #        #put_text("Home"),
    #        put_text("Previous Book"),
    #        put_text("Next Book"),
    #        None
    #    ], size="2fr 3fr 3fr 5fr")
    put_row([put_scope("main"), None, put_scope("sidebar")],
               size="13fr 0.3fr 1fr")

    home_page(0)

@use_scope("main", clear=True)
def home_page(page_index):
    books = all_books.books
    NROW, BPR = 2, 3  # row number, books per row
    BPP = BPR * NROW  # books per page
    contents = []
    for idx in range(page_index * BPP, page_index * BPP + BPP):
        if (idx >= len(books)):
            break
        book = books[idx]
        contents.append(book_brief(book))

    put_column([
        put_row(r) for r in batched(contents, BPR)
    ])

    index = page_index
    no_prev = index - 1 < 0
    no_next = index + 1 >= len(books) / BPP
    buttons = [
        put_text(str(index) + "/" + str(int(len(books) / BPP))),
        #put_button("\u2302", onclick=lambda: home_page(0)),
        put_button("\u21E4", onclick=lambda: home_page(0), disabled=(index == 0)),  # goto head
        put_button("\u2190", onclick=lambda: home_page(index - 1), disabled=no_prev),
        put_button("\u2192", onclick=lambda: home_page(index + 1), disabled=no_next),
    ]
    side_bar(buttons)

def list_join(lst, item):
    newlst = []
    for e in lst:
        newlst += [ e, item ]
    newlst.pop()
    return newlst

def book_brief(book):
    brief = put_column([
        put_row([
            put_text(book.name + "\n" + str(len(book.images)) + "P"),
            put_button("Go", onclick=partial(view_page, book, 0)),
        ], size="85% 15%"),
        put_row([
            put_image(img.read(), height="240px") for img in book.images[0:2]
        ])
    ], size="1fr 3fr")
    style(brief, 'border: 1px solid; border-radius: 8px; padding: 5px; margin: 4px')
    return brief

@use_scope("sidebar", clear=True)
def side_bar(buttons):
    if (not buttons or len(buttons) == 0):
        pass
    put_column(buttons)        

@use_scope("main", clear=True)
def view_page(book, index):
    if index < 0:
        index = 0
    if index >= len(book.images):
        index = len(book.images)

    images = book.images[index : index+2]
    it_imgs = [put_image(img.read()) for img in images]
    it_imgs.insert(1, None)

    put_row(it_imgs, size="48% 4% 48%")

    no_prev_page = index - 1 < 0
    no_next_page = index + 2 >= len(book.images)
    buttons = [
        put_text(str(index) + "/" + str(len(book.images))),
        put_button("\u2302", onclick=lambda: home_page(0)),
        put_button("\u219e", onclick=lambda: toast("prev book")),
        put_button("\u21a0", onclick=lambda: toast("next book")),
        put_button("\u21E4", onclick=lambda: view_page(book, 0), disabled=(index == 0)),  # goto head
        put_button("\u2190", onclick=lambda: view_page(book, index - 2), disabled=no_prev_page),
        put_button("\u2192", onclick=lambda: view_page(book, index + 2), disabled=no_next_page),
    ]
    side_bar(buttons)
