import hashlib
import re
from flask import Blueprint, make_response, session, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from module.user import *

user=Blueprint('user',__name__)


@user.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.json['name']
        password = request.json['password']
        email = request.json['email']
        phonenum = request.json['phonenum']
        if User().get_by_username(name):
            return {"info": "username occupied", "code": 1}, 400
        if User().get_by_phone(phonenum):
            return {"info": "phone number occupied", "code": 2}, 400
        if User().get_by_mail(email):
            return {"info": "email address occupied", "code": 3}, 400
        pwhash = generate_password_hash(password,method='pbkdf2:sha1', salt_length=8)
        print(pwhash)
        user = User(user_name=name,password=pwhash, mail=email, phone=phonenum,user_type='reg')
        user.add()
        return {"info": "success", "code": 0}
    return {"info": "waiting for request", "code": 0}

@user.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.json['name']
        password = request.json['password']
        user = User().get_by_username(name)[0]
        print(user)
        if not user:
            return {"info": "no such user", "code": 1}, 400
        print(user.password)
        print(type(password))
        print(check_password_hash(user.password,password))
        if not check_password_hash(user.password,password):
            return {"info": "wrong password", "code": 2}, 400
        print(user)
        session['isLogin'] = 'true'
        session['user_id'] = user.user_id
        session['user_name'] = name
        session['type'] = user.user_type
        token = user.user_id
        return {"info": "success", "code": 0, 'result': {'token': token}}

@user.route("/logout")
def logout():
    session['isLogin'] = 'false'
    session['user_id'] = -1
    session['user_name'] = ''
    session['type'] = ''
    return {"info": "success" ,"code": 0}


# fengxuan
@user.route('/alter',methods=['POST'])
def modify():
    user_name1=request.form.get('user_name_old').strip()
    user_name2=request.form.get('user_name_new').strip()
    password=request.form.get('password').strip()
    mail=request.form.get('mail').strip()
    preferrence=request.form.get('preferrence').strip()
    phone=request.form.get('phone').strip()

    user=User()
    res=user.get_by_username(user_name1)

    if res==None:
        return 'user-non-exist'  #用户不存在
    else:
        return user.modify_info(user_name1,user_name2,password,mail,preferrence,phone)


@user.route('/info')
def show_info():
    islogin=session.get('islogin')
    if islogin!=True:
        return 'non-login'

    user_name=session.get('user_name')
    user=User().get_by_username(user_name)
    dict={}
    for k,v in user.__dict__.items():
        if not k.startswith('_sa'):
            dict[k]=v

    print(dict)
    return jsonify(dict)





