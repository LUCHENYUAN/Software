import hashlib
import re
from flask import Blueprint, make_response, session, request, redirect, url_for, jsonify
from module.subscribe import *
from module.user import *

subscribe = Blueprint('subscribe', __name__)

#订阅项间以逗号为分割

#增加订阅网站
@subscribe.route("/subscribe/addplatform", methods=['GET'])
def add_plat():
    token = request.args.get("token")
    plat = request.args.get("platform")
    sub = Subscribe().get_by_user_id(token)
    if sub is None:
        sub = Subscribe(user_id=token, platform=plat)
        sub.update_subscribe()
    elif sub.platform is None:
        sub.modify(platform=plat)
    else:
        ori_plats = sub.platform.split(',')
        add_plats = plat.split(',')
        count_add_plats = add_plats.copy()
        for addplat in count_add_plats:
            if addplat in ori_plats:
                add_plats.remove(addplat)
        if add_plats:
            plat = ",".join(add_plats)
            sub.modify(platform=sub.platform+','+plat)
    return {"info": "success", "code": 0}

#取消订阅网站
@subscribe.route("/subscribe/delplatform", methods=['GET'])
def del_plat():
    token = request.args.get("token")
    plat = request.args.get("platform")
    sub = Subscribe().get_by_user_id(token)
    if sub is None:
        return {"info": "no subscribe record for this user", "code": 1}
    elif sub.platform is None:
        return {"info": "no platform subscribe record for this user", "code": 2}
    else:
        ori_plats = sub.platform.split(',')
        del_plats = plat.split(',')
        for delplat in del_plats:
            if delplat in ori_plats:
                ori_plats.remove(delplat)
        plat = ",".join(ori_plats)
        sub.modify(platform=plat)
    return {"info": "success", "code": 0}

#增加订阅等级
@subscribe.route("/subscribe/addlevel", methods=['GET'])
def add_level():
    token = request.args.get("token")
    level = request.args.get("level")
    sub = Subscribe().get_by_user_id(token)
    if sub is None:
        sub = Subscribe(user_id=token, level_=level)
        sub.update_subscribe()
    elif sub.level_ is None:
        sub.modify(level_=level)
    else:
        ori_levels = sub.level_.split(',')
        add_levels = level.split(',')
        count_add_levels = add_levels.copy()
        print(ori_levels)
        print(add_levels)
        for addlevel in count_add_levels:
            if addlevel in ori_levels:
                add_levels.remove(addlevel)
        print(add_levels)
        if add_levels:
            level = ",".join(add_levels)
            sub.modify(level_=sub.level_+','+level)
    return {"info": "success", "code": 0}

#取消订阅等级
@subscribe.route("/subscribe/dellevel", methods=['GET'])
def del_level():
    token = request.args.get("token")
    level = request.args.get("level")
    sub = Subscribe().get_by_user_id(token)
    if sub is None:
        return {"info": "no subscribe record for this user", "code": 1}
    elif sub.level_ is None:
        return {"info": "no level subscribe record for this user", "code": 2}
    else:
        ori_levels = sub.level_.split(',')
        del_levels = level.split(',')
        for dellevel in del_levels:
            if dellevel in ori_levels:
                ori_levels.remove(dellevel)
        level = ",".join(ori_levels)
        sub.modify(level_=level)
    return {"info": "success", "code": 0}


#增加订阅类型
@subscribe.route("/subscribe/addtype", methods=['GET'])
def add_type():
    token = request.args.get("token")
    mtype = request.args.get("type")
    sub = Subscribe().get_by_user_id(token)
    if sub is None:
        sub = Subscribe(user_id=token, game_type=mtype)
        sub.update_subscribe()
    elif sub.game_type is None:
        sub.modify(game_type=mtype)
    else:
        ori_types = sub.game_type.split(',')
        add_types = mtype.split(',')
        count_add_types = add_types.copy()
        for addtype in count_add_types:
            if addtype in ori_types:
                add_types.remove(addtype)
        if add_types:
            mtype = ",".join(add_types)
            sub.modify(game_type=sub.game_type+','+mtype)
    return {"info": "success", "code": 0}

#取消订阅类型
@subscribe.route("/subscribe/deltype", methods=['GET'])
def del_type():
    token = request.args.get("token")
    mtype = request.args.get("type")
    sub = Subscribe().get_by_user_id(token)
    if sub is None:
        return {"info": "no subscribe record for this user", "code": 1}
    elif sub.level_ is None:
        return {"info": "no type subscribe record for this user", "code": 2}
    else:
        ori_types = sub.game_type.split(',')
        del_types = mtype.split(',')
        for deltype in del_types:
            if deltype in ori_types:
                ori_types.remove(deltype)
        mtype = ",".join(ori_types)
        sub.modify(game_type=mtype)
    return {"info": "success", "code": 0}

#获取当前用户的订阅信息
@subscribe.route("/subscribe/byid", methods=['GET'])
def get_subscribe_by_id():
    token = request.args.get("token")
    subscribes = Subscribe().get_by_user_id(token)
    tmp = {}
    for k, v in subscribes.__dict__.items():
        if not k.startswith('_sa_instance_state'):
            tmp[k] = v
    return {'data': tmp}


# @subscribe.route("/subscribe/id", methods=['GET'])
# def get_subscribe_by_username():
#     username = session.get('user_name')
#     u_id = User().get_by_username(username).first()
#
#     # subscribes = find_by_user_id(u_id)
#     subscribes = User().get_by_id(u_id)
#     tmp = {}
#     for k, v in subscribes.__dict__.items():
#         if not k.starswith('_sa_instance_state'):
#             tmp[k] = v
#     return jsonify(tmp)
#
#
# @subscribe.route("/subscribe/id&game", methods=['GET'])
# def get_subscribe_by_username_and_type():
#     username = session.get('user_name')
#     u_id = User().get_by_username(username).first()
#
#     g_type = request.form.get('game_type').strip()
#
#     # subscribes = find_by_user_and_type(u_id, g_type)
#     subscribes = Subscribe().get_by_user_and_type(u_id, g_type)
#     tmp = {}
#     for k, v in subscribes.__dict__.items():
#         if not k.starswith('_sa_instance_state'):
#             tmp[k] = v
#     return jsonify(tmp)
#
#
# @subscribe.route("/subscribe/id&level", methods=['GET'])
# def get_subscribe_by_username_and_level():
#     username = session.get('user_name')
#     u_id = User().get_by_username(username).first()
#
#     level = request.form.get('level_').strip()
#
#     # subscribes = find_by_user_and_level(u_id, level)
#     subscribes = Subscribe.get_by_user_and_level(u_id, level)
#     tmp = {}
#     for k, v in subscribes.__dict__.items():
#         if not k.starswith('_sa_instance_state'):
#             tmp[k] = v
#     return jsonify(tmp)
#
#
# @subscribe.route("/subscribe/id&plat", methods=['GET'])
# def get_subscribe_by_username_and_plat():
#     username = session.get('user_name')
#     u_id = User().get_by_username(username).first()
#
#     plat = request.form.get('platform').strip()
#
#     subscribes = Subscribe().get_by_user_and_plat(u_id, plat)
#     tmp = {}
#     for k, v in subscribes.__dict__.items():
#         if not k.starswith('_sa_instance_state'):
#             tmp[k] = v
#     return jsonify(tmp)


@subscribe.route("/subscribe/update", methods=['GET'])
def update_subscribe():
    m_subscribe = Subscribe()

    username = request.args.get("username").strip()
    u_id = dbsession.query(User).filter_by(user_name=username)
    dbsession.close()

    m_subscribe.user_id = u_id
    m_subscribe.game_type = request.args.get("game_type").strip()
    m_subscribe.level_ = request.args.get("level").strip()
    m_subscribe.platform = request.args.get("platform").strip()

    m_subscribe.update_subscribe()
    return


@subscribe.route("/subscribe/delete", methods=['GET'])
def delete_subscribe():
    m_subscribe = Subscribe()

    username = request.form.get("username").strip()
    u_id = dbsession.query(User).filter_by(user_name=username)
    dbsession.close()

    m_subscribe.user_id = u_id
    m_subscribe.game_type = request.form.get("game_type").strip()
    m_subscribe.level_ = request.form.get("level").strip()
    m_subscribe.platform = request.form.get("platform").strip()

    m_subscribe.delete_subscribe()
    return
