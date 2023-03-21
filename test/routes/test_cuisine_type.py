from models.cuisine_type import CuisineTypeModel
from schemas.cuisine_type import CuisineTypeSchema

test_schema = CuisineTypeSchema()


def test_create():
    obj = create_test()
    assert isinstance(obj, CuisineTypeModel)


def test_error_create():
    data = {
        "not_name": "test",
    }
    obj = create_test(data)
    assert obj is None


def create_test(data: object = None):
    try:
        if data is None:
            data = {
                "name": "test",
            }
        test_data = test_schema.load(data)
        return test_data
    except:
        return None
