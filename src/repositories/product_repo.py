from sqlalchemy.orm import Session
from src.database.models import Product
from src.database.session import get_db


class DbWorker:
    def __init__(self, db: get_db):
        self.db = db

    def get_by_sid(self, sid:int):
        return self.db.query(Product).filter(Product.id == sid).first()


