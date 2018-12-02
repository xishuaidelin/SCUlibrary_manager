# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base

from application import db

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    title = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.String(280), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    location = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
