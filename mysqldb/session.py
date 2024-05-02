from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def get_db(name: str):
    engine = create_engine("mysql://root:root@localhost:3306/", pool_pre_ping=True)
    
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{name}`"))

    engine.dispose()

    engine = create_engine(f"mysql://root:root@localhost:3306/{name}", pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    return session, engine
