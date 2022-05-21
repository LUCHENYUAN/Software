import hashlib
import re
from flask import Blueprint, make_response, session, request, redirect, url_for, jsonify
from common.utility import *
from module.post import *

post=Blueprint('post',__name__)

# 具体阅读某一篇的文章
@post.route('/post/<int:post_id>')
def read(post_id):
    post=Post().get_by_id(post_id)

    dict={}

    for k,v in post.__dict__.items():
        if not k.startswith('_sa_instance_state'):
            dict[k]=v
    print ((dict))
    return jsonify(dict)
    # return ('test')

# 用于显示板块的文章列表
@post.route('/block/<int:type>-<int:page>')
def read_type(type,page):
    post=Post().get_limit_with_user_block(type,10*(page-1),10)

    return jsonify(model_join_list(post))

# 获取热度高的文章
@post.route('/hot')
def get_hot():
    post=Post().get_by_hot()
    return jsonify(model_join_list(post))

if __name__=='__main__':
    read(2)

