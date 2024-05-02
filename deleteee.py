from mongodb import MongoDB


data = [
]


def clean_mongo(db):
    mongo = MongoDB(db)
    mongo.real_db.drop_database(db)
    print(f"[MongoDB]: Deleted {db}")


for i in data:
    clean_mongo(i)
