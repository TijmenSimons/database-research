import os
import subprocess
import zlib
from aerospikedb import AspikeDB
from utils import get_random_str, get_records, time_it


@time_it
def get_size_aspike_records(N: int, **k):
    print("[Aspike]: Starting")
    temp_db = "test"
    temp_set = get_random_str(12)
    aspike = AspikeDB(temp_db, temp_set)

    records = get_records(N)
    records = [{"d": zlib.compress(str(r).encode('utf-8'))} for r in records]
    # records = [zlib.compress(str(r).encode('utf-8')) for r in records]

    print(f"[Aspike]: Creating {len(records)} records")
    all_ids = aspike.insert(records)
    print("[Aspike]: Created")

    container_name = os.getenv("ASPIKE_CONTAINER_ID")  # Replace with your container name
    command = f"docker exec {container_name} asinfo -v sets -l"

    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    disk_bytes = 0
    if error:
        print(f"Error executing asinfo: {error.decode()}")
    else:
        data = output.decode().split("\n")[:-1]
        data = [d.split(":") for d in data]
        data = [{pair.split('=')[0]: pair.split('=')[1] for pair in data_list} for data_list in data]
        matching_dicts = [d for d in data if d.get("set") == temp_set]

        if matching_dicts:
            disk_bytes = int(matching_dicts[0]["data_used_bytes"])

    return disk_bytes, all_ids, temp_set


@time_it
def load_aspike_records(db_name: str, ids: list):
    print(f"[Aspike]: Reading {len(ids)} items.")
    aspike = AspikeDB("test", db_name)

    all_items = []

    for item_id in ids:
        record = aspike.retrieve_by_id(item_id)
        item = zlib.decompress(record["d"]).decode('utf-8')
        all_items.append(item)


def clean_aspike(test, key):
    aspike = AspikeDB(test["dbs"][key]["db"])
    for id_ in test["dbs"][key]["ids"]:
        aspike.db.remove(("test", test["dbs"][key]["db"], id_))
    print(f"[Aspike]: Cleared {test["dbs"][key]["db"]}")
