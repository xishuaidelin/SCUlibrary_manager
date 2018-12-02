from flask import Blueprint,request,jsonify,redirect
from sqlalchemy import  or_
from common.lib.UrlManager import UrlManager
from common.model.dong_tai.speeches import Speeches
from common.model.dong_tai.speech_reservation import SpeechReservation
from application import db,app
from common.lib.Helper import ops_render,getCurrentDate,iPagination

route_dong_tai=Blueprint('dong_tai_page',__name__)
#这里的名字和功能对不上，但是先这样，因为改了容易出错这个页面
@route_dong_tai.route("/index")
def login():
    return ops_render("dong_tai/index.html",{"current":"Academic_communication"})

@route_dong_tai.route("/speeches")
def check_speeches():

    resp_data = {}
    query = Speeches.query
    query.count()#这个就是取得总的页数
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    if 'mix_kw' in req:
        rule = or_(Speeches.title.ilike("%{0}%".format(req['mix_kw'])), Speeches.id.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Speeches.status == int(req['status']))

    page_params = {
        'total': query.count(),
        'page_size':app.config['PAGE_SIZE'],
        'page': page,
        'display':app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace( "&p={}".format(page),"" )
    }
    pages = iPagination( page_params )
    offset = ( page - 1 ) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(Speeches.id.asc()).all()[ offset:limit ]

    #这里是想解决展示的编号问题，先放这里算了
    i=0
    li=[]
    while i<len(list):
        li.append(i)
        i=i+1

    resp_data['list'] = list
    resp_data['pages']=pages
    resp_data['sort']=li
    resp_data['current']='speeches_management'
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']

    return ops_render("dong_tai/speeches.html",resp_data)

@route_dong_tai.route("/speech_info")
def speech_info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = UrlManager.buildUrl("/dong_tai/speeches")

    if id < 1:
        return redirect(reback_url)

    speeches_info = Speeches.query.filter_by(id=id).first()
    if not speeches_info:
        return redirect(reback_url)

        # news_info = News.query.filter(News.id == id).order_by(News.id.asc()).all()
    title = speeches_info.title
    amount= SpeechReservation.query.filter(SpeechReservation.title==title).count()
    speeches_info.amount=amount
    resp_data['speeches_info'] = speeches_info
    # resp_data['news_info'] = news_info

    return ops_render("dong_tai/speech_info.html", resp_data)


@route_dong_tai.route("/set")
def resetPwd():
    return ops_render("dong_tai/set.html")

@route_dong_tai.route("/speech_edit",methods=["GET","POST"])
def speech_edit():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = req['id'] if 'id' in req else ''
        reback_url = UrlManager.buildUrl("/dong_tai/speeches")
        speech_info = Speeches.query.filter_by(id=id).first()
        if not speech_info:
            return redirect(reback_url)

        # news_info = News.query.filter(News.id == id).order_by(News.id.asc()).all()

        resp_data['info'] = speech_info
        return ops_render("dong_tai/speech_edit.html",resp_data)


    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    sid = int(req['id']) if 'id' in req else 0
    title = req['title'] if 'title' in req else ''
    address = req['address'] if 'address' in req else ''
    teacher = req['teacher'] if 'teacher' in req else ''
    email = req['email'] if 'email' in req else ''
    teacher_intro = req['teacher_intro'] if 'teacher_intro' in req else ''
    speech_intro = req['speech_intro'] if 'speech_intro' in req else ''
    time = req['time'] if 'time' in req else getCurrentDate()
    app.logger.info(time)
    #注意：
    #input datetime-local控件获取的日期格式是****-**-**T**:**:**，中间有个很奇怪的T，下面的这个函数已经的证明可以将其赋给数据库
    def deleteT(time):
        time1 = time[:10]
        time2 = time[11:]
        time = time1 + ' '+time2 + ':00'
        return time

    time = deleteT(time)
    app.logger.info(time)

    # 假吧意思判断两个，重点是判断时间到底对没对
    if title is None or len(title) > 20:
        resp['code'] = -1
        resp['msg'] = "请输入规范的标题名~~"
        return jsonify(resp)

    if address is None:
        resp['code'] = -1
        resp['msg'] = "请输入规范的讲座地址~~"
        return jsonify(resp)

    speech_info = Speeches.query.filter_by(id=sid).first()
    speech_info.title = title
    speech_info.address = address
    speech_info.teacher = teacher
    speech_info.teacher_conn = email
    speech_info.speech_time = time
    speech_info.teacher_intro = teacher_intro
    speech_info.speech_intro = speech_intro
    # 数据库提交
    db.session.add(speech_info)
    db.session.commit()

    return jsonify(resp)




@route_dong_tai.route("/new_set")
def set():
    return ops_render("dong_tai/new_set.html")

@route_dong_tai.route("/new_speech",methods=["GET","POST"])
def new_speech():
    if request.method == "GET":
        return ops_render("dong_tai/new_speech.html")
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    title = req['title'] if 'title' in req else ''
    address = req['address'] if 'address' in req else ''
    teacher = req['teacher'] if 'teacher' in req else ''
    email = req['email'] if 'email' in req else ''
    teacher_intro = req['teacher_intro'] if 'teacher_intro' in req else ''
    speech_intro = req['speech_intro'] if 'speech_intro' in req else ''
    app.logger.info(req['time'])
    app.logger.info(getCurrentDate())
    time = req['time'] if 'time' in req else getCurrentDate()
    app.logger.info(time)

    # 注意：
    # input datetime-local控件获取的日期格式是****-**-**T**:**:**，中间有个很奇怪的T，下面的这个函数已经的证明可以将其赋给数据库
    #这里和上一个函数原理不同
    def deleteT(time):
        time1=time[:4]
        time2=time[5:7]
        time3=time[8:10]
        time4 = time[11:13]
        time5 = time[14:]
        time =time1+time2+time3+time4+time5+'00'
        time=int(time)
        return time
    time=deleteT(time)
    app.logger.info(time)
   #假吧意思判断两个
    if title is None or len(title) > 20:
        resp['code'] = -1
        resp['msg'] = "请输入规范的标题名~~"
        return jsonify(resp)

    if address is None or len(address) > 15:
        resp['code'] = -1
        resp['msg'] = "请输入规范的讲座地址~~"
        return jsonify(resp)

    speech = Speeches()
    speech.title = title
    speech.address = address
    speech.teacher = teacher
    speech.teacher_conn = email
    speech.speech_time = time
    speech.teacher_intro = teacher_intro
    speech.speech_intro = speech_intro

    # 数据库提交
    db.session.add(speech)
    db.session.commit()

    return jsonify(resp)
@route_dong_tai.route("/ops",methods = [ "POST" ])
def ops():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values

    id = int(req['id']) if 'id' in req else 0
    act = req['act'] if 'act' in req else ''
    if not id :
        resp['code'] = -1
        resp['msg'] = "请选择要操作的对象~~"
        return jsonify(resp)

    if  act not in [ 'remove','recover' ] :
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    speech_info = Speeches.query.filter_by(id=id).first()
    if not speech_info:
        resp['code'] = -1
        resp['msg'] = "指定讲座不存在~~"
        return jsonify(resp)

    if act == "remove":
        speech_info.status = 0
    elif act == "recover":
        speech_info.status = 1

    db.session.add(speech_info)
    db.session.commit()
    return jsonify(resp)

