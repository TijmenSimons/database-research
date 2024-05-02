import base64
import os
import zlib
from orientdb import OrientDB
from utils import get_random_ltrs, get_records, time_it


rdb_path = os.path.join(os.getcwd(), 'data', 'dump.rdb')


@time_it
def get(N: int, **k):
    print("[Orient]: Starting")
    temp_db = get_random_ltrs(12)
    orient = OrientDB(temp_db)

    records = get_records(N)
    # records = [zlib.compress(str(r).encode('utf-8')) for r in records]
    records = [base64.b64encode((zlib.compress(str(r).encode('utf-8')))).decode() for r in records]

    print(f"[Orient]: Creating {len(records)} records")
    all_ids = orient.insert(records)
    print("[Orient]: Created")

    size = orient.client.db_size()

    return size, all_ids, temp_db


@time_it
def load(db_name: int, ids: list):
    print(f"[Orient]: Reading {len(ids)} items.")
    orientdb = OrientDB(db_name)

    all_items = []

    for item_id in ids:
        record = orientdb.retrieve_by_id(item_id)

        item = zlib.decompress(base64.b64decode(record.data.encode())).decode('utf-8')
        all_items.append(item)


def clean(test, key):
    orient = OrientDB(test["dbs"][key]["db"])
    orient.client.db_drop(test["dbs"][key]["db"])
    print(f"[Orient]: Deleted {test["dbs"][key]["db"]}")
