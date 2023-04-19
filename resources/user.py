from flask import request
from flask_restx import Resource, fields, Namespace
from werkzeug.security import generate_password_hash

from db import db
from models.constants import Role
from models.user import UserModel
from models.utils import is_admin, is_self_user
from schemas.user import UserSchema

USER_NOT_FOUND = "User not found."

user_ns = Namespace("user", description="User related operations")
users_ns = Namespace("users", description="Users related operations")

user_schema = UserSchema()
user_list_schema = UserSchema(many=True)

user = users_ns.model(
    "User",
    {
        "username": fields.String("Username of the User"),
        "password": fields.String("Password of the User"),
        "role": fields.Integer(2, min=1),
    },
)

user_update = users_ns.model(
    "UserUpdate",
    {
        "username": fields.String("Username of the User"),
        "password": fields.String("Password of the User"),
    },
)


class User(Resource):
    def get(self, id):
        user_data = UserModel.find_by_id(id)
        if user_data:
            return user_schema.dump(user_data), 200
        return {"message": USER_NOT_FOUND}, 404

    @is_admin
    def delete(self, id):
        user_data = db.session.query(UserModel).filter(UserModel.id == id).first()
        if user_data:
            user_data.delete_from_db()
            return {"message": "User Deleted successfully"}, 200
        return {"message": USER_NOT_FOUND}, 404

    @user_ns.expect(user_update)
    @is_self_user
    def put(self, id):
        user_data = db.session.query(UserModel).filter(UserModel.id == id).first()
        user_json = request.get_json()

        if user_data:
            user_data.username = user_json["username"]
            user_json["password"] = generate_password_hash(user_json["password"])
        else:
            user_json["role"] = Role(user_json["role"]).name
            user_data = user_schema.load(user_json)

        try:
            user_data.save_to_db()
        except Exception as e:
            return {"error": e.args}, 400
        return user_schema.dump(UserModel.find_by_id(id)), 200


class UserList(Resource):
    @users_ns.doc("Get all the Users")
    def get(self, page):
        return user_list_schema.dump(UserModel.find_all(page)), 200


class UserRegister(Resource):
    @users_ns.expect(user)
    @users_ns.doc("Create an User")
    def post(self):
        user_json = request.get_json()

        try:
            user_json["password"] = generate_password_hash(user_json["password"])
            user_json["role"] = Role(user_json["role"]).name
            user_data = user_schema.load(user_json)
            user_data.save_to_db()
        except Exception as e:
            return {"error": e.args}, 400

        return user_schema.dump(UserModel.find_by_id(user_data.id)), 201
