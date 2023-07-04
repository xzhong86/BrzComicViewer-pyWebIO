import os
import pywebio
from pywebio.pin import  *
from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local

from functools import partial
from more_itertools import batched

from utils.books import BooksInfo


all_books = BooksInfo()
#all_books.scanImageFolderInPath("./books")
all_books.scanImagePackInPath("./packs-cn")

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
               size="13fr 0.3fr 0.8fr")

    web_local.home_page_index = 0
    web_local.view_page_index = 0
    web_local.view_book_index = 0
    home_page()

@use_scope("sidebar", clear=True)
def side_bar(items):
    if (not items or len(items) == 0):
        pass
    put_column(items)        


HOME_NROW = 2   # rows in home page
HOME_BPR  = 3   # books per row
HOME_BPP  = HOME_NROW * HOME_BPR # books per page

@use_scope("main", clear=True)
def home_page(index = None):
    if (index == None):
        index = web_local.home_page_index
    books = all_books.books
    BPP = HOME_BPP
    contents = []
    for idx in range(index, index + BPP):
        if (idx >= len(books)):
            break
        book = books[idx]
        contents.append(book_brief(book))

    put_column([
        put_row(r) for r in batched(contents, HOME_BPR)
    ])
    web_local.home_page_index = index

    #index = page_index
    no_prev = index - BPP < 0
    no_next = index + BPP >= len(books)
    buttons = [
        put_text(str(index) + "/" + str(len(books))),
        put_input("goto", type=NUMBER, value=index),
        put_button("Go", onclick=home_page_goto),
        None,
        #put_button("\u2302", onclick=lambda: home_page(0)),
        put_button("\u21E4", onclick=lambda: home_page(0), disabled=(index == 0)),  # goto head
        put_button("\u2190", onclick=home_page_prev, disabled=no_prev),
        put_button("\u2192", onclick=home_page_next, disabled=no_next),
    ]
    side_bar(buttons)

def home_page_goto():
    index = pin.goto
    index = index if index > 0 else 0
    if (index >= len(all_books.books)):
        toast("book index over max!")
    else:
        index = index - index % HOME_BPP
        home_page(index)

def home_page_prev():
    index = web_local.home_page_index - HOME_BPP
    index = index if index > 0 else 0
    home_page(index)

def home_page_next():
    index = web_local.home_page_index
    index = index + HOME_BPP if index < len(all_books.books) else index
    home_page(index)


def list_join(lst, item):
    newlst = []
    for e in lst:
        newlst += [ e, item ]
    newlst.pop()
    return newlst

def book_brief(book):
    title = book.title[0:30] + "..."
    brief = put_column([
        put_row([
            put_text(title + "\n" + str(len(book.images)) + "P"),
            put_button("Go", onclick=partial(view_page, book, 0), link_style=True),
        ], size="85% 15%"),
        put_row([
            put_image(img.read(), height="240px") for img in book.images[0:2]
        ])
    ], size="1fr 3fr")
    style(brief, 'border: 1px solid; border-radius: 8px; padding: 5px; margin: 4px')
    return brief

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
        put_button("\u2302", onclick=lambda: home_page(None)),
        put_button("\u2139", onclick=lambda: view_book_info(book)),
        put_button("\u219e", onclick=lambda: toast("prev book")),
        put_button("\u21a0", onclick=lambda: toast("next book")),
        put_button("\u21E4", onclick=lambda: view_page(book, 0), disabled=(index == 0)),  # goto head
        put_button("\u2190", onclick=lambda: view_page(book, index - 2), disabled=no_prev_page),
        put_button("\u2192", onclick=lambda: view_page(book, index + 2), disabled=no_next_page),
    ]
    side_bar(buttons)

def view_book_info(book):
    info = put_table([
        ["Attr",   "Description"],
        ["title:", book.title],
        ["url:",   book.url],
        ["tags:",  ", ".join(book.tags)],
        ["dir:",   book.name],
        ["other:", str(len(book.images)) + " images"]
    ])
    popup("Book Information:",
          info,
          size="normal")

