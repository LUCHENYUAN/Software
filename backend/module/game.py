from sqlalchemy import Table
from common.database import dbconnect
from datetime import datetime
import time

dbsession, md, DBase = dbconnect()


class Game(DBase):
    __table__ = Table('game', md, autoload=True)

    # 以下为自定义的方法
    def add(self):
        dbsession.add(self)
        dbsession.commit()

    def rm(self):
        dbsession.delete(self)
        dbsession.commit()



    # 获取所有比赛
    def get_all(self):
        res = dbsession.query(Game).all()
        return res

    # 获取指定时间后的所有比赛，参数为datetime类型
    def get_after_date(self,mytime):
        res = dbsession.query(Game).filter(Game.game_start_time.__gt__(mytime)).all()
        return res

    def get_by_name(self,name):
        res = dbsession.query(Game).filter_by(name=name).first()
        return res

    def get_by_site(self,site):
        res = dbsession.query(Game).filter_by(website=site).first()
        return res

    def get_by_type(self,mtype):
        res = dbsession.query(Game).filter_by(game_type=mtype).all()
        return res

    def get_by_level(self,level):
        res = dbsession.query(Game).filter_by(level_=level).all()
        return res

    def get_by_platform(platform):
        res = dbsession.query(Game).filter_by(platform=platform).all()
        return res
#
# # 获取所有比赛
# def get_all_game():
#     res = dbsession.query(Game).all()
#     return res
#
#
# # 获取指定时间后的所有比赛，参数为datetime类型
# def get_game_after_date(mytime):
#     res = dbsession.query(Game).filter(Game.game_start_time.__gt__(mytime)).all()
#     return res
#
#
# def get_game_by_name(name):
#     res = dbsession.query(Game).filter_by(name=name).first()
#     return res
#
#
# def get_game_by_site(site):
#     res = dbsession.query(Game).filter_by(website=site).first()
#     return res
#
#
# def get_game_by_type(mtype):
#     res = dbsession.query(Game).filter_by(game_type=mtype).all()
#     return res
#
#
# def get_game_by_level(level):
#     res = dbsession.query(Game).filter_by(level_=level).all()
#     return res
#
#
# def get_game_by_platform(platform):
#     res = dbsession.query(Game).filter_by(platform=platform).all()
#     return res