from ma import ma
from models.cuisine_type import CuisineTypeModel


class CuisineTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CuisineTypeModel
        load_instance = True

    # restaurants = ma.Nested(RestaurantSchema, many=True)