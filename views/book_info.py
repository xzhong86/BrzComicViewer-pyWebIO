
import re
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
    book.desc = pin.book_desc
    re_spc = re.compile(r'\s+')
    re_sep = re.compile(r'\s*,\s*')
    tags_str = re_spc.sub(' ', pin.book_tags)
    tags     = re_sep.split(tags_str)
    book.tags = tags
    book.dataUpdated()
    close_popup()

def show_info(book):
    tags_str = ", ".join(book.tags)
    info_table = put_table([
        ["Attr",   "Description"],
        ["title:", book.title],
        ["url:",   book.url],
        ["desc:",  put_input("book_desc", value=book.desc)],
        ["tags:",  put_input("book_tags", value=tags_str)],
        ["like:",  put_score_radio("like", 5,  book.like) ],
        ["story:", put_score_radio("story", 5, book.story) ],
        ["style:", put_score_radio("style", 5, book.style) ],
        ["quality:", put_score_radio("quality", 5, book.quality)],
        ["info:",  f"view: {book.view}, {book.image_num} pages, {book.page_viewed} page viewed" ],
        ["other:", f"{book.dir_name}, {book.birth_time.isoformat()}"]
    ])
    popup("Book Information:",
          [
              info_table,
              put_button("Update", onclick=partial(update_info, book))
          ],
          size="large")

