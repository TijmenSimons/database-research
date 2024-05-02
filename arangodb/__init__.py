import pyArango
import pyArango.connection
import pyArango.database


class ArangoDB:
    conn: pyArango.connection.Connection
    db: pyArango.database.Database

    def __init__(cls, name: str = "test") -> None:
        cls.conn, cls.db, cls.col = ArangoDB.get_database(name)

    @staticmethod
    def get_database(name):
        conn = pyArango.connection.Connection(username="root", password="root")

        try:
            db = conn[name]
        except KeyError:
            db = conn.createDatabase(name=name)

        try:
            col = db["body"]
        except KeyError:
            col = db.createCollection(name="body")

        return conn, db, col

    def insert(cls, items):
        ids = []
        for item in items:
            doc = cls.col.createDocument()
            doc['d'] = item
            doc.save()
            ids.append(doc._key)
        return ids

    def retrieve(cls):
        records = []
        for key in cls.db.scan_iter():
            value = cls.db.get(key)
            records.append(value)

        return records

    def retrieve_by_id(cls, item_id):
        return cls.col[item_id]


__all__ = [
    "Arango",
]
