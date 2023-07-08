
from pywebio.pin import  *
from pywebio.output import  *
from functools import partial

def put_score_radio(name, max_score, cur_score):
    items = [ dict(label=str(n), value=n, selected=(n == cur_score))
              for n in range(1, max_score+1) ]
    return put_radio("book_score_" + name, items, inline=True)

def show_info(book):
    info = put_table([
        ["Attr",   "Description"],
        ["title:", book.title],
        ["url:",   book.url],
        ["tags:",  ", ".join(book.tags)],
        ["like:",  put_score_radio("like", 5, book.like)],
        ["story:", put_score_radio("story", 5, 3)],
        ["style:", put_score_radio("style", 5, 3)],
        ["quality:", put_score_radio("quality", 5, 3)],
        ["info:",  f"like {book.like}, view {book.view}" ],
        ["other:", f"{book.dir_name}, images {len(book.images)}"]
    ])
    popup("Book Information:",
          info,
          size="normal")

