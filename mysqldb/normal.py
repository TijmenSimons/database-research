from sqlalchemy import text
from sqlalchemy.orm import declarative_base
from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from mysqldb import SqlDB
from utils import get_random_str, get_records, time_it


Base = declarative_base()


class Body(Base):
    __tablename__ = "body"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[dict] = mapped_column(JSON, nullable=False)


@time_it
def get_size_sql_records(N: int, **k):
    print("[MySQL]: Starting")
    temp_db = get_random_str(10)
    sql = SqlDB(temp_db, Base, Body)

    records = get_records(N)
    records = [Body(body=r) for r in records]

    print(f"[MySQL]: Creating {len(records)} records")
    all_ids = [body.id for body in sql.insert(records)]
    print("[MySQL]: Created")

    # force sql to recalculate
    sql.session.execute(text("""ANALYZE TABLE `body`;"""))
    
    status = sql.session.execute(text(f"""SELECT table_name AS "Table",
       data_length + index_length AS "size"
FROM information_schema.TABLES
WHERE table_schema = '{temp_db}'
      AND table_name = 'body';"""))
    
    data = next(status)  # returns Body table data, it's the only table
    db_stats = {key: value for (key, value) in zip(status.keys(), data)}

    sql.session.close()

    return db_stats["size"], all_ids, temp_db


@time_it
def load_sql_records(db_name: str, ids: list):
    print(f"[MySQL]: Reading {len(ids)} items.")
    sql = SqlDB(db_name, Base, Body, check=False)

    all_items = []

    for item_id in ids:
        cursor = sql.retrieve_by_id(item_id)
        for item in cursor:
            all_items.append(item)

    sql.session.close()


def clean_sql(test, key):
    sql = SqlDB(test["dbs"][key]["db"], Base, Body, check=False)
    sql.reset()
    sql.session.close()
    print(f"[MySQL]: Deleted {test["dbs"][key]["db"]}")
