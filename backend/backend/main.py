from flask import Flask, render_template, request, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql
from flask_cors import *

pymysql.install_as_MySQLdb()  # 解决版本兼容性问题

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # 产生sessionid

# 跨域请求
# CORS(app)

# 使用集成方式连接处理sqlalchemy，建议大家密码都改成 commonpass
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:commonpass@localhost:3306/letscode?charset=utf8"

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # 跟踪数据库的修改，及时发送信号
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 跟踪数据库的修改，及时发送信号
# 实例化db对象
db = SQLAlchemy(app)

CORS(app,supports_credentials=True,resources={r"/*"})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html')

@app.errorhandler(500)
def server_error(e):
    return render_template('error_500.html')

@app.route('/')
def home():
    return ('letscode')



if __name__ == '__main__':
    from controller.comment import *
    app.register_blueprint(comment)

    from controller.game import *
    app.register_blueprint(game)

    from controller.post import *
    app.register_blueprint(post)

    from controller.reserve import *
    app.register_blueprint(reserve)

    from controller.subscribe import *
    app.register_blueprint(subscribe)

    from controller.user import *
    app.register_blueprint(user)



    app.jinja_env.auto_reload = True
    app.run(debug=True)