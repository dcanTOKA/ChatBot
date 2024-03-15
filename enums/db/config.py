import enum
from decouple import config


class ConfigDB(enum.Enum):
    DB_USER = config('DB_USER')
    DB_PASSWORD = config('DB_PASSWORD')
    DB_HOST = config('DB_HOST')
    DB_PORT = str(config('DB_PORT'))
    DB_NAME = config('DB_NAME')
