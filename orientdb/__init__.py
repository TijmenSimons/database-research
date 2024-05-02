import pyorient


class OrientDB:
    def __init__(cls, dbname: str = "test") -> None:
        cls.client, cls.db = OrientDB.get_database(dbname)

    @staticmethod
    def get_database(db_name):
        client = pyorient.OrientDB("localhost", 2424)
        client.connect("root", "rootpwd")

        if not client.db_exists(db_name):
            client.db_create(db_name)

        db = client.db_open(db_name, "root", "rootpwd")

        try:
            client.command("CREATE CLASS body")
            client.command("CREATE PROPERTY body.data STRING")

        except Exception:
            ...

        return client, db

    def insert(cls, items):
        ids = []
        for item in items:
            command = "INSERT INTO body SET "
            command += "data = '{}'".format(item)
            inserted_record = cls.client.command(command)
            ids.append(inserted_record[0]._rid)
        return ids

    def retrieve(cls):
        query = "SELECT FROM body"
        return cls.client.query(query)

    def retrieve_by_id(cls, item_id):
        query = "SELECT FROM body WHERE @rid = {}".format(item_id)
        result = cls.client.query(query)
        return result[0]
