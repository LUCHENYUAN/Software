import hashlib
import re
from flask import Blueprint, make_response, session, request, redirect, url_for,jsonify
from module.game import *
from datetime import datetime
game = Blueprint('game', __name__)


@game.route("/game/all", methods=['GET'])
def get_all_game():
    games = Game().get_all()
    # print(games[0])
    gamelist = []
    for game in games:
        gdict = {}
        for k,v in game.__dict__.items():
            if not k.startswith('_sa_instance_state'):
                gdict[k]=v
        gamelist.append(gdict)
    # print ((dict))
    return {'data': gamelist}


@game.route("/game/all_by_time", methods=['GET'])
def get_all_game_by_time():
    mytime = request.args.get('game_start_time')

    # games = get_game_after_date(mytime)
    games = Game().get_after_date(mytime)
    gamelist = []
    for game in games:
        gdict = {}
        for k, v in game.__dict__.items():
            if not k.startswith('_sa_instance_state'):
                gdict[k] = v
        gamelist.append(gdict)
    # print ((dict))
    return {'data': gamelist}

# 传回最新i个比赛的信息，用于主页展示，后续可以更改
@game.route('/displaygames',methods=['GET'])
def display_games():
    if request.method == 'GET':
        index = int(request.args.get('index'))
        # game = get_all_game()[0-index]
        game = Game().get_all[0-index]

        return {"name": game.game_name, "start": game.game_start_time.strftime('%Y-%m-%d %H:%M:%S'),
                "end": game.game_end_time.strftime('%Y-%m-%d %H:%M:%S'),
                "duration": game.duration,"website": game.website,"type":game.game_type ,
                "level": game.level_, "platform": game.platform}
    return {}