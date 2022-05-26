from sqlalchemy import Table
from common.database import dbconnect
import time

dbsession,md,DBase=dbconnect()


class User(DBase):
    __table__ = Table('user', md, autoload=True)
    #以下为自定义的方法
    def add(self):
        dbsession.add(self)
        dbsession.commit()
    def rm(self):
        dbsession.delete(self)
        dbsession.commit()

    def get_by_username(self, name):
        res = dbsession.query(User).filter_by(user_name=name).all()
        return res

    def get_by_phone(self,phone):
        res = dbsession.query(User).filter_by(phone=phone).first()
        return res

    def get_by_mail(self,mail):
        res = dbsession.query(User).filter_by(mail=mail).first()
        return res


    def modify_info(self,user_name1,user_name2,password,mail,preferrence,phone):
        data = {}

        if user_name2 != None:
            data['user_name'] = user_name2

        if password != None:
            data['password'] = password

        if mail != None:
            data['mail'] = mail

        if preferrence != None:
            data['preferrence'] = preferrence

        if phone != None:
            data['phone'] = phone

        try:
            dbsession.query(User).filter_by(user_name=user_name1).updata(data)
            dbsession.commit()
            return  {"info": "success" ,"code": 0}
        except:
            return {"info": "error" ,"code": 1}



