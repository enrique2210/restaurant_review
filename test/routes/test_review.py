import datetime

from models.review import ReviewModel
from schemas.review import ReviewSchema
from test.routes.test_cuisine_type import create_test as cuisine_type_create_test
from test.routes.test_restaurant import create_test as restaurant_create_test
from test.routes.test_user import create_test as user_create_test

test_schema = ReviewSchema()


def test_create():
    user_obj = user_create_test()
    cuisine_type_obj = cuisine_type_create_test()
    # Assign id as it was created from "DB"
    user_obj.id = 1
    cuisine_type_obj.id = 1
    restaurant_obj = restaurant_create_test(
        user=user_obj, cuisine_type=cuisine_type_obj
    )
    # Assign id as it was created from "DB"
    restaurant_obj.id = 1
    obj = create_test(user=user_obj, restaurant=restaurant_obj)
    assert isinstance(obj, ReviewModel)


def test_error_create():
    data = {
        "date_visit": datetime.datetime.utcnow().date().strftime("%Y-%m-%d"),
        "comment": "test",
        "star": 5,
        "restaurant_id": None,
        "user_id": None,
    }
    obj = create_test(None, None, data)
    assert obj is None


def create_test(user, restaurant, data: object = None):
    try:
        if data is None:
            data = {
                "date_visit": datetime.datetime.utcnow().date().strftime("%Y-%m-%d"),
                "comment": "test",
                "star": 5,
                "restaurant_id": restaurant.id,
                "user_id": user.id,
            }
        test_data = test_schema.load(data)
        return test_data
    except Exception as e:
        return None
