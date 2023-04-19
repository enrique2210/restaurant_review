from flask import request
from flask_login import current_user
from flask_restx import Resource, fields, Namespace

from models.cuisine_type import CuisineTypeModel
from models.restaurant import RestaurantModel
from models.utils import is_admin, is_owner
from schemas.restaurant import RestaurantSchema

RESTAURANT_NOT_FOUND = "Restaurant not found."
RESTAURANT_ALREADY_EXISTS = "Restaurant '{}' Already exists."

restaurant_ns = Namespace("restaurant", description="Restaurant related operations")
restaurants_ns = Namespace("restaurants", description="Restaurants related operations")

restaurant_schema = RestaurantSchema()
restaurant_list_schema = RestaurantSchema(many=True)

restaurant = restaurants_ns.model(
    "Restaurant",
    {
        "name": fields.String("Name of the Restaurant"),
        "location": fields.String("Location of the Restaurant"),
        "cuisine_type_id": fields.Integer(0),
    },
)


class Restaurant(Resource):
    def get(self, id):
        restaurant_data = RestaurantModel.find_by_id(id)
        if restaurant_data:
            return restaurant_schema.dump(restaurant_data)
        return {"message": RESTAURANT_NOT_FOUND}, 404

    @is_admin
    def delete(self, id):
        restaurant_data = RestaurantModel.find_by_id(id)
        if restaurant_data:
            restaurant_data.delete_from_db()
            return {"message": "Restaurant Deleted successfully"}, 200
        return {"message": RESTAURANT_NOT_FOUND}, 404


class RestaurantList(Resource):
    @restaurants_ns.doc("Get all the Restaurants")
    def get(self, page):
        if page < 0:
            return {"error": "Page must be minimun 0"}, 401
        return restaurant_list_schema.dump(RestaurantModel.find_all(page)), 200


class RestaurantListByStar(Resource):
    @restaurants_ns.doc("Get all the Restaurants by Stars")
    def get(self, stars, page):
        if page < 0:
            return {"error": "Page must be minimun 0"}, 401
        if stars > 5:
            return {"error": "Stars must be between 0 and 5"}, 401
        return (
            restaurant_list_schema.dump(RestaurantModel.find_by_star(stars, page)),
            200,
        )


class RestaurantRegister(Resource):
    @restaurants_ns.expect(restaurant)
    @restaurants_ns.doc("Create a Restaurant")
    @is_owner
    def post(self):
        restaurant_json = request.get_json()
        try:
            if not CuisineTypeModel.find_by_id(restaurant_json["cuisine_type_id"]):
                return {"error": "No cuisine_type with that id"}, 400

            restaurant_json["user_id"] = current_user.id
            restaurant_data = restaurant_schema.load(restaurant_json)
            restaurant_data.save_to_db()
        except Exception as e:
            return {"error": e.args}, 400

        return restaurant_schema.dump(restaurant_data), 201
