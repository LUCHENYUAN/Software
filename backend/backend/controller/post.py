import hashlib
import re
from flask import Blueprint, make_response, session, request, redirect, url_for, jsonify

from module.post import *

post=Blueprint('post',__name__)

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

if __name__=='__main__':
    read(2)

