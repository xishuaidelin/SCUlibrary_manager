# coding: utf-8
from application import db


class SpeechReservation(db.Model):
    __tablename__ = 'speech_reservation'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    studentID = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    college = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    title = db.Column(db.String(60), nullable=False, server_default=db.FetchedValue())
    speech_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
