from marshmallow import fields

from ma import ma
from models.review import ReviewModel
from models.user import UserModel


class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ReviewModel
        load_instance = True
        include_fk = True

    user = fields.Method("get_user")

    @staticmethod
    def get_user(obj):
        user = UserModel.find_by_id(obj.user_id)
        return {"id": user.id, "username": user.username}
