import datetime

from flask import request
from flask_login import current_user
from flask_restx import Resource, fields, Namespace

from models.restaurant import RestaurantModel
from models.review import ReviewModel
from models.utils import is_admin, is_client
from schemas.review import ReviewSchema

REVIEW_NOT_FOUND = "Review not found."

review_ns = Namespace("review", description="Review related operations")
reviews_ns = Namespace("reviews", description="Reviews related operations")

review_schema = ReviewSchema()
review_list_schema = ReviewSchema(many=True)

# Model required by flask_restplus for expect
review = reviews_ns.model(
    "Review",
    {
        "restaurant_id": fields.Integer,
        "star": fields.Integer(5, min=1, max=5),
        "comment": fields.String(255),
        "date_visit": fields.Date(
            dt_format="mm-dd-YYYY", max=datetime.datetime.utcnow()
        ),
    },
)


class Review(Resource):
    def get(self, id):
        review_data = ReviewModel.find_by_id(id)
        if review_data:
            return review_schema.dump(review_data)
        return {"message": REVIEW_NOT_FOUND}, 404

    @is_admin
    def delete(self, id):
        review_data = ReviewModel.find_by_id(id)
        if review_data:
            review_data.delete_from_db()
            return {"message": "Review Deleted successfully"}, 200
        return {"message": REVIEW_NOT_FOUND}, 404


class ReviewList(Resource):
    @reviews_ns.doc("Get all the Reviews")
    def get(self, page):
        return review_list_schema.dump(ReviewModel.find_all(page)), 200


class ReviewRegister(Resource):
    @reviews_ns.expect(review)
    @reviews_ns.doc("Create an Review")
    @is_client
    def post(self):
        review_json = request.get_json()
        review_json["user_id"] = current_user.id
        review_data = review_schema.load(review_json)
        try:
            if not RestaurantModel.find_by_id(review_json["restaurant_id"]):
                return {"error": "No restaurant with that id"}, 400
            if ReviewModel.find_by_restaurant_and_user(
                review_json["restaurant_id"], current_user.id
            ):
                return {"error": "Already reviewed that restaurant"}, 400
            review_data.save_to_db()
            calculate_star_rating(review_json["restaurant_id"])

        except Exception as e:
            return {"error": e.args}, 400

        return review_schema.dump(review_data), 201


def calculate_star_rating(restaurant_id):
    restaurant = RestaurantModel.find_by_id(restaurant_id)
    reviews = ReviewModel.find_by_restaurant(restaurant_id)
    total = sum(_review.star for _review in reviews)
    avg = round(total / len(reviews), 2)
    restaurant.star_rating = avg
    restaurant.save_to_db()
