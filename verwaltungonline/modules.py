from verwaltungonline import app, db
from sqlalchemy import text

def query_models():
    for t in db.metadata.tables.values():
        pass #        print(t.alias)
    #print(t.alias)
    t = db.metadata.tables
    #print(type(t))
    # models = {
    # mapper.class_.__name__
    # for mapper in db.Model.registry.mappers
    # }
    # print(models)
    # print(type(models))
    # test = list(models)
    # print(test)
    # with app.app_context():
    #     query = text("SELECT * FROM " + test[0])
    #     conn = db.engine.connect()
    #     result = conn.execute(query)
    # for row in result:
    #     print(row[1])


query_models()