import datetime
from typing import List

from sqlalchemy import Integer, DateTime, String

from db import db
from models.constants import PAGINATE_DEFAULT_RESULS


class CuisineTypeModel(db.Model):
    __tablename__ = "cuisine_types"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(100), unique=True)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, name):
        self.name = name

    @classmethod
    def find_by_id(cls, _id) -> "CuisineTypeModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls, page=0) -> List["CuisineTypeModel"]:
        if page == 0:
            search = cls.query.all()
        else:
            search = cls.query.paginate(page=page, per_page=PAGINATE_DEFAULT_RESULS)
        return search

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
