'''
Description: Copyright © 1999 - 2020 Winter. All Rights Reserved. 
Author: Winter
Email: 837950571@qq.com
Date: 2021-04-01 16:44:44
LastEditTime: 2021-04-17 14:08:47
'''
from flask import Blueprint, Response, jsonify, request, send_from_directory, make_response, send_file
import os
import cv2
import base64
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from auth import login_required
import io, zipfile
from werkzeug.wsgi import FileWrapper

from models import DRecord, ARecord, db

record_blue = Blueprint('record', __name__)


# 显示检测记录界面
@record_blue.route('/getRecord', methods=["get"])
@login_required
def getRecord():
    token = request.headers["token"]
    s = Serializer("SECRET_KEY")
    # try:
    data = s.loads(token)
    print(data)
    userid = data["userid"]
    drecords = DRecord.query.filter_by(userid=userid).all()
    res = []
    for drecord in drecords:
        res.append({
            "key": drecord.drecordid,
            "name": drecord.name,
            "description": drecord.description,
            "time": str(drecord.time),
            "category": drecord.category,
            "num": drecord.num,
            "diagnosis": drecord.diagnosis
        })
    return jsonify(res)
    # except Exception:
    #     return "", 401


# 显示检测记录界面
@record_blue.route('/deleteRecord', methods=["get"])
@login_required
def deleteRecord():
    token = request.headers["token"]
    s = Serializer("SECRET_KEY")
    try:
        data = s.loads(token)
        userid = data["userid"]
    except Exception:
        return "", 401

    drecordid = request.args["drecord"]
    print("delete record", userid, drecordid)
    drecord = DRecord.query.filter_by(drecordid=drecordid).all()
    if len(drecord) == 0:
        return ""
    arecords = ARecord.query.filter_by(drecordid=drecordid).all()
    for arecord in arecords:
        # 删除文件
        path = os.path.dirname(arecord.rawimage)
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
        os.removedirs(path)
        db.session.delete(arecord)
        db.session.commit()
    db.session.delete(drecord[0])
    db.session.commit()
    return "ok"


#下载
@record_blue.route('/downloadRecord', methods=["GET"])
@login_required
def download():
    print("token", request.headers["token"])
    drecordid = request.args["drecord"]
    print(drecordid)
    drecord = DRecord.query.filter_by(drecordid=drecordid).all()[0]
    arecords = ARecord.query.filter_by(drecordid=drecordid).all()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zfile:
        zfile.writestr(
            "result.txt",
            f"命名:{drecord.name}\n描述:{drecord.description}\n时间:{drecord.time}\n检查类别:{drecord.category}\n影像数量:{drecord.num}\n诊断结果:{drecord.num}"
        )
        for arecord in arecords:
            with open(arecord.rawimage, 'rb') as fd:
                zfile.writestr(f"{arecord.filename}/raw.png", fd.read())
            with open(arecord.annotationimage, 'rb') as fd:
                zfile.writestr(f"{arecord.filename}/annotationimage.png",
                               fd.read())
            zfile.writestr(
                f"{arecord.filename}/info.txt",
                f"文件:{arecord.filename}\n检查类别:{arecord.category}\n诊断:{arecord.diagnosis}\n"
            )
    buffer.seek(0)
    response = make_response(buffer.read())
    return response


# 详情页面总数据
@record_blue.route('/getRecordDetail')
@login_required
def getRecordDetail():
    print(request.args)
    drecordid = int(request.args["drecord"])
    arecords = ARecord.query.filter_by(drecordid=drecordid).all()
    res = []
    for arecord in arecords:
        res.append({
            "key": len(res),
            "arecordid": arecord.arecordid,
            "filename": arecord.filename,
            "category": arecord.category,
            "diagnosis": arecord.diagnosis
        })
    drecord = DRecord.query.filter_by(drecordid=drecordid).first()
    res = {
        "info": {
            "key": drecord.drecordid,
            "name": drecord.name,
            "description": drecord.description,
            "time": str(drecord.time),
            "category": drecord.category,
            "num": drecord.num,
            "diagnosis": drecord.diagnosis,
        },
        "arecords": res
    }
    print(res)
    return jsonify(res)


# 根据arecord查找并返回图片
@record_blue.route("/getImage", methods=["get"])
def getImage():
    arecordid = request.args["arecordid"]
    israw = request.args["israw"]
    print(israw, type(israw))
    arecord = ARecord.query.filter_by(arecordid=arecordid).first()
    imagePath = arecord.rawimage if israw == "true" else arecord.annotationimage
    print(israw, arecord.rawimage, arecord.annotationimage, imagePath)
    with open(imagePath, 'rb') as f:
        image = f.read()
        image = base64.b64encode(image)
        resp = Response(image, mimetype='image/png')
    return resp


@record_blue.route("/getIntroduction", methods=["get"])
def getIntroduction():
    return send_from_directory("images", "Winter.pdf", as_attachment=True)