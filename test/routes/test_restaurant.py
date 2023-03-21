from models.restaurant import RestaurantModel
from schemas.restaurant import RestaurantSchema
from test.routes.test_cuisine_type import create_test as cuisine_type_create_test
from test.routes.test_user import create_test as user_create_test

test_schema = RestaurantSchema()


def test_create():
    user_obj = user_create_test()
    cuisine_type_obj = cuisine_type_create_test()
    # Assign id as it was created from "DB"
    user_obj.id = 1
    cuisine_type_obj.id = 1
    obj = create_test(user=user_obj, cuisine_type=cuisine_type_obj)
    assert isinstance(obj, RestaurantModel)


def test_error_create():
    data = {
        "name": "test",
        "location": "test",
        "cuisine_type_id": None,
        "user_id": None,
    }
    obj = create_test(None, None, data)
    assert obj is None


def create_test(user, cuisine_type, data: object = None):
    try:
        if data is None:
            data = {
                "name": "test",
                "location": "test",
                "cuisine_type_id": cuisine_type.id,
                "user_id": user.id,
            }
        test_data = test_schema.load(data)
        return test_data
    except:
        return None
