import datetime
from typing import List

from sqlalchemy import Integer, DateTime, String, Float

from db import db
from models.constants import PAGINATE_DEFAULT_RESULS


class RestaurantModel(db.Model):
    __tablename__ = "restaurants"
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(80), nullable=False, unique=False)
    location = db.Column(String(80), nullable=False)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    star_rating = db.Column(Float, nullable=False, default=0)
    reviews = db.relationship(
        "ReviewModel",
        lazy="dynamic",
        primaryjoin="RestaurantModel.id == ReviewModel.restaurant_id",
    )

    cuisine_type_id = db.Column(
        db.Integer, db.ForeignKey("cuisine_types.id"), nullable=False
    )
    cuisine_type = db.relationship(
        "CuisineTypeModel",
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(
        "UserModel",
    )

    def __init__(self, name, location, cuisine_type_id, user_id):
        self.name = name
        self.location = location
        self.cuisine_type_id = cuisine_type_id
        self.user_id = user_id
        self.star_rating = 0

    @classmethod
    def find_by_name(cls, name) -> "RestaurantModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id) -> "RestaurantModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls, page=0) -> List["RestaurantModel"]:
        if page == 0:
            search = cls.query.order_by(RestaurantModel.star_rating.desc()).all()
        else:
            search = cls.query.order_by(RestaurantModel.star_rating.desc()).paginate(
                page=page, per_page=PAGINATE_DEFAULT_RESULS
            )
        return search

    @classmethod
    def find_by_star(cls, star, page=0) -> List["RestaurantModel"]:
        if page == 0:
            search = (
                cls.query.filter(RestaurantModel.star_rating >= star)
                .order_by(RestaurantModel.star_rating.desc())
                .all()
            )
        else:
            search = (
                cls.query.filter(RestaurantModel.star_rating >= star)
                .order_by(RestaurantModel.star_rating.desc())
                .paginate(page=page, per_page=PAGINATE_DEFAULT_RESULS)
            )
        return search

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
