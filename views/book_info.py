
from pywebio.pin import  *
from pywebio.output import  *
from functools import partial

def put_score_radio(name, max_score, cur_score):
    items = [ dict(label=str(n), value=n, selected=(n == cur_score))
              for n in range(1, max_score+1) ]
    return put_radio("book_score_" + name, items, inline=True)

def update_info(book):
    for item in ["like", "story", "style", "quality"]:
        value = pin["book_score_" + item]
        setattr(book, item, value)
    close_popup()

def show_info(book):
    info_table = put_table([
        ["Attr",   "Description"],
        ["title:", book.title],
        ["url:",   book.url],
        ["tags:",  ", ".join(book.tags)],
        ["like:",  put_score_radio("like", 5,  book.like) ],
        ["story:", put_score_radio("story", 5, book.story) ],
        ["style:", put_score_radio("style", 5, book.style) ],
        ["quality:", put_score_radio("quality", 5, book.quality)],
        ["info:",  f"like {book.like}, view {book.view}" ],
        ["other:", f"{book.dir_name}, images {len(book.images)}"]
    ])
    popup("Book Information:",
          [
              info_table,
              put_button("Update", onclick=partial(update_info, book))
          ],
          size="normal")

