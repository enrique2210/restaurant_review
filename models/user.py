import datetime
from typing import List

from sqlalchemy import Integer, DateTime, String, Enum
from werkzeug.security import check_password_hash

from db import db
from login_manager import login_manager
from models.constants import Role, PAGINATE_DEFAULT_RESULS


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(32), index=True, unique=True)
    password = db.Column(String(255))
    role = db.Column(Enum(Role))
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    @classmethod
    def find_by_id(cls, _id) -> "UserModel":
        return cls.query.with_entities(
            UserModel.id,
            UserModel.username,
            UserModel.role,
            UserModel.created_at,
        ).filter_by(id=_id).first()

    @classmethod
    def find_all(cls, page=0) -> List["UserModel"]:
        if page == 0:
            search = cls.query.with_entities(
                UserModel.id,
                UserModel.username,
                UserModel.role,
                UserModel.created_at,
            ).all()
        else:
            search = cls.query.with_entities(
                UserModel.id,
                UserModel.username,
                UserModel.role,
                UserModel.created_at,
            ).paginate(page=page, per_page=PAGINATE_DEFAULT_RESULS)
        return search

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.id


@login_manager.user_loader
def user_loader(id):
    return UserModel.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = UserModel.query.filter_by(username=username).first()
    return user if user else None
