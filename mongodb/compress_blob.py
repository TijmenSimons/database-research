import zlib
from mongodb import MongoDB
from utils import get_random_str, get_records, time_it


@time_it
def get_size_mongo_records(N: int, **k):
    print("[MongoDB]: Starting")
    temp_db = get_random_str(12)
    temp_col = "body"
    mongo = MongoDB(dbname=temp_db, collection=temp_col)

    records = get_records(N)
    records = [{"d": zlib.compress(str(r).encode('utf-8'))} for r in records]

    print(f"[MongoDB]: Creating {len(records)} records")
    all_ids = mongo.insert(records).inserted_ids
    print("[MongoDB]: Created")

    # https://stackoverflow.com/questions/18836064/pymongo-method-of-getting-statistics-for-collection-byte-usage
    db_stats = mongo.db.command("dbstats")

    return db_stats["dataSize"], all_ids, temp_db


@time_it
def load_mongo_records(db_name: str, ids: list):
    print(f"[MongoDB]: Reading {len(ids)} items.")
    mongo = MongoDB(db_name, "body")

    all_items = []

    for item_id in ids:
        cursor = mongo.retrieve_by_id(item_id)
        for item in cursor:
            item = zlib.decompress(item["d"]).decode('utf-8')
            all_items.append(item)


def clean_mongo(test, key):
    mongo = MongoDB(test["dbs"][key]["db"])
    mongo.db.drop_collection(test["dbs"][key]["db"])
    print(f"[MongoDB]: Deleted {test["dbs"][key]["db"]}")
