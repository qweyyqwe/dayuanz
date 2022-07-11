import time
import traceback

import requests
from flask import Blueprint,jsonify,redirect
from flask_restful import Api,Resource,request
from werkzeug.security import check_password_hash

from common.models.admin import OauthUser
from common.utils.db import db1
from common.utils.getdata import get_data
from common.utils.jwt_util import jwt_token

weibo_bp = Blueprint("weibo_bp",__name__)
api = Api(weibo_bp)


client_id = '3648830690'
redirect_uri='http://127.0.0.1:8000/users/weiboCallback/'

# 微博url
@weibo_bp.route('/get_url')
def get_url():
    url = "https://api.weibo.com/oauth2/authorize?client_id=%s&response_type=code&redirect_uri=%s" % (
        client_id, redirect_uri)
    return jsonify({'code':200,'url':url})



# 微博登录回调地址
@weibo_bp.route('/users/weiboCallback/')
def weibo():
    code = request.args.get('code')
    # 跳到前端路由
    url = 'http://127.0.0.1:8080/#/weibo?code='+code
    return redirect(url)


# 微博前端回调
@weibo_bp.route('/weiboCallback')
def weiboCallback():
    code = request.args.get('code')
    # 微博认证地址
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    # 参数
    response = requests.post(access_token_url,data={
        "client_id": '3648830690',
        "client_secret": "916d80b477ccffce5d70e63b02bb1092",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:8000/users/weiboCallback/",
    })
    # .json（）将获取的字符串形式的json数据反序列化成字典或者列表对象
    res = response.json()
    print(res)
    # 微博的uid
    uid = res['uid']
    oauth_token = res['access_token']
    print('uid',uid)
    # 查找用户是否已经添加绑定关系
    sql = "select * from oauth_user where uid='%s'"%uid
    oauth_user = db1.find_one(sql)
    print('oauth-user',oauth_user)
    if oauth_user:
        # 用户已经添加绑定关系
        if oauth_user['user_id']:
            user_id = oauth_user['user_id']
            sql2 = "select username from user where id=%d"%user_id
            user = db1.find_one(sql2)
            # 直接返回主页面
            token = jwt_token.create_token({'userid':user_id,'time':int(time.time())})
            return jsonify({'code':200,'username':user['username'],'userid':user_id,'token':token})

    return jsonify({'code':201,'mes':'Not bind account','data':{'uid':uid,'oauth_token':oauth_token}})



# 绑定微博账号
@weibo_bp.route('/bind',methods=['post'])
def bind():
    data = get_data()
    # 微博的uid
    uid = data.get('uid')
    oauth_token = data.get('oauth_token')
    username = data.get('username')
    password = data.get('password')
    print(uid,oauth_token,username,password)
    if not all([uid,username,password,oauth_token]):
        return jsonify({'code':401,'mes':'请完善信息'})

    # sql = "select * from user where username='%s' and password='%s'"%(username,password)
    sql = "select * from user where username='%s'" % (username)
    user = db1.find_one(sql)
    if not user:
        return {'code': 402}
    print('res', user)
    if not check_password_hash(user['password'], password):
    # user = db1.find_one(sql)
    # print('user',user)
    # if not user:
        return jsonify({'code':403,'mes':'账号或密码错误'})
    # 判断是否绑定
    sql = "select * from oauth_user where uid='%s'" % uid
    is_bind = db1.find_one(sql)
    print('is_bind',is_bind)
    if is_bind:
        return jsonify({'code':406,'mes':'该用户已经绑定'})
    try:
        sql2 = "insert into oauth_user(uid,user_id,oauth_token,oauth_type) values('%s',%d,'%s','%s')"%(uid,user['id'],oauth_token,'weibo')
        print('sql2',sql2)
        db1.update(sql2)
        db1.commit()

        # 直接返回主页面
        token = jwt_token.create_token({'userid': user['id'], 'time': int(time.time())})
        print('token',token)
        return jsonify({'code': 200, 'username': user['username'], 'userid': user['id'], 'token': token})

    except:
        error = traceback.format_exc()
        db1.rollbock()
        return jsonify({'code':500})


