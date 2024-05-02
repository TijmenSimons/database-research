import ast
import os
import zlib
from arangodb import ArangoDB
from utils import get_random_ltrs, get_records, time_it


rdb_path = os.path.join(os.getcwd(), 'data', 'dump.rdb')


@time_it
def get(N: int, **k):
    print("[Arango]: Starting")
    temp_db = get_random_ltrs(12)
    arango = ArangoDB(temp_db)

    records = get_records(N)
    records = [zlib.compress(str(r).encode('utf-8')) for r in records]

    print(f"[Arango]: Creating {len(records)} records")
    all_ids = arango.insert(records)
    print("[Arango]: Created")

    info = arango.col.figures()["figures"]
    size = info["documentsSize"] + info["indexes"]["size"]

    return size, all_ids, temp_db


@time_it
def load(db_name: int, ids: list):
    print(f"[Arango]: Reading {len(ids)} items.")
    arangodb = ArangoDB(db_name)

    all_items = []

    for item_id in ids:
        record = arangodb.retrieve_by_id(item_id)
        data = ast.literal_eval(record["d"])

        item = zlib.decompress(data).decode('utf-8')
        all_items.append(item)


def clean(test, key):
    arango = ArangoDB(test["dbs"][key]["db"])
    arango.db.dropAllCollections()
    print(f"[Arango]: Deleted {test["dbs"][key]["db"]}")
