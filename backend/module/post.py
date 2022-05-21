from sqlalchemy import Table, func
from common.database import dbconnect
import time
from module.user import *

dbsession,md,DBase=dbconnect()

class Post(DBase):
    __table__ = Table('post', md, autoload=True)

    #以下为自定义的方法
    #查询所有文章
    def get_all(self):
        res=dbsession.query(Post).all()

    #根据id查询文章
    def get_by_id(self,post_id):
        row=dbsession.query(Post).filter(Post.post_id==post_id,Post.drafted==0,Post.checked==1).first()
        return row

    #指定分页的limit和offset，同时与User表作连接查询,实现分页功能
    def get_limit_with_user(self,start,count):
        #倒叙排列
        res=dbsession.query(Post,User.user_name).join(User,User.user_id==Post.user_id)\
            .filter(Post.drafted==0,Post.checked==1).order_by(Post.post_id.desc())\
        .limit(count).offset(start).all()
        return res

    def get_limit_with_user(self,start,count):
        #倒叙排列
        res=dbsession.query(Post,User.user_name).join(User,User.user_id==Post.user_id)\
            .filter(Post.drafted==0,Post.checked==1).order_by(Post.post_id.desc())\
        .limit(count).offset(start).all()
        return res

    def get_limit_with_user_block(self,block_type,start,count):
        #倒叙排列
        res=dbsession.query(Post,User.user_name).join(User,User.user_id==Post.user_id)\
            .filter(Post.drafted==0,Post.checked==1,Post.block_type==block_type).order_by(Post.post_id.desc())\
        .limit(count).offset(start).all()
        return res

    def get_by_hot(self):
        max=dbsession.query(func.max(Post.com_count)).all()
        avg=dbsession.query(func.avg(Post.com_count)).all()

        res=dbsession.query(Post,User.user_name).join(User,User.user_id==Post.user_id).filter(Post.com_count>=avg,Post.com_count<=max).all()
        return res