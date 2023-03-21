from werkzeug.security import generate_password_hash

from models.constants import Role
from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


def test_create():
    obj = create_test()
    assert isinstance(obj, UserModel)


def test_error_create():
    obj = create_test(10)
    assert obj is None


def create_test(data: object = None):
    try:
        if data is None or isinstance(data, int):
            data = {
                "username": "test",
                "role": data if isinstance(data, int) else Role.CLIENT,
                "password": "test"
            }
        data['password'] = generate_password_hash(data['password'])
        data['role'] = Role(data['role']).name
        test_data = user_schema.load(data)
        return test_data
    except:
        return None
