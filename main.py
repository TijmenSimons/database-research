import os
# import mongodb.normal as mongo_normal
# import mongodb.compress_blob as mongo_compress_blob
# import mongodb.compress_individual as mongo_compress_individual
# import mysqldb.normal as mysql_normal
# import mysqldb.compressed as mysql_compressed
# import aerospikedb.normal as aspike_normal
import aerospikedb.compress as aspike_compressed
# import postgresdb.normal as postgres_normal
# import postgresdb.compress as postgres_cmprss
import redisdb.compress as redis_cmprss
import etcddb.compress as etcd_cmprss
# import arangodb.compress as arango_cmprss
import arangodb.compress64 as arango_cmprss64
import orientdb.compress as orient_cmprss
from utils import format_bytes, get_records


def compare(delete_after: bool = True):
    print("[main]: Starting tests")
    tests = {}

    def add_test(size):
        tests[f"{len(tests.keys())+1}"] = {
            "item_count": size,
            "dbs": {
                "redis_compressd": {
                    "create": redis_cmprss.get,
                    "read": redis_cmprss.load,
                    "clean": redis_cmprss.clean,
                },
                "etcd_compressed": {
                    "create": etcd_cmprss.get,
                    "read": etcd_cmprss.load,
                    "clean": etcd_cmprss.clean,
                },
                # "arango_compress": {
                #     "create": arango_cmprss.get,
                #     "read": arango_cmprss.load,
                #     "clean": arango_cmprss.clean,
                # },
                "arango_cmprss64": {
                    "create": arango_cmprss64.get,
                    "read": arango_cmprss64.load,
                    "clean": arango_cmprss64.clean,
                },
                "orient_compress": {
                    "create": orient_cmprss.get,
                    "read": orient_cmprss.load,
                    "clean": orient_cmprss.clean,
                },
                # "postgres_normal": {
                #     "create": postgres_normal.get_size_sql_records,
                #     "read": postgres_normal.load_sql_records,
                #     "clean": postgres_normal.clean_sql,
                # },
                # "postgres_cmprss": {
                #     "create": postgres_cmprss.get_size_sql_records,
                #     "read": postgres_cmprss.load_sql_records,
                #     "clean": postgres_cmprss.clean_sql,
                # },
                # "aspike_normal": {
                #     "create": aspike_normal.get_size_aspike_records,
                #     "read": aspike_normal.load_aspike_records,
                #     "clean": aspike_normal.clean_aspike,
                # },
                "aspike_comprssd": {
                    "create": aspike_compressed.get_size_aspike_records,
                    "read": aspike_compressed.load_aspike_records,
                    "clean": aspike_compressed.clean_aspike,
                },
                # "mongo_normal": {
                #     "create": mongo_normal.get_size_mongo_records,
                #     "read": mongo_normal.load_mongo_records,
                #     "clean": mongo_normal.clean_mongo,
                # },
                # "mongo_compressd": {
                #     "create": mongo_compress_individual.get_size_mongo_records,
                #     "read": mongo_compress_individual.load_mongo_records,
                #     "clean": mongo_compress_individual.clean_mongo,
                # },
                # "mongo_comp_blob": {
                #     "create": mongo_compress_blob.get_size_mongo_records,
                #     "read": mongo_compress_blob.load_mongo_records,
                #     "clean": mongo_compress_blob.clean_mongo,
                # },
                # "mysql_normal": {
                #     "create": mysql_normal.get_size_sql_records,
                #     "read": mysql_normal.load_sql_records,
                #     "clean": mysql_normal.clean_sql,
                # },
                # "mysql_compressd": {
                #     "create": mysql_compressed.get_size_sql_records,
                #     "read": mysql_compressed.load_sql_records,
                #     "clean": mysql_compressed.clean_sql,
                # }
            }
        }

    add_test(10)
    add_test(100)
    add_test(1000)
    add_test(10000)
    add_test(100000)
    # add_test(500000)

    print(f"[main]: Running {len(tests.keys())} tests")

    print("\n[main]: Phase 1 - Creating objects")

    for key, test in tests.items():
        print(f"\nTest: {key} - {test['item_count']:>{10-len(key)}} records")
        get_records(test["item_count"])

        for key, value in test["dbs"].items():
            timed, size, ids, db = value["create"](test["item_count"], tests=tests)
            test["dbs"][key]["create_time"] = timed
            test["dbs"][key]["size"] = size
            test["dbs"][key]["ids"] = ids
            test["dbs"][key]["db"] = db

    print("\n[main]: Phase 2 - Reading objects")

    for key, test in tests.items():
        for key, value in test["dbs"].items():
            timed, _ = value["read"](test["dbs"][key]["db"], test["dbs"][key]["ids"])
            test["dbs"][key]["read_time"] = timed

    print("\n[main]: Phase 3 - Results")

    for key, test in tests.items():
        print(f"\nTest: {key} - {test['item_count']:>{10-len(key)}} records")
        print("-" * 64)
        for key, value in test["dbs"].items():
            msg = key.capitalize()
            msg += f"\t{format_bytes(test["dbs"][key]['size']):>12}"
            msg += f"\t- write {round(test["dbs"][key]['create_time'], 2):>6}s"
            msg += f"\t- read {round(test["dbs"][key]['read_time'], 2):>6}s"
            print(msg)
        print()

    print("\n[main]: Phase 4 - Cleaning up")

    if delete_after:
        for key, test in tests.items():
            for key, value in test["dbs"].items():
                test["dbs"][key]["clean"](test, key)
    else:
        print("[main]: Cleaning up denied")

    print("\n[main]: Closing connections")


if __name__ == "__main__":
    os.environ["ASPIKE_CONTAINER_ID"] = "6a5e27c34d2c50705c1c050ff051b40f614eb5babf2ad8e9f14a1557bd7d843c"
    os.environ["POSTGRES_CONTAINER_ID"] = "2f6835f1998753ef1dce9ac6633120530b403ebd4c392049afd196cc2a703c57"
    os.environ["ETCD_CONTAINER_ID"] = "bb7759aef4ebc50eb8a816d21f5bceec8538e17b3ca557ba1737af61f9fa25dd,dd2039b7f173c19b608f9e88308eaacde9b9ff40594ae69ba75e88b7ccde8adf,9a60e0c92c88bf2e7096816fad25af5239652e8755c13790132b6dd63b257377"

    compare()
