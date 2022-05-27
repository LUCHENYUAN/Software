from sqlalchemy import Table, Integer, Column
from common.database import dbconnect
import time

dbsession, md, DBase = dbconnect()


class Reserve(DBase):
    __table__ = Table('reserve', md, autoload=True)

    # reserve_id = Column(Integer, primary_key=True)
    # user_id = Column(Integer)
    # game_id = Column(Integer)

    # 以下为自定义的方法

    def update_reserve(self):
        dbsession.add(self)
        dbsession.commit()
        dbsession.close()
        return

    def delete_reverse(self):
        dbsession.query(Reserve).filter_by(reserve_id=self.reserve_id).delete()
        dbsession.commit()
        dbsession.close()
        return

    def get_by_id(self,r_id):
        reserve = dbsession.query(Reserve).filter_by(reserve_id=r_id).all()
        dbsession.close()
        return reserve

    def get_by_user(self,u_id):
        reserve = dbsession.query(Reserve).filter_by(user_id=u_id).all()
        dbsession.close()
        return reserve

    def get_by_user_and_game(self,u_id, g_id):
        reserve = dbsession.query(Reserve).filter_by(user_id=u_id, game_id=g_id).all()
        dbsession.close()
        return reserve


