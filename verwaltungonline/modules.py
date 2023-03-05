from routes import app, db, bcrypt
from sqlalchemy import text

def qery_models():
    for t in db.metadata.tables.values():
        pass
    models = {
    mapper.class_.__name__
    for mapper in db.Model.registry.mappers
    }
    query = text("SELECT * FROM " + test[0])
    conn = db.engine.connect()
    result = conn.execute(query)
    for row in result:
        print(row[1])