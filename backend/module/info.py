from sqlalchemy import Table, func
from common.database import dbconnect
import time
from module.user import *

dbsession,md,DBase=dbconnect()

class Info(DBase):
    __table__ = Table('info', md, autoload=True)

    def get_info_by_user(self,user_id):
        res=dbsession.query(Info).filter(Info.user_id==user_id).all()
        return res