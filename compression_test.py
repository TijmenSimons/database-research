import gzip
import secrets
import sys
import zlib
import lz4.frame
from matplotlib import pyplot as plt


# https://stackoverflow.com/questions/45393694/size-of-a-dictionary-in-bytes
def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


def create(num):
    obj = {}
    depth = 0
    
    while depth < num:
        obj[secrets.token_urlsafe(32)] = secrets.token_urlsafe(32)
        depth += 1
    
    return obj


totalwins = {"gzip": 0, "lz4": 0, "zlib": 0, "ties": 0}
test_output = {}

tests, size = 20, 10
for i in range(tests):
    amount = size*(i+1)*(i+1)
    print(f"\n> Test {i+1} - Object size: {amount}")
    wins = {"gzip": 0, "lz4": 0, "zlib": 0, "ties": 0}
    test_totals = {"original": 0,"gzip": 0, "lz4": 0, "zlib": 0}

    for _ in range(size):
        x = create(amount)
        r = str(x)

        gzip_size = get_size(gzip.compress(r.encode('utf-8')))
        lz4_size = get_size(lz4.frame.compress(r.encode('utf-8')))
        zlib_size = get_size(zlib.compress(r.encode('utf-8')))

        test_totals["original"] += get_size(x)
        test_totals["gzip"] += gzip_size
        test_totals["lz4"] += lz4_size
        test_totals["zlib"] += zlib_size

        if gzip_size < lz4_size and gzip_size < zlib_size:
            wins["gzip"] += 1
            continue

        if lz4_size < gzip_size and lz4_size < zlib_size:
            wins["lz4"] += 1
            continue

        if zlib_size < lz4_size and zlib_size < gzip_size:
            wins["zlib"] += 1
            continue

        wins["ties"] += 1

    print(wins)
    totalwins["gzip"] += wins["gzip"]
    totalwins["lz4"] += wins["lz4"]
    totalwins["zlib"] += wins["zlib"]
    totalwins["ties"] += wins["ties"]

    test_output[amount] = test_totals



print(test_output)

print("\n> Totals")
print(totalwins)
print("\n> Percentage")
print({key: f"{value / (tests*size) * 100:.1f}%" for key, value in totalwins.items()})


# x_axis = [key for key in test_output]

# original_line = [value["original"] / 1000 for value in test_output.values()]
# gzip_line = [value["gzip"] / 1000 for value in test_output.values()]
# lz4_line = [value["lz4"] / 1000 for value in test_output.values()]
# zlib_line = [value["zlib"] / 1000 for value in test_output.values()]

# diff_line = [g - z for g, z in zip(gzip_line, zlib_line)]

# plt.plot(x_axis, original_line)
# plt.plot(x_axis, gzip_line, linestyle="dotted", linewidth=4)
# plt.plot(x_axis, lz4_line)
# plt.plot(x_axis, zlib_line, linestyle="dashed")


# plt.xlabel('Grootte van object (totaal aantal velden met random data)')
# plt.ylabel('Aantal bytes in memory')

# plt.legend(["origineel", "gzip", "lz4", "zlib"])
# plt.show()



x_axis = [key for key in test_output]

gzip_line = [value["gzip"] for value in test_output.values()]
zlib_line = [value["zlib"] for value in test_output.values()]

diff_line = [z - g for g, z in zip(gzip_line, zlib_line)]
zero_line = [0 for _ in test_output]

plt.plot(x_axis, diff_line)
plt.plot(x_axis, zero_line, color="black")

plt.xlabel('Grootte van object (totaal aantal velden met random data)')
plt.ylabel('Verschil in grootte in bytes (gzip vs zlib)')

plt.legend(["difference (gzip - zlib)"])
plt.show()
