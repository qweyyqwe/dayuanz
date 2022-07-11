# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : login_resoures.py
# @Software: PyCharm


"""
接入微博
"""
# encoding:utf-8
import base64
import hmac
import json
import time
import urllib
from hashlib import sha256
from urllib.parse import urlencode

import requests
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal

from tlogin.custom_output_json import custom_output_json

oauth2_bp = Blueprint('oauth2_bp', __name__, url_prefix='/oauth2')
api = Api(oauth2_bp)


@api.representation('application/json')
def output_json(data, code=200, headers=None):
    return custom_output_json(data, code, headers)


class GetWeiBoUrl(Resource):
    """
    获取微博登录的url
    """

    def post(self):
        url = 'https://api.weibo.com/oauth2/authorize?'  # 微博授权的url地址
        data = {
            'client_id': '3516473472',  # settings.WEIBO_CLIENT_ID
            'response_type': 'code',
            'redirect_uri': 'http://127.0.0.1:8080/oauth/callback/',  # VUE的回调，微博后台授权的回调地址
        }
        weibo_url = url + urlencode(data)
        # https://api.weibo.com/oauth2/authorize?client_id=4152203033&response_type=code&redirect_uri=http://127.0.0.1:8000/api/weibo_back/
        # return Response({'weibo_url': weibo_url})

        return {'message': 'success', 'data': {'url': weibo_url}}, 200


class DingDingCallBack(Resource):
    """
    钉钉三方登录回调
    """

    def get(self):
        # 获取code
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True)
        args = parser.parse_args()
        code = args.get('code')
        print('code>>>>>>>>>>>>>>', code)

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
        # 验证code合法   传了unid
        res = requests.post('https://oapi.dingtalk.com/sns/getuserinfo_bycode?signature=' + urllib.parse.quote(
            signature.decode("utf-8")) + "&timestamp=" + timestamp + "&accessKey=dingoajf8cqgyemqarekhr",
                            data=json.dumps(payload), headers=headers)

        # res_dict = json.loads(res.text)
        res_json = res.json()
        # print('res_json>>>>>>>>>>>>>>', res_json)

        if res_json['errcode'] != 0:
            return {'message': res_json['errmsg'], 'code': 500, 'data': {'uid': '110'}}
        unid = res_json['user_info']['unionid']
        # 查找用户是否已经添加绑定关系
        user = OauthUser.query.filter_by(uid=unid, oauth_type='dingding').first()
        if user:
            # 用户已经添加绑定关系
            if user.user:
                # 直接返回主页面
                users = UserBase.query.get(user.user)
                token = _generate_token(users.account, users.id)
                return {'message': 'ok', 'code': 200, 'data': marshal(users, userbase_fields), 'token': token}
        return {'message': 'Not bind account', 'code': 201, 'data': {'uid': unid}}


class BindDingDing(Resource):
    """
    绑定钉钉账号
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('unid', required=True)
        parser.add_argument('account', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()
        unid = args.get('unid')
        account = args.get('account')
        password = args.get('password')
        # print("unid>>>>>>>>>>", unid)
        # print("绑定钉钉的数据》》》》", account, password)

        user = UserBase.query.filter_by(account=account, password=password).first()
        if not user:
            return {'message': '账号密码错误', 'code': 405}
        dingding = OauthUser(uid=unid, oauth_type='dingding', user=user.id)

        # token, refresh_token = _generate_token(user.account, user.uid)
        # print(token)
        # db.session.add(dingding)
        # db.session.commit()
        # return {'message': 'ok', 'code': 200, 'data': marshal(user, userbase_fields), 'token': token}
        user_id = dingding.id
        db.session.add(dingding)
        db.session.commit()
        token, refresh_token = _generate_token(account, user_id)
        return {'message': 'ok', 'code': 200, 'data': marshal(user, userbase_fields),
                'token': token}


api.add_resource(DingDingCallBack, '/dingding', endpoint='dingding')
api.add_resource(BindDingDing, '/dingding/bind', endpoint='dingding/bind')
