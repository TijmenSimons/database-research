from pymongo import MongoClient

from mongodb.actions import MongoActions



class MongoDB:
    # db: Any
    # collection_name: Any

    def __init__(cls, dbname = "some_db", collection = "bodies1") -> None:
        cls.real_db = MongoDB.get_database()
        cls.db = cls.real_db[dbname]
        cls.collection_name = cls.db[collection]

    @staticmethod
    def get_database():
        CONNECTION_STRING = "mongodb://localhost:27017/"

        client: MongoClient = MongoClient(CONNECTION_STRING)

        return client

    def insert(cls, items: list[dict]):
        return cls.collection_name.insert_many(items)

    def retrieve(cls):
        return cls.collection_name.find()

    def retrieve_by_id(cls, item_id):
        return cls.collection_name.find({"_id": item_id})


__all__ = [
    "MongoActions",
    "MongoDB",
]
