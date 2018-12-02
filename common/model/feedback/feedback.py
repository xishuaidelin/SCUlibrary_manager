# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db

class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    description = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    advice = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    location = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    wx_name = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    feedback_lib = db.Column(db.String(280), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
