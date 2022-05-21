#封装数据库的公用操作
from sqlalchemy import MetaData

def dbconnect():
    from main import db
    dbsession=db.session
    DBase=db.Model
    metadata=MetaData(bind=db.engine)
    return (dbsession,metadata,DBase)