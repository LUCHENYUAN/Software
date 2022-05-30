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
        dbsession.close()
    def rm(self):
        dbsession.delete(self)
        dbsession.commit()
        dbsession.close()


    def get_by_username(self, name):
        res = dbsession.query(User).filter_by(user_name=name).all()
        dbsession.close()
        return res

    def get_by_id(self, id):
        res = dbsession.query(User).filter_by(user_id=id).first()
        dbsession.close()
        return res

    def get_by_phone(self,phone):
        res = dbsession.query(User).filter_by(phone=phone).first()
        dbsession.close()
        return res

    def get_by_mail(self,mail):
        res = dbsession.query(User).filter_by(mail=mail).first()
        dbsession.close()
        return res

    def modify(self,user_name=None,password=None,mail=None,preferrence=None,phone=None,mail_confirmed=None):
        data = {}

        if user_name != None:
            data['user_name'] = user_name

        if password != None:
            data['password'] = password

        if mail != None:
            data['mail'] = mail

        if preferrence != None:
            data['preferrence'] = preferrence

        if phone != None:
            data['phone'] = phone

        if mail_confirmed != None:
            data['mail_confirmed'] = mail_confirmed

        try:
            dbsession.query(User).filter_by(user_id = self.user_id).update(data)
            # self.update(data)
            dbsession.commit()
            dbsession.close()
            return  {"info": "success" ,"code": 0}
        except:
            return {"info": "error" ,"code": 1}


    def modify_info(self,user_name1=None,user_name2=None,password=None,mail=None,preferrence=None,phone=None,mail_confirmed=None):
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

        if mail_confirmed != None:
            data['mail_confirmed'] = mail_confirmed

        try:
            dbsession.query(User).filter_by(user_name=user_name1).update(data)
            dbsession.commit()
            dbsession.close()
            return  {"info": "success" ,"code": 0}
        except:
            return {"info": "error" ,"code": 1}



    #以下内容只有管理员才有权限操作
    #禁用该用户的权限
    def set_user_black(self,user_id):
        data={'black':1}
        try:
            dbsession.query(User).filter_by(user_id=user_id).update(data)
            dbsession.commit()
            dbsession.close()
            return {"info": "success" ,"code": 0}
        except:
            return {"info": "error", "code": 1}

    # 恢复该用户的权限
    def set_user_white(self,user_id):
        data={'black':0}
        try:
            dbsession.query(User).filter_by(user_id=user_id).update(data)
            dbsession.commit()
            dbsession.close()
            return {"info": "success" ,"code": 0}
        except:
            return {"info": "error", "code": 1}




