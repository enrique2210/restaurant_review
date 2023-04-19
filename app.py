import os

from flask import Flask, Blueprint, jsonify
from flask_login import login_user, logout_user, current_user
from flask_restx import Api, Resource, fields
from marshmallow import ValidationError

from db import db
from login_manager import login_manager
from ma import ma
from models.user import UserModel
from resources.cuisine_type import (
    CuisineType,
    CuisineTypeList,
    cuisine_type_ns,
    cuisine_types_ns,
    CuisineTypeRegister,
)
from resources.restaurant import (
    Restaurant,
    RestaurantList,
    RestaurantRegister,
    restaurant_ns,
    restaurants_ns,
    RestaurantListByStar,
)
from resources.review import Review, ReviewList, reviews_ns, review_ns, ReviewRegister
from resources.user import User, UserList, users_ns, user_ns, UserRegister
from schemas.user import UserSchema

app = Flask(__name__)
bluePrint = Blueprint("api", __name__, url_prefix="/api")
api = Api(bluePrint, doc="/doc", title="Restaurant Review APP")

app.register_blueprint(bluePrint)

environment_configuration = os.environ["CONFIGURATION_SETUP"]
app.config.from_object(environment_configuration)
print(f"Environment: {app.config['ENV']}")

api.add_namespace(user_ns)
api.add_namespace(users_ns)

api.add_namespace(cuisine_type_ns)
api.add_namespace(cuisine_types_ns)

api.add_namespace(restaurant_ns)
api.add_namespace(restaurants_ns)

api.add_namespace(review_ns)
api.add_namespace(reviews_ns)

db.init_app(app)
ma.init_app(app)
login_manager.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


@api.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


user_ns.add_resource(User, "/<int:id>")
users_ns.add_resource(UserList, "/<int:page>")
users_ns.add_resource(UserRegister, "")

cuisine_type_ns.add_resource(CuisineType, "/<int:id>")
cuisine_types_ns.add_resource(CuisineTypeList, "/<int:page>")
cuisine_types_ns.add_resource(CuisineTypeRegister, "")

restaurant_ns.add_resource(Restaurant, "/<int:id>")
restaurants_ns.add_resource(RestaurantList, "/<int:page>")
restaurants_ns.add_resource(RestaurantListByStar, "/<int:stars>/<int:page>")
restaurants_ns.add_resource(RestaurantRegister, "")

review_ns.add_resource(Review, "/<int:id>")
reviews_ns.add_resource(ReviewList, "/<int:page>")
reviews_ns.add_resource(ReviewRegister, "")

login_fields = api.model(
    "Login",
    {
        "username": fields.String,
        "password": fields.String,
    },
)


@api.route("/login", endpoint="login")
class Login(Resource):
    @api.expect(login_fields)
    def post(self):
        user = UserModel.query.filter_by(username=api.payload["username"]).first()
        if not user or not user.verify_password(api.payload["password"]):
            return {"message": "Error in username or password"}, 400
        login_user(user, force=True)
        return {"message": f"Login Sucess, welcome {user.username}"}, 200


@api.route("/current-user", endpoint="current-user")
class CurrentUser(Resource):
    def get(self):
        if hasattr(current_user, "id"):
            return UserSchema().dump(UserModel.find_by_id(current_user.id))
        return {}


@api.route("/logout", endpoint="logout")
class Logout(Resource):
    def get(self):
        logout_user()
        return {"message": f"Log out Sucess"}, 200


if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
