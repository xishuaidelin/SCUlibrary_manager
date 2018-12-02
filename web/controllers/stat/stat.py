from flask import Blueprint,request
from common.lib.Helper import ops_render
from common.model.lending_lib.lending import Lending
from common.model.books_lib.books import Books
from application import app,db


route_stat = Blueprint( 'stat_page',__name__ )

@route_stat.route( "/index",methods=['POST','GET'] )
def index():
    if request.method=='GET':
        resp_data={}
        query=Lending.query
        lending_info=query.all()

        #app.logger.info(lending_info[0].title)
        #这段需要优化
        books_info= Books.query.all()
        for item in lending_info:
            for book in books_info:
                if item.title==book.title:
                    item.book_type=book.book_type
        #app.logger.info(lending_info[0].book_type)

        resp_data['current']='index'
        return ops_render("stat/index.html",resp_data)

@route_stat.route( "/speeches",methods=['POST','GET'] )
def speeches():
    if request.method=='GET':
        resp_data={}
        resp_data['current']='speeches'
        return ops_render("stat/speeches.html",resp_data)
