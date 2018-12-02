# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from application import db

class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False, server_default=db.FetchedValue())
    author = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    press = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    intro = db.Column(db.String(300), nullable=False, server_default=db.FetchedValue())
    book_type = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    update_amount = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    image = db.Column(db.String(200), nullable=False, server_default=db.FetchedValue())
    location = db.Column(db.String(20), nullable=False, server_default=db.FetchedValue())
    current_amount = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
