'''
Description: Copyright © 1999 - 2020 Winter. All Rights Reserved. 
Author: Winter
Email: 837950571@qq.com
Date: 2021-04-01 16:42:14
LastEditTime: 2021-05-08 16:54:12
'''
from flask import Blueprint, request
import time
import os
import cv2
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from detector import CXRDetector, CTDetector
from models import DRecord, ARecord, User, db
from auth import login_required

detection_blue = Blueprint('detection', __name__)


# 上传检测页面
@detection_blue.route('/upload', methods=["POST"])
@login_required
def upload():
    token = request.headers["token"]
    s = Serializer("SECRET_KEY")
    data = s.loads(token)
    userid = data["userid"]

    print(request.data, request.form)
    name = request.form["name"]
    description = request.form["description"]
    category = request.form["category"]
    files = request.files.getlist('files[]')
    for f in files:
        f.save(os.path.join("./images/temp", f.filename))

    start = time.time()
    valid = True
    # 检测
    try:
        if category == "CXR":
            diagnosis, rawimage, annotationimage = CXRDetector().detect(
                "./images/temp")
        else:
            diagnosis, slices = CTDetector().detect("./images/temp")
    except:
        print(category, "detect error")
        valid = False

    if valid and category == "CXR":
        print(category, diagnosis)
        dr = DRecord(userid=1,
                     name=name,
                     description=description,
                     category=category,
                     num=1,
                     diagnosis=diagnosis)
        db.session.add(dr)
        db.session.flush()

        ar = ARecord(drecordid=dr.drecordid,
                     filename=files[0].filename,
                     category=category,
                     rawimage="",
                     annotationimage="",
                     diagnosis=diagnosis)
        db.session.add(ar)
        db.session.flush()

        # 创建文件夹
        if not os.path.exists(f"./images/{ar.arecordid}"):
            os.mkdir(f"./images/{ar.arecordid}")
        raw_path = os.path.join(f"./images/{ar.arecordid}", "raw.png")
        cv2.imwrite(raw_path, rawimage)
        ar.rawimage = raw_path
        ar.annotationimage = raw_path
        if annotationimage is not None:
            cv2.imwrite(
                os.path.join(f"./images/{ar.arecordid}", "processed.png"),
                annotationimage)
            ar.annotationimage = os.path.join(f"./images/{ar.arecordid}",
                                              "processed.png")

        db.session.flush()
        db.session.commit()

    if valid and category == "CT":
        print(category, diagnosis)
        dr = DRecord(userid=1,
                     name=name,
                     description=description,
                     category=category,
                     num=len(slices),
                     diagnosis=diagnosis)
        db.session.add(dr)
        db.session.flush()
        for i in range(len(slices)):
            slice_diagnosis, rawimage, annotationimage = slices[i]
            ar = ARecord(drecordid=dr.drecordid,
                        filename=f"slice_{i}",
                        category=category,
                        rawimage="",
                        annotationimage="",
                        diagnosis=slice_diagnosis)
            db.session.add(ar)
            db.session.flush()

            # 创建文件夹
            if not os.path.exists(f"./images/{ar.arecordid}"):
                os.mkdir(f"./images/{ar.arecordid}")
            raw_path = os.path.join(f"./images/{ar.arecordid}", "raw.png")
            cv2.imwrite(raw_path, rawimage)
            ar.rawimage = raw_path
            ar.annotationimage = raw_path
            if annotationimage is not None:
                cv2.imwrite(
                    os.path.join(f"./images/{ar.arecordid}", "processed.png"),
                    annotationimage)
                ar.annotationimage = os.path.join(f"./images/{ar.arecordid}",
                                                "processed.png")

            db.session.flush()
        db.session.commit()

    for f in os.listdir("./images/temp"):
        os.remove(os.path.join("./images/temp", f))
    print("using time: ", time.time()- start)
    if valid:
        return 'success'
    return '文件不合法'