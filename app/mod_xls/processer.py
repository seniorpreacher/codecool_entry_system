import xlrd
from xlrd.sheet import ctype_text
from peewee import *
from app import db
from app.mod_xls.models import Book, BaseModel


class FileProcesser():
    XLS_TO_MODEL = {
        "státusz": "status", "műleírás id": "description_id", "termék id": "book_id", "szerző": "author",
        "cím": "title", "kiadási év": "publication_year", "kiadó": "publisher", "vonalkód": "barcode",
        "tárolóhely": "storage_place", "kép": "picture_url", "egységár": "price",  "felvitel dátuma": "uploaded",
        "bolti eladás dátuma": "sold_in_shop", "bolt": "shop", "súly": "weight", "oldalszám": "number_of_pages",
        "kötés (extra)": "cover", "minőség": "quality", "moreinfo": "moreinfo", "feltöltő": "uploader",
        "kategória": "category", "annotáció": "annotation", "kiadás id": "publication_id", "isbn": "isbn"
    }

    def __init__(self, route):
        book = xlrd.open_workbook(route)
        sheet = book.sheet_by_index(0)

        self.dict_list = []
        for row in range(1, sheet.nrows):
            current_row = {}
            for column in range(sheet.ncols):
                current_row[self.XLS_TO_MODEL.get(sheet.cell(0, column).value)] = sheet.cell(row, column).value
            self.dict_list.append(current_row)

    def add_to_database(self):
        with db.atomic():
            Book.insert_many(self.dict_list).execute()

    def add_links_to_database(self):
        pass
