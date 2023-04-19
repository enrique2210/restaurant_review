from enum import IntEnum

PAGINATE_DEFAULT_RESULS = 10


class Role(IntEnum):
    OWNER = 1
    CLIENT = 2
    ADMIN = 0
