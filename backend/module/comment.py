from flask import session, request
from sqlalchemy import Table
from common.database import dbconnect
from common.utility import model_join_list
from module.user import User
import time

# from common.utility import model_join_list

dbsession, md, DBase = dbconnect()


class Comment(DBase):
    __table__ = Table('comment', md, autoload=True)

    # 新增一条评论
    def insert_comment(self, post_id, content, ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')

        comment = Comment(user_id=request.json['user_id'], user_name=request.json['user_name'], post_id=post_id,
                          content=content,
                          ipaddr=ipaddr, create_time=now, reply_id=0)
        dbsession.add(comment)
        dbsession.commit()

    # 根据文章编号查看所有评论
    def get_by_postid(self, post_id):
        result = dbsession.query(Comment).filter_by(post_id=post_id, hidden=0, reply_id=0).all()
        return result

    def insert_reply(self, post_id, comment_id, content, ipaddr):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        comment = Comment(user_id=request.json['user_id'], user_name=request.json['user_name'], post_id=post_id,
                          content=content, ipaddr=ipaddr, reply_id=comment_id,
                          create_time=now,
                          )
        dbsession.add(comment)
        dbsession.commit()

        # 查找评论与用户信息，注意评论区也要分页

    def get_limit_with_user(self, post_id, start, count):
        res = dbsession.query(Comment, User).join(User, User.user_id == Comment.user_id) \
            .filter(Comment.post_id == post_id, Comment.hidden == 0) \
            .order_by(Comment.comment_id.desc()).limit(count).offset(start).all()
        return res

    def get_comment_with_user(self, post_id, start, count):
        res = dbsession.query(Comment, User).join(User, User.user_id == Comment.user_id) \
            .filter(Comment.post_id == post_id, Comment.hidden == 0, Comment.reply_id == 0) \
            .order_by(Comment.comment_id.desc()).limit(count).offset(start).all()
        return res

    def get_reply_with_user(self, reply_id):
        res = dbsession.query(Comment, User.user_name).join(User, User.user_id == Comment.user_id) \
            .filter(Comment.hidden == 0, Comment.reply_id == reply_id).all()
        return res

    def get_comment_user_list(self, post_id, start, count):
        res1 = self.get_comment_with_user(post_id, start, count)
        comment_list = model_join_list(res1)

        # for comment in comment_list:
        #     res = self.get_reply_with_user(comment['comment_id'])
        #     comment['reply_list'] = model_join_list(res)
        list=[]
        list+=(comment_list)

        while list:
            layer=[]
            for i in list:
                res2 = self.get_reply_with_user(i['comment_id'])
                i['reply_list'] = model_join_list(res2)
                layer += i['reply_list']

            list.clear()
            list+=(layer)

        print(comment_list[1])
        return comment_list



    def get_count_by_postid(self, post_id):
        count = dbsession.query(Comment).filter_by(post_id=post_id, hidden=0, reply_id=0).count()
        return count


