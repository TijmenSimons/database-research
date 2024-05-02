import os
import zlib
from redisdb import RedisDB
from utils import get_records, time_it


rdb_path = os.path.join(os.getcwd(), 'data', 'dump.rdb')

the_ids = {}


@time_it
def get(N: int, tests, **k):
    print("[Redis]: Starting")
    temp_db = N
    redis = RedisDB(temp_db)

    records = get_records(N)
    records = [zlib.compress(str(r).encode('utf-8')) for r in records]

    print(f"[Redis]: Creating {len(records)} records")
    all_ids = redis.insert(records)
    for x in all_ids:
        the_ids[x] = True
    print("[Redis]: Created")

    redis.db.save()
    rdb_size = os.path.getsize(rdb_path)

    stored_size = sum([test["dbs"]["redis_compressd"].get("size", 0) for test in tests.values()])

    rdb_size -= stored_size

    return rdb_size, all_ids, N


@time_it
def load(db_name: int, ids: list):
    print(f"[Redis]: Reading {len(ids)} items.")
    redisdb = RedisDB(db_name)

    all_items = []

    for item_id in ids:
        if not the_ids.get(item_id):
            print(item_id)
            exit()
        record = redisdb.retrieve_by_id(item_id)
        item = zlib.decompress(record).decode('utf-8')
        all_items.append(item)


def clean(test, key):
    redis = RedisDB(test["dbs"][key]["db"])
    redis.db.flushdb(asynchronous=True)
    print(f"[Redis]: Cleaned redis db {test["dbs"][key]["db"]}")
