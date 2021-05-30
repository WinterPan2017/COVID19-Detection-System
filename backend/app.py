'''
Description: Copyright © 1999 - 2020 Winter. All Rights Reserved. 
Author: Winter
Email: 837950571@qq.com
Date: 2021-03-31 16:44:32
LastEditTime: 2021-05-19 15:00:15
'''
from flask import Flask
import pymysql
from flask_cors import CORS

app = Flask(__name__)
# mysql密码 sudo cat /etc/mysql/debian.cnf

# 跨域访问
CORS(app)

#配置flask配置对象中键：SQLALCHEMY_DATABASE_URI
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://debian-sys-maint:eHEcwLTkDrI0qFNa@localhost/COVID19"

#配置flask配置对象中键：SQLALCHEMY_COMMIT_TEARDOWN,设置为True,应用会自动在每次请求结束后提交数据库中变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


from models import db, User, DRecord, ARecord
from detection import detection_blue
from record import record_blue
from login import login_blue

db.init_app(app)
app.register_blueprint(detection_blue)
app.register_blueprint(record_blue)
app.register_blueprint(login_blue)
app.app_context().push()


if __name__ == '__main__':
    db.drop_all(app=app)
    db.create_all(app=app)
    db.session.add(User(account="Winter", password="123456"))
    db.session.commit()
    # db.session.add(
    #     DRecord(userid=1,
    #             name="ct test1",
    #             description="this is a test for Normal",
    #             category="CT",
    #             num=1,
    #             diagnosis="Normal"))
    # db.session.add(
    #     DRecord(userid=1,
    #             name="ct test2",
    #             description="this is a test for COVID-19",
    #             category="CT",
    #             num=1,
    #             diagnosis="COVID-19"))
    # db.session.add(
    #     DRecord(userid=1,
    #             name="ct test3",
    #             description="this is a test for CAP",
    #             category="CT",
    #             num=20,
    #             diagnosis="CAP"))
    # db.session.add(
    #     DRecord(userid=1,
    #             name="x-ray test1",
    #             description="this is a test",
    #             category="CXR",
    #             num=1,
    #             diagnosis="COVID-19"))
    # db.session.add(
    #     DRecord(userid=1,
    #             name="x-ray test2",
    #             description="this is a test",
    #             category="CXR",
    #             num=1,
    #             diagnosis="Normal"))
    # db.session.commit()
    # db.session.add(
    #     ARecord(drecordid=1,
    #             filename="patient_Normal.dcm",
    #             category="CT",
    #             rawimage="./images/1/raw.png",
    #             annotationimage="./images/1/processed.png",
    #             diagnosis="Normal"))
    # db.session.add(
    #     ARecord(drecordid=2,
    #             filename=f"patient_001_1.dcm",
    #             category="CT",
    #             rawimage="./images/2/raw.png",
    #             annotationimage="./images/2/processed.png",
    #             diagnosis="COVID-19"))
    # db.session.add(
    #     ARecord(drecordid=2,
    #             filename=f"patient_001_2.dcm",
    #             category="CT",
    #             rawimage="./images/2/raw.png",
    #             annotationimage="./images/2/processed.png",
    #             diagnosis="COVID-19"))
    # db.session.add(
    #     ARecord(drecordid=4,
    #             filename="cxr_021.png",
    #             category="CXR",
    #             rawimage="./images/4/raw.png",
    #             annotationimage="./images/4/processed.png",
    #             diagnosis="COVID-19"))
    # db.session.commit()
    app.run(debug=True)
