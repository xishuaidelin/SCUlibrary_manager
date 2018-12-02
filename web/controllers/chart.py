#主要统一进行画图数据后台请求
from flask import Blueprint,jsonify
from application import app
from common.model.dong_tai.speech_reservation import SpeechReservation
from common.model.lending_lib.lending import Lending
from common.model.books_lib.books import Books


route_chart=Blueprint('chart_page',__name__)


@route_chart.route("/speeches")
def speech():
    reservation= SpeechReservation.query.filter(SpeechReservation.status==1).all()
   # list = StatDailySite.query.filter(StatDailySite.date >= date_from) \
    #    .filter(StatDailySite.date <= date_to).order_by(StatDailySite.id.asc()) \
     #   .all()
    title=[]
    amount=[]
    def clear(reservation):
        i=0
        while i < (len(reservation))-1:
            if reservation[i].title==reservation[i+1].title:
                del(reservation[i])
                continue
            i=i+1
        return reservation
    reservation_cleared=clear(reservation)#已经将title正确地取出来了的
    app.logger.info(reservation_cleared)
    app.logger.info(reservation_cleared[0].title)
    app.logger.info(reservation_cleared[1].title)
    app.logger.info(reservation_cleared[2].title)
    for item in reservation_cleared:
        title.append(item.title)
        count=SpeechReservation.query.filter(SpeechReservation.title==item.title).count()
        amount.append(count)
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    data = {
        "categories": title,
        "series": [
            {
                "name": "预约人数",
                "data": amount
            }
        ]
    }

    resp['data'] = data
    return jsonify(resp)

@route_chart.route("/Pie")
def pie():
    total=Lending.query.count()
    books_type=app.config['BOOK_TYPES']
    types_count={'文学':0,'历史':0,'理工':0,'医学':0,'其他':0}
    #通过Books的数据去判断这个书籍是什么类型
    lending=Lending.query.all()
    title=[]
    def clear(lending):
        i=0
        while i < (len(lending))-1:
            if lending[i].title==lending[i+1].title:
                del(lending[i])
                continue
            i=i+1
        return lending
    lending_cleared=clear(lending)
    amount=[]
    for item in lending_cleared:
        title.append(item.title)
        count=Lending.query.filter(Lending.title==item.title).count()
        amount.append(count)
    #转换类型这里其实和books_lib里面的转换一模一样
    for i,item in enumerate(title):
        B=Books.query.filter(Books.title==item).first()
        t=B.book_type#这个是数字化的书籍类型
        t = str(t)
        type=books_type[t]
        app.logger.info("转换出来的书籍type:",type)
        types_count[type]=types_count[type]+amount[i]
        app.logger.info(types_count[type])

    app.logger.info('最后验证下每个部分对应的借书数量：')
    app.logger.info(types_count['文学'])
    app.logger.info(types_count['历史'])
    app.logger.info(types_count['理工'])
    app.logger.info(types_count['医学'])
    #成功
    for item in types_count:
        types_count[item]=types_count[item]/total

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    data = {
        "series": [
            {
                "name": "文学",
                "y":types_count['文学']
            },
            {
                "name": "历史",
                "y": types_count['历史']
            },
            {
                "name": "理工",
                "y": types_count['理工']
            },
            {
                "name": "医学",
                "y": types_count['医学']
            },
            {
                "name": "其他",
                "y": types_count['其他']
            }

        ]
    }

    resp['data'] = data
    return jsonify(resp)