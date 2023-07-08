import os
import pywebio
from pywebio.pin import  *
from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local

from functools import partial
from more_itertools import batched

from utils import books as ubooks

glb_bsi = None

def view():
    global glb_bsi
    glb_bsi = ubooks.getBooksInfo()
    pywebio.session.set_env(output_max_width="90%")

    put_row([put_scope("main"), None, put_scope("sidebar")],
               size="13fr 0.3fr 0.8fr")
    #pywebio.session.defer_call(clean_up)

    web_local.home_page_index = glb_bsi.getHomeIndex() or 0
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

    books = glb_bsi.books
    books_num = len(books)
    last_idx  = books_num - 1

    index = 0 if index < 0 else index
    index = last_idx if index > last_idx else index
    index = index - index % HOME_BPP  # align index

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
    glb_bsi.setHomeIndex(index, BPP)

    show_sidebar(index)

def show_sidebar(index):
    BPP     = HOME_BPP
    nr_books = len(glb_bsi.books)
    no_prev = index - BPP < 0
    no_next = index + BPP >= nr_books
    buttons = [
        put_text(str(index) + "/" + str(nr_books)),
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
    if (index >= len(glb_bsi.books)):
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
    index = index + HOME_BPP if index < len(glb_bsi.books) else index
    home_page(index)

def book_brief(book):
    from views.viewer import view_book
    from views.book_info import show_info
    title = book.title[0:50] + "..."
    brief = put_column([
        put_text(title),
        put_row([
            put_text(f"{len(book.images)}P, like: {book.like}, view: {book.view}"),
            put_button("\u2139", onclick=partial(show_info, book), small=True),
            put_button("Open", onclick=partial(view_book, book), small=True, outline=True),
        ], size="8fr 1fr 1fr"),
        put_row([
            put_image(img.read(thumb=True), height="240px") for img in book.images[0:2]
        ])
    ], size="0.5fr 0.3fr 3fr")
    style(brief, 'border: 1px solid; border-radius: 8px; padding: 5px; margin: 4px')
    return brief

