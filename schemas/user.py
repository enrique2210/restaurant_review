from marshmallow import fields

from ma import ma
from models.constants import Role
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    role = fields.Enum(Role, by_value=False)

    class Meta:
        model = UserModel
        load_instance = True
        include_fk = True
