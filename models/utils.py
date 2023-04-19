from flask_login import current_user

from models.constants import Role


def is_owner(func):
    def wrapper(*args, **kwargs):
        if hasattr(current_user, "id") and current_user.role in [
            Role.OWNER,
            Role.ADMIN,
        ]:
            return func(*args, **kwargs)
        return {}, 401

    return wrapper


def is_client(func):
    def wrapper(*args, **kwargs):
        if hasattr(current_user, "id") and current_user.role in [
            Role.CLIENT,
            Role.ADMIN,
        ]:
            return func(*args, **kwargs)
        return {}, 401

    return wrapper


def is_admin(func):
    def wrapper(*args, **kwargs):
        if hasattr(current_user, "id") and current_user.role == Role.ADMIN:
            return func(*args, **kwargs)
        return {}, 401

    return wrapper


def is_self_user(func):
    def wrapper(*args, **kwargs):
        if hasattr(current_user, "id") and current_user.role == Role.ADMIN:
            return func(*args, **kwargs)
        if hasattr(current_user, "username") and kwargs["id"] == current_user.id:
            return func(*args, **kwargs)
        return {}, 401

    return wrapper
