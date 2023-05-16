import re
from config import Config
import sqlite3
from typing import Iterable
from mark import Mark

cfg = Config()
mark_cfg = Mark.load(cfg.mark_file)

# DATETIME(ZANNOTATIONCREATIONDATE + STRFTIME("%s", "2001-01-01"), "unixepoch") as created_date,

ANNOTATION_QUERY = f"""
select 
    ZANNOTATIONUUID as id,
    ZANNOTATIONSELECTEDTEXT as highlight, 
    ZANNOTATIONNOTE as note, 
    ZANNOTATIONCREATIONDATE as time_mark,
    ZANNOTATIONASSETID as book_id, 
    ZANNOTATIONLOCATION as location 
from 
    ZAEANNOTATION 
where 
    ZANNOTATIONSELECTEDTEXT is not null 
    and ZANNOTATIONDELETED = 0
    and ZANNOTATIONCREATIONDATE > {mark_cfg.get_time_mark()}
order by
    ZANNOTATIONCREATIONDATE desc
"""

BOOK_QUERY = """
select 
    ZASSETID as id, 
    ZAUTHOR as book_author, 
    ZTITLE as book_name 
from 
    ZBKLIBRARYASSET 
where 
    ZASSETID is not null
"""


def row_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def query_and_get_dict(db_path: str, sql: str) -> Iterable[dict]:
    connection = sqlite3.connect(db_path)
    connection.row_factory = row_factory
    for row in connection.execute(sql):
        yield row


def format_name(book):
    book['book_name'] = re.sub(r'[【（(][^)）\]】]*(?:[)）\]】])?', '', book['book_name'])
    book.pop('id')
    return book


def append_book_info(annotation, book):
    if book:
        annotation.update(book)
    pattern = re.compile(r"[\n]|[\n][Oo][\n]|[（(][nN][\n][)）]")
    annotation['highlight'] = re.sub(pattern, '', annotation.get('highlight'))
    return annotation


def update_time_mark(time_mark: str):
    mark_cfg.last_time_mark = mark_cfg.time_mark
    mark_cfg.time_mark = time_mark
    mark_cfg.save(cfg.mark_file)


def query():
    books_dict = {
        b['id']: format_name(b)
        for b in query_and_get_dict(cfg.book_sqlite_path, BOOK_QUERY)
    }

    annotations = [
        append_book_info(a, books_dict.get(a['book_id'])) for a in
        query_and_get_dict(cfg.annotation_sqlite_path, ANNOTATION_QUERY)
    ]

    update_time_mark(annotations[0].get('time_mark'))

    # 替换简短的 id 节省 tokens
    for idx, item in enumerate(annotations):
        item['id'] = "i" + str(idx)

    return annotations