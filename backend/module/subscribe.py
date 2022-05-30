from sqlalchemy import Table, Column, Integer, String, Boolean
from common.database import dbconnect
import time

dbsession, md, DBase = dbconnect()


class Subscribe(DBase):
    __table__ = Table('Subscribe', md, autoload=True)

    # 以下为自定义的方法

    def update_subscribe(self):
        dbsession.add(self)
        dbsession.commit()
        dbsession.close()
        return

    def delete_subscribe(self):
        dbsession.query(Subscribe).filter_by(subscribe_id=self.subscribe_id).delete()
        dbsession.commit()
        dbsession.close()
        return

    def get_by_user_id(self,u_id):
        subscribes = dbsession.query(Subscribe).filter_by(user_id=u_id).first()
        dbsession.close()
        return subscribes

    def get_by_user_and_type(self,u_id, g_type):
        subscribes = dbsession.query(Subscribe).filter_by(user_id=u_id, game_type=g_type).all()
        dbsession.close()
        return subscribes

    def get_by_user_and_level(self,u_id, lev):
        subscribes = dbsession.query(Subscribe).filter_by(user_id=u_id, level_=lev).all()
        dbsession.close()
        return subscribes

    def get_by_user_and_plat(self,u_id, plat):
        subscribes = dbsession.query(Subscribe).filter_by(user_id=u_id, platform=plat).all()
        dbsession.close()
        return subscribes

    def modify(self, platform=None, game_type=None, level_=None):
        data = {}

        if platform != None:
            data['platform'] = platform

        if game_type != None:
            data['game_type'] = game_type

        if level_ != None:
            data['level_'] = level_

        try:
            dbsession.query(Subscribe).filter_by(subscribe_id=self.subscribe_id).update(data)
            dbsession.commit()
            dbsession.close()
            return {"info": "success", "code": 0}
        except:
            return {"info": "error", "code": 1}