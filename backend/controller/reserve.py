import hashlib
import re
from flask import Blueprint, make_response, session, request, redirect, url_for, jsonify
from module.user import *
from module.reserve import *
from module.game import *

reserve = Blueprint('reserve', __name__)


@reserve.route("/reserve/username", methods=['GET'])
def get_reserve_by_user2():
    username = session.get('user_name')
    u_id = User().get_by_username(username).first()

    # reserves = find_by_user(u_id)
    reserves = Reserve().get_by_user(u_id)
    tmp = {}
    for k, v in reserves.__dict__.items():
        if not k.starswith('_sa_instance_state'):
            tmp[k] = v
    return jsonify(tmp)


@reserve.route("/reserve/user&game", methods=['GET'])
def get_reserve_by_user():
    username = session.get('user_name')
    u_id = User().get_by_username(username).first()

    g_name = request.form.get('game_name')
    # g_id = get_game_by_name(g_name).first()
    g_id = Game().get_by_name(g_name).first()

    # reserves = find_by_user_and_game(u_id,g_id)
    reserves = Reserve.get_by_user_and_game(u_id, g_id)
    tmp = {}
    for k, v in reserves.__dict__.items():
        if not k.starswith('_sa_instance_state'):
            tmp[k] = v
    return jsonify(tmp)


# 这里好像有点问题，不过也可能我错了，大家可以一起讨论下
@reserve.route("/reserve/update", methods=['GET'])
def reserve_update():
    m_reserve = Reserve(user_id=request.form.get("username").strip(), game_id=request.form.get("game_name").strip())

    # username = request.form.get("username").strip()
    # m_reserve.user_id = dbsession.query(User).filter_by(user_name=username).first()
    #
    # g_name = request.form.get("game_name").strip()
    # m_reserve.game_id = dbsession.query(Game).filter_by(game_name=g_name).first()

    m_reserve.update_reserve()
    return


@reserve.route("/reserve/delete", methods=['GET'])
def reserve_delete():
    username = request.form.get("username").strip()
    g_name = request.form.get("game_name").strip()

    m_reserve = dbsession.query(User).filter_by(user_name=username, game_name=g_name).first()
    m_reserve.delete_reverse()

    return
