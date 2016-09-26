from peewee import *
import sqlite3
from app import db


class BaseModel(Model):

    class Meta:
        database = db


class Book(BaseModel):
    BOOKLINE_LINK_HEAD = "http://bookline.hu/search/search.action?inner=true&searchfield="
    BOOKLINE_LINK_TAIL = "&tab=bookline.hu%2Fbook"
    ADMIN_LINK_HEAD = "http://admin.bookline.hu/product/editBookProduct!input.action?apid=10:"

    status = CharField()
    description_id = CharField()
    book_id = CharField()
    author = CharField()
    title = CharField()
    publication_year = CharField()
    publisher = CharField()
    barcode = CharField()
    storage_place = CharField()
    picture_url = CharField()
    price = CharField()
    uploaded = DateTimeField()
    sold_in_shop = DateTimeField()
    shop = CharField()
    weight = FloatField()
    number_of_pages = CharField()
    cover = CharField()
    quality = CharField()
    moreinfo = TextField()
    uploader = CharField()
    category = CharField()
    annotation = TextField()
    publication_id = CharField()
    isbn = CharField()

    admin_link = CharField(null=True)
    bookline_link = CharField(null=True)

    def create_admin_link(self):
        return str(self.ADMIN_LINK_HEAD + self.book_id)

    def create_bookline_link(self):
        inner_part = str((self.author + "+" + self.title).replace(" ", "+"))
        return self.BOOKLINE_LINK_HEAD + inner_part + self.BOOKLINE_LINK_TAIL
