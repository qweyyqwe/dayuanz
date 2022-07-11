import base64
import hmac
import json
import pickle
import time
import traceback
import logging
import urllib
from datetime import datetime
from hashlib import sha256
from io import BytesIO
import random
from urllib.parse import urlencode

import requests
from flask import Blueprint, jsonify, redirect
from flask_restful import Api, Resource, request

from common.models.admin import OauthUser, User
from common.models import db
from common.utils.db import db1
from common.utils.getdata import get_data
from common.utils.jwt_util import jwt_token

dingding_bp = Blueprint("dingding_bp", __name__)
api = Api(dingding_bp)

# client_id = '3648830690'
# redirect_uri='http://127.0.0.1:8000/users/weiboCallback/'


appid = "dingoajf8cqgyemqarekhr"
redirect_uri = 'http://127.0.0.1:8000/dingding_back'


# 钉钉url
@dingding_bp.route('/get_urls')
def get_url():
    url = "https://oapi.dingtalk.com/connect/qrconnect?appid=%s&response_type=code&scope=snsapi_login&state=STATE&redirect_uri=%s" % (
    appid, redirect_uri)
    return jsonify({'code': 200, 'url': url})


# 钉钉扫码回调地址
@dingding_bp.route('/dingding_back')
def dingding():
    code = request.args.get('code')
    print('code', code)
    # 跳到前端路由
    url = 'http://127.0.0.1:8080/#/dingding?code=' + code
    return redirect(url)


#   钉钉三方登录回调
@dingding_bp.route('/dingdingCallback')
def dingdingCallback():
    # 获取code
    code = request.args.get("code")
    print(code)

    t = time.time()
    # 时间戳
    timestamp = str((int(round(t * 1000))))
    appSecret = 'Fcah25vIw-koApCVN0mGonFwT2nSze14cEe6Fre8i269LqMNvrAdku4HRI2Mu9VK'
    # 构造签名
    signature = base64.b64encode(
        hmac.new(appSecret.encode('utf-8'), timestamp.encode('utf-8'), digestmod=sha256).digest())
    # 请求接口，换取钉钉用户名
    payload = {'tmp_auth_code': code}
    headers = {'Content-Type': 'application/json'}
    res = requests.post('https://oapi.dingtalk.com/sns/getuserinfo_bycode?signature=' + urllib.parse.quote(
        signature.decode("utf-8")) + "&timestamp=" + timestamp + "&accessKey=dingoajf8cqgyemqarekhr",
                        data=json.dumps(payload), headers=headers)

    # res_dict = json.loads(res.text)
    res_json = res.json()
    print('res_json', res_json)
    if res_json['errcode'] != 0:
        return {'message': res_json['errmsg'], 'code': 500, 'data': {'uid': '110'}}
    unid = res_json['user_info']['unionid']
    # 查找用户是否已经添加绑定关系
    user = OauthUser.query.filter_by(uid=unid, oauth_type='dingding').first()
    print('user', user)
    if user:
        # 用户已经添加绑定关系
        if user.user_id:
            # 直接返回主页面
            print('333', user.user_id)
            user = User.query.get(user.user_id)
            print('222', user)
            print(user.id)
            userid = user.id
            username = user.username
            print('username', username)
            # 直接返回主页面
            token = jwt_token.create_token({'userid': userid, 'time': int(time.time())})
            return jsonify({'code': 200, 'username': username, 'userid': userid, 'token': token})

    return jsonify({'code': 201, 'mes': 'Not bind account', 'data': {'uid': unid}})


# 绑定钉钉账号
@dingding_bp.route('/dingding_bind', methods=['post'])
def dingding_bind():
    data = get_data()
    # 钉钉的unid
    unid = data.get('uid')
    # oauth_token = data.get('oauth_token')
    username = data.get('username')
    password = data.get('password')
    print(unid, username, password)
    if not all([unid, username, password]):
        return jsonify({'code': 401, 'mes': '请完善信息'})

    print('unid', unid)
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return {'message': 'not account'}
    is_bind = OauthUser.is_oauth_user(unid, 'dingding')
    if is_bind:
        return {'message': '该用户已经绑定', 'code': 406}
    dingding = OauthUser(uid=unid, oauth_type='dingding', user_id=user.id)
    db.session.add(dingding)
    db.session.commit()

    # 直接返回主页面
    token = jwt_token.create_token({'userid': user.id, 'time': int(time.time())})
    return jsonify({'code': 200, 'username': username, 'userid': user.id, 'token': token})
