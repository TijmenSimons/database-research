import os
import subprocess
import zlib
from etcddb import EtcdDB
from utils import full_bytes, get_records, time_it


rdb_path = os.path.join(os.getcwd(), 'data', 'dump.rdb')


@time_it
def get(N: int, tests, **k):
    print("[Etcd]: Starting")
    temp_db = N
    etcd = EtcdDB(temp_db)

    records = get_records(N)
    records = [zlib.compress(str(r).encode('utf-8')) for r in records]

    print(f"[Etcd]: Creating {len(records)} records")
    all_ids = etcd.insert(records)
    print("[Etcd]: Created")

    disk_bytes = 0
    container_names = os.getenv("ETCD_CONTAINER_ID")  # Replace with your container name
    for name in container_names.split(","):
        command = f"docker exec {name} etcdctl endpoint status"

        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            print(f"Error executing: {error.decode()}")
        else:
            # output: 127.0.0.1:2379, f9bb7dc32e4429fd, 3.5.0, 20 kB, false, false, 3, 15, 15,
            data = output.decode()[:-1].split(", ")[3]
            disk_bytes += int(full_bytes(data))

    stored_size = sum([test["dbs"]["etcd_compressed"].get("size", 0) for test in tests.values()])

    disk_bytes -= stored_size

    return disk_bytes, all_ids, N


@time_it
def load(db_name: int, ids: list):
    print(f"[Etcd]: Reading {len(ids)} items.")
    etcddb = EtcdDB(db_name)

    all_items = []

    for item_id in ids:
        record, meta = etcddb.retrieve_by_id(item_id)
        item = zlib.decompress(record).decode('utf-8')
        all_items.append(item)


def clean(test, key):
    etcd = EtcdDB(test["dbs"][key]["db"])
    etcd.reset(test["dbs"][key]["ids"])
    print(f"[Etcd]: Cleaned etcd prefix {test["dbs"][key]["db"]}")
