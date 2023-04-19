from flask import request
from flask_restx import Resource, fields, Namespace

from db import db
from models.cuisine_type import CuisineTypeModel
from models.utils import is_admin
from schemas.cuisine_type import CuisineTypeSchema

CUISINE_TYPE_NOT_FOUND = "CuisineType not found."

cuisine_type_ns = Namespace(
    "cuisine_type", description="CuisineType related operations"
)
cuisine_types_ns = Namespace(
    "cuisine_types", description="CuisineTypes related operations"
)

cuisine_type_schema = CuisineTypeSchema()
cuisine_type_list_schema = CuisineTypeSchema(many=True)

cuisine_type = cuisine_types_ns.model(
    "CuisineType",
    {
        "name": fields.String("Name of the CuisineType"),
    },
)


class CuisineType(Resource):
    def get(self, id):
        cuisine_type_data = CuisineTypeModel.find_by_id(id)
        if cuisine_type_data:
            return cuisine_type_schema.dump(cuisine_type_data), 200
        return {"message": CUISINE_TYPE_NOT_FOUND}, 404

    @is_admin
    def delete(self, id):
        cuisine_type_data = (
            db.session.query(CuisineTypeModel).filter(CuisineTypeModel.id == id).first()
        )
        if cuisine_type_data:
            cuisine_type_data.delete_from_db()
            return {"message": "CuisineType Deleted successfully"}, 200
        return {"message": CUISINE_TYPE_NOT_FOUND}, 404

    @cuisine_type_ns.expect(cuisine_type)
    @is_admin
    def put(self, id):
        cuisine_type_data = (
            db.session.query(CuisineTypeModel).filter(CuisineTypeModel.id == id).first()
        )
        cuisine_type_json = request.get_json()

        if cuisine_type_data:
            cuisine_type_data.name = cuisine_type_json["name"]
        else:
            cuisine_type_data = cuisine_type_schema.load(cuisine_type_json)

        cuisine_type_data.save_to_db()
        return cuisine_type_schema.dump(CuisineTypeModel.find_by_id(id)), 200


class CuisineTypeList(Resource):
    @cuisine_types_ns.doc("Get all the CuisineTypes")
    def get(self, page):
        return cuisine_type_list_schema.dump(CuisineTypeModel.find_all(page)), 200


class CuisineTypeRegister(Resource):
    @cuisine_types_ns.expect(cuisine_type)
    @cuisine_types_ns.doc("Create an CuisineType")
    @is_admin
    def post(self):
        cuisine_type_json = request.get_json()

        try:
            cuisine_type_data = cuisine_type_schema.load(cuisine_type_json)
            cuisine_type_data.save_to_db()
        except Exception as e:
            return {"error": e.args}, 400

        return cuisine_type_schema.dump(cuisine_type_data), 201
