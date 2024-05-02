from sqlalchemy import ForeignKey, select, text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

from mysqldb import SqlDB
from utils import get_random_str, get_records, time_it


Base = declarative_base()


class Body(Base):
    __tablename__ = "body"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)

    properties: Mapped["BodyProperty"] = relationship(back_populates="body")


class Property(Base):
    __tablename__ = "property"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)  # will be enum: Types

    bodies: Mapped["BodyProperty"] = relationship(back_populates="property")
    children_properties: Mapped["PropertyProperty"] = relationship(back_populates="parent_property")
    parent_properties: Mapped["PropertyProperty"] = relationship(back_populates="chld_property")


class BodyProperty(Base):
    __tablename__ = "body_property"

    body_id: Mapped[int] = mapped_column(ForeignKey("body.id"), mapped_column=True)
    property_id: Mapped[int] = mapped_column(
        ForeignKey("property.id"), mapped_column=True
    )
    is_required: Mapped[bool] = mapped_column(nullable=False)

    body: Mapped[Body] = relationship(back_populates="properties")
    property: Mapped[Property] = relationship(back_populates="bodies")


class PropertyProperty(Base):
    __tablename__ = "body_property"

    parent_property_id: Mapped[int] = mapped_column(
        ForeignKey("property.id"), mapped_column=True
    )
    chld_property_id: Mapped[int] = mapped_column(
        ForeignKey("property.id"), mapped_column=True
    )
    is_required: Mapped[bool] = mapped_column(nullable=False)

    parent_property: Mapped[Property] = relationship(back_populates="children_properties")
    chld_property: Mapped[Property] = relationship(back_populates="parent_properties")


@time_it
def get_size_sql_records(N: int, **k):
    print("[MySQL]: Starting")
    temp_db = get_random_str(10)
    sql = SqlDB(temp_db, Base, Body)

    records = get_records(N)
    # records = [Body(body=r) for r in records]
    all_ids = []

    for record in records:
        body = Body(name=get_random_str(10))
        
        for key, value in record.items():
            query = select(Property).where(Property.name == key)
            result = sql.session.execute(query)
            if (prop := result.scalars().first()) is None:
                prop = Property(name=key)
            
            body.properties.append(prop)
        
        sql.session.add(body)
        sql.session.commit()
        sql.session.refresh(body)

        all_ids.append(body.id)

        


    print(f"[MySQL]: Creating {len(records)} records")
    all_ids = [body.id for body in sql.insert(records)]
    print("[MySQL]: Created")

    # force sql to recalculate
    sql.session.execute(text("""ANALYZE TABLE `body`;"""))

    status = sql.session.execute(
        text(f"""SELECT table_name AS "Table",
       data_length + index_length AS "size"
FROM information_schema.TABLES
WHERE table_schema = '{temp_db}'
      AND table_name = 'body';""")
    )

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


def clean_sql(test):
    sql = SqlDB(test["dbs"]["mysql"]["db"], Base, Body, check=False)
    sql.reset()
    sql.session.close()
    print(f"[MySQL]: Deleted {test["dbs"]["mysql"]["db"]}")
