import hashlib
import re
from flask import Blueprint, make_response, session, request, redirect, url_for, jsonify
from module.subscribe import *
from module.user import *

subscribe = Blueprint('subscribe', __name__)


@subscribe.route("/subscribe/id", methods=['GET'])
def get_subscribe_by_username():
    username = session.get('user_name')
    u_id = User().get_by_username(username).first()

    # subscribes = find_by_user_id(u_id)
    subscribes = User().get_by_id(u_id)
    tmp = {}
    for k, v in subscribes.__dict__.items():
        if not k.starswith('_sa_instance_state'):
            tmp[k] = v
    return jsonify(tmp)


@subscribe.route("/subscribe/id&game", methods=['GET'])
def get_subscribe_by_username_and_type():
    username = session.get('user_name')
    u_id = User().get_by_username(username).first()

    g_type = request.form.get('game_type').strip()

    # subscribes = find_by_user_and_type(u_id, g_type)
    subscribes = Subscribe().get_by_user_and_type(u_id, g_type)
    tmp = {}
    for k, v in subscribes.__dict__.items():
        if not k.starswith('_sa_instance_state'):
            tmp[k] = v
    return jsonify(tmp)


@subscribe.route("/subscribe/id&level", methods=['GET'])
def get_subscribe_by_username_and_level():
    username = session.get('user_name')
    u_id = User().get_by_username(username).first()

    level = request.form.get('level_').strip()

    # subscribes = find_by_user_and_level(u_id, level)
    subscribes = Subscribe.get_by_user_and_level(u_id, level)
    tmp = {}
    for k, v in subscribes.__dict__.items():
        if not k.starswith('_sa_instance_state'):
            tmp[k] = v
    return jsonify(tmp)


@subscribe.route("/subscribe/id&plat", methods=['GET'])
def get_subscribe_by_username_and_plat():
    username = session.get('user_name')
    u_id = User().get_by_username(username).first()

    plat = request.form.get('platform').strip()

    # subscribes = find_by_user_and_plat(u_id, plat)
    subscribes = Subscribe().get_by_user_and_plat(u_id, plat)
    tmp = {}
    for k, v in subscribes.__dict__.items():
        if not k.starswith('_sa_instance_state'):
            tmp[k] = v
    return jsonify(tmp)


@subscribe.route("/subscribe/update", methods=['GET'])
def update_subscribe():
    m_subscribe = Subscribe

    username = request.form.get("username").strip()
    u_id = dbsession.query(User).filter_by(user_name=username)

    m_subscribe.user_id = u_id
    m_subscribe.game_type = request.form.get("game_type").strip()
    m_subscribe.level_ = request.form.get("level").strip()
    m_subscribe.platform = request.form.get("platform").strip()

    m_subscribe.update_subscribe()
    return


@subscribe.route("/subscribe/delete", methods=['GET'])
def delete_subscribe():
    m_subscribe = Subscribe

    username = request.form.get("username").strip()
    u_id = dbsession.query(User).filter_by(user_name=username)

    m_subscribe.user_id = u_id
    m_subscribe.game_type = request.form.get("game_type").strip()
    m_subscribe.level_ = request.form.get("level").strip()
    m_subscribe.platform = request.form.get("platform").strip()

    m_subscribe.delete_subscribe()
    return
