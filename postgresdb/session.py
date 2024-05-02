import os
import subprocess
import time
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from docker import DockerClient


def wait_for_database(dbname, retries=10, delay=5):
    for _ in range(retries):
        try:
            engine = create_engine(f"postgresql://postgres:example@localhost:5432/{dbname}")
            with engine.connect() as connection:
                connection.execute("SELECT 1")  # Test the connection
            return True
        except OperationalError:
            print("Database is not yet available. Retrying...")
            time.sleep(delay)
    
    print("Max retries exceeded. Database might not be available.")
    return False


def get_db(name: str):
    # engine = create_engine("postgresql+psycopg2://postgres:example@localhost:5432/")
    
    # with engine.connect() as connection:
    #     connection.execute(text("COMMIT"))
    #     connection.execute(text("END TRANSACTION"))
    #     connection.exec_driver_sql(f'DROP DATABASE IF EXISTS "{name}"; CREATE DATABASE "{name}";')

    # engine.dispose()

    container_name = os.getenv("POSTGRES_CONTAINER_ID")

    client = DockerClient()

    # Get the container object
    container = client.containers.get(container_name)

    # sql_command = f"DROP DATABASE IF EXISTS \"{name}\";"
    # exec_cmd = ["psql", "-U", "postgres", "-c", sql_command]
    # print(container.exec_run(exec_cmd))

    sql_command = f"CREATE DATABASE \"{name}\";"
    exec_cmd = ["psql", "-U", "postgres", "-c", sql_command]
    output = container.exec_run(exec_cmd)
    # print(output)


    # commands = [
    #     # f'docker exec -i {container_name} psql -U postgres -c "COMMIT;"',
    #     f'docker exec -i {container_name} psql -U postgres -c "DROP DATABASE IF EXISTS \\"{name}\\";"',
    #     f'docker exec -i {container_name} psql -U postgres -c "CREATE DATABASE \\"{name}\\";"'
    # ]

    # wait_for_database(name)

    engine = create_engine(f"postgresql://postgres:example@localhost:5432/{name}")
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    return session, engine
