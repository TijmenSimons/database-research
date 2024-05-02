from sqlalchemy import select, text
from postgresdb.session import get_db
from sqlalchemy.exc import ProgrammingError


class PostgresDB:
    def __init__(cls, name, base, table_to_check, check: bool = True) -> None:
        cls.base = base
        cls.table_to_check = table_to_check
        cls.name = name
        cls.session, cls.engine = get_db(name)
        if check:
            cls.create_if_not_exists()

    def create_if_not_exists(cls):
        try:
            stmt = select(cls.table_to_check)
            cls.session.execute(stmt).first()

        except ProgrammingError:
            cls.base.metadata.create_all(cls.engine)

    def insert(cls, items: list):

        for item in items:
            cls.session.add(item)
            cls.session.commit()
            cls.session.refresh(item)
        return items

    def retrieve(cls):
        query = select(cls.table_to_check)
        result = cls.session.execute(query)
        return result.scalars().all()

    def retrieve_by_id(cls, id: int):
        query = select(cls.table_to_check).where(cls.table_to_check.id == id)
        result = cls.session.execute(query)
        return result.scalars().all()
    
    def reset(cls):
        cls.session.execute(text("""TRUNCATE TABLE body"""))
        cls.session.commit()
