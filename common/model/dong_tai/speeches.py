# coding: utf-8
from application import db

class Speeches(db.Model):
    __tablename__ = 'speeches'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    teacher = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    teacher_conn = db.Column(db.String(50), nullable=False, server_default=db.FetchedValue())
    speech_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    address = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    speech_intro = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    teacher_intro = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    amount = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
