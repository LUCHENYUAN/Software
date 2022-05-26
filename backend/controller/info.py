import hashlib
import re
from flask import Blueprint, make_response, session, request, redirect, url_for, jsonify
from module.info import *
from datetime import datetime
info = Blueprint('info', __name__)

@info.route('/infoall')
def show_info():
    res=Info().get_info_by_user(request.json['user_id'])
    res+=Info().get_info_by_user(0)

    list=[]
    for row in res:
        dict={}
        for k,v in row.__dict__.items():
            if not k.startswith('_sa'):
                dict[k]=v
        list.append(dict)
    return jsonify(list)
