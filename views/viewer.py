
import pywebio
from pywebio.pin import  *
from pywebio.input import  *
from pywebio.output import  *
from pywebio.session import local as web_local

from functools import partial

from views.home import home_page, side_bar, show_book_info

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
        put_button("\u2139", onclick=lambda: show_book_info(book)),
        put_button("\u219e", onclick=lambda: toast("prev book")),
        put_button("\u21a0", onclick=lambda: toast("next book")),
        put_button("\u21E4", onclick=lambda: view_page(book, 0), disabled=(index == 0)),  # goto head
        put_button("\u2190", onclick=lambda: view_page(book, index - 2), disabled=no_prev_page),
        put_button("\u2192", onclick=lambda: view_page(book, index + 2), disabled=no_next_page),
    ]
    side_bar(buttons)

