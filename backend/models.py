'''
Description: Copyright © 1999 - 2020 Winter. All Rights Reserved. 
Author: Winter
Email: 837950571@qq.com
Date: 2021-03-31 18:23:33
LastEditTime: 2021-04-01 16:53:56
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, LargeBinary
import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    userid = Column(Integer,
                    nullable=False,
                    primary_key=True,
                    autoincrement=True)
    account = Column(String(16), nullable=False, unique=True)
    password = Column(String(16), nullable=False, unique=False)
    isAdministrator = Column(Boolean, nullable=False, default=False)


class DRecord(db.Model):
    __tablename__ = "drecord"
    drecordid = Column(Integer,
                       nullable=False,
                       primary_key=True,
                       autoincrement=True)
    userid = Column(
        Integer,
        ForeignKey('user.userid'),
        nullable=False,
        unique=False,
    )
    name = Column(String(16), nullable=False, unique=False)
    description = Column(String(128), nullable=False, unique=False)
    time = Column(DateTime, nullable=False, default=datetime.datetime.now)
    category = Column(String(16), nullable=False)
    num = Column(Integer, nullable=False)
    diagnosis = Column(String(16), nullable=False)


class ARecord(db.Model):
    __tablename__ = "arecord"
    arecordid = Column(Integer,
                       nullable=False,
                       primary_key=True,
                       autoincrement=True)
    drecordid = Column(Integer,
                       ForeignKey('drecord.drecordid'),
                       nullable=False,
                       unique=False)
    filename = Column(String(128), nullable=False)
    category = Column(String(16), nullable=False)
    rawimage = Column(String(128), nullable=False)
    annotationimage = Column(String(128), nullable=False)
    diagnosis = Column(String(16), nullable=False)
