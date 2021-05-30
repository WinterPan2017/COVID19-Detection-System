'''
Description: Copyright © 1999 - 2021 Winter. All Rights Reserved. 
Author: Winter
Email: 837950571@qq.com
Date: 2021-04-14 18:55:10
LastEditTime: 2021-04-16 19:16:29
'''
from flask import Blueprint, Response, jsonify, request, send_from_directory, make_response
import os
import cv2
import base64
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import AUTH_SECRET_KEY

from models import User

login_blue = Blueprint('login', __name__)


# 显示检测记录界面
@login_blue.route('/login', methods=["post"])
def login():
    # token = request.headers["token"]
    print(request.cookies.get('token'))
    username = request.form["username"]
    password = request.form["password"]
    # 验证密码
    print(username, password)
    user = User.query.filter_by(account=username).first()
    if user is None or user.password != password:
        return "", 401
    # 验证成功
    userid = user.userid
    s = Serializer(AUTH_SECRET_KEY, expires_in=36000)
    token = s.dumps({"userid": userid}).decode("ascii")
    res = {"token": token}
    response = make_response(jsonify(res))
    return response, 200
