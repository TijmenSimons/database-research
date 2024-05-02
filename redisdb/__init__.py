import redis

from utils import get_random_str


class RedisDB:
    def __init__(cls, dbnr=0) -> None:
        cls.db = RedisDB.get_database()

    @staticmethod
    def get_database():
        r = redis.Redis(host='localhost', port=6379)

        return r

    def insert(cls, items):
        ids = []
        for item in items:
            new_id = get_random_str(16)
            cls.db.set(new_id, item)
            ids.append(new_id)
        return ids

    def retrieve(cls):
        records = []
        for key in cls.db.scan_iter():
            value = cls.db.get(key)
            records.append(value)

        return records

    def retrieve_by_id(cls, item_id):
        return cls.db.get(item_id)


__all__ = [
    "Redis",
]
