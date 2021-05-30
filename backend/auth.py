'''
Description: Copyright © 1999 - 2021 Winter. All Rights Reserved. 
Author: Winter
Email: 837950571@qq.com
Date: 2021-04-16 15:15:43
LastEditTime: 2021-04-16 19:15:00
'''
import functools
from flask import jsonify, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import AUTH_SECRET_KEY

def login_required(view_func):
    @functools.wraps(view_func)
    def verify_token(*args,**kwargs):
        try:
            #在请求头上拿到token
            token = request.headers["token"]
        except Exception:
            #没接收的到token,给前端抛出错误
            #这里的code推荐写一个文件统一管理。这里为了看着直观就先写死了。
            print("没接收的到token")
            return jsonify(code = 4103,msg = '缺少参数token')
        
        s = Serializer(AUTH_SECRET_KEY)
        try:
            s.loads(token)
        except Exception:
            print("登录已过期")
            return jsonify(code = 4101,msg = "登录已过期")

        return view_func(*args,**kwargs)

    return verify_token
