# coding: utf-8
from application import db

class Lost(db.Model):
    __tablename__ = 'lost'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    image = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    description = db.Column(db.String(100), nullable=False, server_default=db.FetchedValue())
    name = db.Column(db.String(40), nullable=False, server_default=db.FetchedValue())
    conn = db.Column(db.String(40), nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    cat = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    place = db.Column(db.String(40), nullable=False, server_default=db.FetchedValue())
