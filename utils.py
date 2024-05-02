import json
import random
import string
import time
from typing import Callable
from mongodb.actions import Field, MongoActions


def get_random_str(length: int):
    return f"%0{length}x" % random.randrange(16**length)


# "caching" records so we have data consistency
stored_records: dict[int, list[dict[str, Field]]] = {}


def deepcopy(obj):
    return json.loads(json.dumps(obj))


def get_records(N: int, **k) -> list[dict[str, Field]]:
    print(f"[main]: Getting {N} records.")
    global stored_records

    if stored_records.get(N):
        return deepcopy(stored_records[N])

    print(f"[main]: Records not exist, generating {N} records...")
    records: list[dict[str, Field]] = []
    for _ in range(N):
        field_count = random.choice(range(5, 15))
        item: dict[str, Field] = {
            get_random_str(2): MongoActions.create_field() for _ in range(field_count)
        }
        records.append(item)

    stored_records[N] = records
    return deepcopy(records)


def format_bytes(size):
    if size == 0:
        return "unknown"

    power = 1024  # 2**10 = 1024
    n = 0
    power_labels = {0: "", 1: "K", 2: "M", 3: "G", 4: "T"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]+'B'}"


def full_bytes(size_str):
    size_str = size_str.strip()
    size, unit = size_str.split(" ")
    unit = unit.lower()
    size = float(size)
    if unit == "kb":
        return size * 1024
    elif unit == "mb":
        return size * 1024 * 1024
    elif unit == "gb":
        return size * 1024 * 1024 * 1024
    else:
        return size


def time_it(func: Callable):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        if isinstance(result, (list, tuple)):
            final = (end - start, *result)
        else:
            final = (end - start, result)
        return final

    return wrapper


def get_random_ltrs(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

