import datetime
from typing import List

from sqlalchemy import Integer, SmallInteger, DateTime, Date, String

from db import db
from models.constants import PAGINATE_DEFAULT_RESULS


class ReviewModel(db.Model):
    __tablename__ = "reviews"

    id = db.Column(Integer, primary_key=True)
    star = db.Column(SmallInteger, nullable=False)
    comment = db.Column(String, nullable=False)
    date_visit = db.Column(Date, nullable=False)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    user_id = db.Column(Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(
        "UserModel",
    )
    restaurant_id = db.Column(Integer, db.ForeignKey("restaurants.id"), nullable=False)

    def __init__(self, star, comment, restaurant_id, user_id, date_visit):
        self.restaurant_id = restaurant_id
        self.user_id = user_id
        self.star = star
        self.comment = comment
        self.date_visit = date_visit

    def __repr__(self):
        return "ReviewModel(star=%s, date_visit=%s)" % (self.star, self.date_visit)

    def json(self):
        return {"star": self.star, "date_visit": self.date_visit}

    @classmethod
    def find_by_id(cls, _id) -> "ReviewModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_restaurant_and_user(cls, _restaurant_id, _user_id) -> "ReviewModel":
        return cls.query.filter_by(
            restaurant_id=_restaurant_id, user_id=_user_id
        ).first()

    @classmethod
    def find_by_restaurant(cls, _restaurant_id, page=0) -> "ReviewModel":
        if page == 0:
            search = cls.query.filter_by(restaurant_id=_restaurant_id).all()
        else:
            search = cls.query.filter_by(restaurant_id=_restaurant_id).paginate(
                page=page, per_page=PAGINATE_DEFAULT_RESULS
            )
        return search

    @classmethod
    def find_all(cls, page=0) -> List["ReviewModel"]:
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
