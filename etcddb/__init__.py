import etcd3
from utils import get_random_str


class EtcdDB:
    def __init__(cls, prefix: str = "/test") -> None:
        cls.db = EtcdDB.get_database()
        cls.prefix = str(prefix)

    @staticmethod
    def get_database():
        return etcd3.client(host='127.0.0.1', port=2379)

    def insert(cls, items):
        ids = []
        for item in items:
            new_id = get_random_str(16)
            cls.db.put(f'{cls.prefix}/{new_id}', item)
            ids.append(new_id)
        return ids

    def retrieve(cls):
        records = []
        keys = cls.db.get_prefix(cls.prefix)
        for key in keys:
            value = key[0].decode("utf-8")
            records.append(value)

        return records

    def retrieve_by_id(cls, item_id):
        return cls.db.get(f"{cls.prefix}/{item_id}")
    
    def reset(cls, all_ids):
        for key in all_ids:
            cls.db.delete(f'{cls.prefix}/{key}')



__all__ = [
    "Etcd",
]
