from sqlalchemy import text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

from postgresdb import PostgresDB
from utils import get_random_str, get_records, time_it


def get_postgres_db(N):
    return f"test_db_{N}"


Base = declarative_base()


class Body(Base):
    __tablename__ = "body"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[dict] = mapped_column(JSONB, nullable=False)


@time_it
def get_size_sql_records(N: int, **k):
    print("[Postgres]: Starting")
    temp_db = get_postgres_db(N)
    sql = PostgresDB(temp_db, Base, Body)

    records = get_records(N)
    records = [Body(body=r) for r in records]

    print(f"[Postgres]: Creating {len(records)} records")
    all_ids = [body.id for body in sql.insert(records)]
    print("[Postgres]: Created")

    # force sql to recalculate
    # sql.session.execute(text("""ANALYZE TABLE `body`;"""))
    
    status = sql.session.execute(text("""SELECT pg_total_relation_size('body');"""))
    data = next(status)

    sql.session.close()

    return data[0], all_ids, temp_db


@time_it
def load_sql_records(db_name: str, ids: list):
    print(f"[Postgres]: Reading {len(ids)} items.")
    sql = PostgresDB(db_name, Base, Body, check=False)

    all_items = []

    for item_id in ids:
        cursor = sql.retrieve_by_id(item_id)
        for item in cursor:
            all_items.append(item)

    sql.session.close()


def clean_sql(test, key):
    sql = PostgresDB(test["dbs"][key]["db"], Base, Body, check=False)
    sql.reset()
    sql.session.close()
    print(f"[Postgres]: Truncated {test["dbs"][key]["db"]}'s body table")
