import aerospike

from utils import get_random_str


class AspikeDB:
    def __init__(cls, dbname="some_db", set_name="bodies1") -> None:
        cls.db = AspikeDB.get_database()
        cls.key = (dbname, set_name, get_random_str(16))

    @staticmethod
    def get_database():
        config = {"hosts": [("localhost", 3000)]}

        client = aerospike.client(config).connect()

        return client

    def insert(cls, items: list[dict]):
        ids = []
        for i in items:
            new_id = get_random_str(16)
            cls.db.put((cls.key[0], cls.key[1], new_id), i)
            ids.append(new_id)
        return ids

    def retrieve(cls):
        print("RETRIEVE START")
        print("RETRIEVE START")
        print("RETRIEVE START")
        records = []
        scan = cls.db.scan(cls.key[0], cls.key[1])
        scan.select()
        for key, metadata, record in scan.results():
            print(key, metadata, record)
            print()
            records.append(record)

        return records

    def retrieve_by_id(cls, item_id):
        (key, metadata, record) = cls.db.get((cls.key[0], cls.key[1], item_id))
        return record


__all__ = [
    "Aspike",
]
