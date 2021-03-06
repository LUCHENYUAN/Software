import hashlib
import re
from flask import Blueprint, make_response, session, request, redirect, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from common.utility import *
from module.game import Game
from module.user import *
from flask_mail import Message
from main import mail
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
        user = User(user_name=name, password=pwhash, mail=email, phone=phonenum, user_type='reg', mail_confirmed=False)
        user.add()
        #邮箱认证
        subject = "邮箱验证-注册"
        recipient = email
        ##这里是后端的验证邮箱路由，带用户邮箱参数
        url = "http://127.0.0.1:5000/confirmEmail?mail=" + str(email)
        body = "<p>感谢您使用Letscode！</p> <a href=\"" + str(url) + "\" rel=\"bookmark\">请点击此链接，进行邮箱认证</a>"
        mes = Message(subject=subject, recipients=[recipient], html=body)
        mail.send(mes)
        return {"info": "success", "code": 0}
    return {"info": "waiting for request", "code": 0}

@user.route('/confirmEmail',methods=['GET'])
def confirmEmail():
    email = request.args.get('mail')
    user = User().get_by_mail(email)
    user.modify(mail_confirmed=True)
    return "邮箱验证成功，快去登录吧！"


@user.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.json['name']
        password = request.json['password']

        user = User().get_by_username(name)[0]
        # print(user.__dict__)
        if not user:
            return {"info": "no such user", "code": 1}, 400
        if not user.mail_confirmed:
            return {"info": "mail not confirmed", "code": 3}, 400
        print(user.password)
        print(type(password))
        print(check_password_hash(user.password,password))

        if not check_password_hash(user.password,password):
            return {"info": "wrong password", "code": 2}, 400
        # print(user)
        session['isLogin'] = 'true'
        session['user_id'] = user.user_id
        session['user_name'] = name
        session['type'] = user.user_type
        token = user.user_id

        return {"info": "success", "code": 0, 'result': {'token': token}}

@user.route('/loginByPhone',methods=['GET','POST'])
def loginByPhone():
    if request.method == 'POST':
        phone = request.json['phone']
        password = request.json['password']

        user = User().get_by_phone(phone)[0]
        # print(user.__dict__)
        if not user:
            return {"info": "no such user", "code": 1}, 400
        print(user.password)
        print(type(password))
        print(check_password_hash(user.password,password))

        if not check_password_hash(user.password,password):
            return {"info": "wrong password", "code": 2}, 400
        # print(user)
        session['isLogin'] = 'true'
        session['user_id'] = user.user_id
        session['user_name'] = user.user_name
        session['type'] = user.user_type
        token = user.user_id

        return {"info": "success", "code": 0, 'result': {'token': token}}

@user.route('/loginByMail',methods=['GET','POST'])
def loginByMail():
    if request.method == 'POST':
        mail = request.json['mail']
        password = request.json['password']

        user = User().get_by_mail(mail)[0]
        # print(user.__dict__)
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
        session['user_name'] = user.user_name
        session['type'] = user.user_type
        token = user.user_id

        return {"info": "success", "code": 0, 'result': {'token': token}}

@user.route('/changePassword',methods=['GET','POST'])
def changePassword():
    if request.method == 'POST':
        token = request.json['token']
        oripwd = request.json['oripwd']
        newpwd = request.json['newpwd']

        user = User().get_by_id(token)[0]
        if not user:
            return {"info": "no such user", "code": 1}, 400
        if not check_password_hash(user.password,oripwd):
            return {"info": "wrong original password", "code": 2}, 400
        pwhash = generate_password_hash(newpwd, method='pbkdf2:sha1', salt_length=8)
        user.modify(password=pwhash)
        return {"info": "success", "code": 0}

@user.route('/favicon.ico')
def default():
    return {}

@user.route('/forgotPassword',methods=['GET','POST'])
def forgotPassword():
    if request.method == 'POST':
        email = request.json['mail']
        user = User().get_by_mail(email)
        if not user:
            return {"info": "no such user", "code": 1}, 400
        subject = "邮箱验证-忘记密码"
        recipient = email
        ##这里是前端的重置密码界面的url，带用户邮箱参数
        url = "http://127.0.0.1:8080/resetpwd?mail="+str(user.email)
        body = "<p>感谢您使用Letscode！</p> <a href=\""+str(url)+"\" rel=\"bookmark\">请点击此链接，重置密码</a>"
        mes = Message(subject=subject, recipients=[recipient], html=body)
        mail.send(mes)
        return {"info": "success", "code": 0}
    # if request.method == 'GET':
    #     email = request.args.get('mail')
    #     print(email)
    #     user = User().get_by_mail(email)
    #     if not user:
    #         return {"info": "no such user", "code": 1}, 400
    #     subject = "邮箱验证-忘记密码"
    #     recipient = email
    #     ##这里是前端的重置密码界面的url，带用户邮箱参数
    #     url = "http://127.0.0.1:8080/resetpwd?mail="+user.mail
    #     body = "<p>感谢您使用Letscode！</p> <a href=\""+url+"\" rel=\"bookmark\">请点击此链接，重置密码</a>"
    #     mes = Message(subject=subject, recipients=[recipient], html=body)
    #     mail.send(mes)
    #     return {"info": "success", "code": 0}

#忘记密码邮箱验证后，不需要原密码
@user.route('/resetPassword',methods=['GET','POST'])
def resetPassword():
    if request.method == 'POST':
        email = request.json['email']
        newpwd = request.json['newpwd']

        user = User().get_by_mail(email)[0]
        if not user:
            return {"info": "no such user", "code": 1}, 400
        pwhash = generate_password_hash(newpwd, method='pbkdf2:sha1', salt_length=8)
        user.modify(password=pwhash)
        return {"info": "success", "code": 0}


@user.route("/logout")
def logout():
    session['isLogin'] = 'false'
    session['user_id'] = -1
    session['user_name'] = ''
    session['type'] = ''
    return {"info": "success" ,"code": 0}


# 修改个人信息
@user.route('/alter',methods=['POST'])
def alter():
    user_name1=request.form.get('user_name_old').strip()
    user_name2=request.form.get('user_name_new').strip()
    password=request.form.get('password').strip()
    mail=request.form.get('mail').strip()
    preferrence=request.form.get('preferrence').strip()
    phone=request.form.get('phone').strip()

    user=User()
    res=user.get_by_username(user_name1)

    if res==None:
        return {"info": "error" ,"code": 2} #2为用户不存在
    else:
        return user.modify_info(user_name1,user_name2,password,mail,preferrence,phone) #1为修改失败 ，0为修改成功


@user.route('/info/user')
def show_info():
    u_id=request.json['user_id']
    if u_id==None:
        return {"info": "error" ,"code": 0} #未等录

    user_name=request.json['user_name']
    user=User().get_by_username(user_name)
    dict={}
    for k,v in user.__dict__.items():
        if not k.startswith('_sa'):
            dict[k]=v

    print(dict)
    return jsonify(dict)

@user.route('/sendset')
def set_send():
    send_time=request.form.get('send_time').strip()
    send_way=request.form.get('send_way').strip()

    user_id=request.json['user_id']
    try:
        dbsession.query(User).filter_by(user_id=user_id).update({'send_time':send_time})
        dbsession.query(User).filter_by(user_id=user_id).update({'send_way':send_way})
        dbsession.commit()
        dbsession.close()
        return {"info": "success" ,"code": 0}
    except:
        return {"info": "error" ,"code": 1} #修改失败

#以下均为管理员操作

#禁用用户权限/恢复用户权限
@user.route('/black/<user_id>')
def set_black_white(user_id):
    u_id=request.form.get('user_id')
    black=request.form.get('black')

    if u_id==None or black==None:
        return {"info":"error","code":2}  #前端获取信息不完整

    try:
        dbsession.query(User).filter_by(user_id=user_id).update({"black":black})
        dbsession.commit()
        dbsession.close()
        return {"info": "success", "code": 0}

    except:
        return {"info": "error", "code": 1}  # 修改失败


@user.route('/info/unchecked-game')
def show_unchecked_game():
    res=Game().get_all_uchecked()
    for i in res:
        print(i.__dict__)

    list=[]

    for i in res:
        dict={}
        for k,v in i.__dict__.items():
            if not k.startswith('_sa_instance_state'):
                dict[k]=v
        list.append(dict)

    return  jsonify(list)

@user.route('/check/<game_id>')
def check_game(game_id):
    try:
        Game().set_checked_by_id(game_id)
        return {"info":"success","code":0}
    except:
        return {"info": "error", "code": 1}  # 修改失败


