# coding: utf-8
from application import db

class Contribution(db.Model):
    __tablename__ = 'contribution'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    content = db.Column(db.String(280), nullable=False, server_default=db.FetchedValue())
    wx_name = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    feedback_lib = db.Column(db.String(280), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
