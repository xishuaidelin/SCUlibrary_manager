# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, String, Table
from application import db


class User(db.Model):
    __tablename__ = 'user'

    uid=db.Column('uid', db.BigInteger,primary_key=True)
    nickname=db.Column('nickname', db.String(100))
    email=db.Column('email', db.String(100))
    sex=db.Column('sex', db.Integer)
    avatar=db.Column('avatar', db.String(64))
    login_name=db.Column('login_name', db.String(32))
    login_pwd=db.Column('login_pwd', db.String(32))
    login_salt=db.Column('login_salt', db.String(32))
    status=db.Column('status', db.Integer)
    mobile=db.Column('mobile', db.String(20))

