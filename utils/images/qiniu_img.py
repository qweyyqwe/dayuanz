# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 
# @File    : qiniu_img.py
# @Software: PyCharm


from qiniu import Auth
AK = 't3cMfIhCo01zE0bBrsZZN7t6qB4neh8HW_QnOamy'
SK = '97pMyQwZ6A3M_gZa2TKvf_ekuvyli9EPudfxRYKx'
# 要上传的空间
bucket_name = 'shixun-yang-one'


def get_qiniu_token():
    # 构建鉴权对象
    q = Auth(AK, SK)
    # 生成上传Token，可以指定过期时间等
    token = q.upload_token(bucket_name)
    return token


'''
# 封装七牛云token
from qiniu import Auth

# 需要填写你的 Access Key 和 Secret Key
access_key = ""
secret_key = ""

def generate_qiniu_token():
  # 构建鉴权对象
  q = Auth(access_key, secret_key)
  # 要上传的空间
  bucket_name = 'a2107'
  # 生成上传 Token，可以指定过期时间等
  token = q.upload_token(bucket_name, expires=3600)
  return token
'''
