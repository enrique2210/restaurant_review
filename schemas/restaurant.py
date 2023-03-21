from marshmallow import fields

from ma import ma
from models.restaurant import RestaurantModel
from models.user import UserModel
from schemas.cuisine_type import CuisineTypeSchema
from schemas.review import ReviewSchema


class RestaurantSchema(ma.SQLAlchemyAutoSchema):
    reviews = ma.Nested(ReviewSchema, many=True)

    class Meta:
        model = RestaurantModel
        load_instance = True
        include_fk = True

    cuisine_type = ma.Nested(CuisineTypeSchema, many=False)
    user = fields.Method('get_user')

    @staticmethod
    def get_user(obj):
        user = UserModel.find_by_id(obj.user_id)
        return {
            "id": user.id,
            "username": user.username
        }
