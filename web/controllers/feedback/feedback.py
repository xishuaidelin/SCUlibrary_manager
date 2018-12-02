from flask import Blueprint,request,jsonify,redirect
from application import app,db
from sqlalchemy import  or_
from common.model.feedback.feedback import Feedback
from common.model.feedback.contribution import Contribution
from common.lib.Helper import ops_render,getCurrentDate,iPagination
from common.lib.UrlManager import UrlManager

route_feedback=Blueprint('feedback_page',__name__)

@route_feedback.route("/index")
def index():
    resp_data = {}
    query = Contribution.query
    query.count()  # 这个就是取得总的页数
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }
    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    if 'status' in req and int(req['status']) > -1:  # 顺序为1，倒序为2
        if int(req['status']) == 1:
            list = query.order_by(Contribution.created_time.asc()).all()[offset:limit]
        else:
            list = query.order_by(Contribution.created_time.desc()).all()[offset:limit]
    else:
        list = query.order_by(Contribution.id.asc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['order'] = app.config['ORDER']
    resp_data['current'] = 'index'

    return ops_render("feedback/index.html",resp_data)

@route_feedback.route("/feedback")
def feedback():

    resp_data = {}
    query = Feedback.query
    query.count()  # 这个就是取得总的页数
    req = request.values
    lib_location = app.config['LIB_LOCATION']
    page = int(req['p']) if ('p' in req and req['p']) else 1

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Feedback.status == int(req['status']))

    if 'location' in req and int(req['location']) > -1:
        query = query.filter(Feedback.location == lib_location[req['location']])

    page_params = {
        'total': query.count(),
        'page_size': app.config['PAGE_SIZE'],
        'page': page,
        'display': app.config['PAGE_DISPLAY'],
        'url': request.full_path.replace("&p={}".format(page), "")
    }
    pages = iPagination(page_params)
    offset = (page - 1) * app.config['PAGE_SIZE']
    limit = app.config['PAGE_SIZE'] * page

    list = query.order_by(Feedback.id.asc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['lib_location'] = app.config['LIB_LOCATION']
    resp_data['current'] = 'feedback'

    return ops_render("feedback/feedback.html", resp_data)


@route_feedback.route("/feed_info",methods=['GET','POST'])
def info():
    if request.method=='GET':
        resp_data = {}
        req = request.args
        id = int(req.get("id", 0))
        reback_url = UrlManager.buildUrl("/feedback/feedback")

        if id < 1:
            return redirect(reback_url)

        feed_info = Feedback.query.filter_by(id=id).first()
        if not feed_info:
            return redirect(reback_url)

        resp_data['feed_info'] = feed_info
        # resp_data['news_info'] = news_info
        return ops_render("feedback/feed_info.html",resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0
    feedback_lib = req['feedback'] if 'feedback' in req else ''

    app.logger.info(feedback_lib)

    if id ==0:
        resp['code'] = -1
        resp['msg'] = "数据的id获取失败~~"
        return jsonify(resp)

    if feedback_lib is None or len(feedback_lib) < 2:
        resp['code'] = -1
        resp['msg'] = "请填写规范的回复~~"
        return jsonify(resp)

    model_info = Feedback.query.filter_by(id=id).first()


    model_info.feedback_lib = feedback_lib


    db.session.add(model_info)
    db.session.commit()

    return jsonify(resp)



@route_feedback.route("/gao_info",methods=['GET','POST'])
def gao_info():
    if request.method=='GET':
        resp_data = {}
        req = request.args
        id = int(req.get("id", 0))
        reback_url = UrlManager.buildUrl("/feedback/index")

        if id < 1:
            return redirect(reback_url)

        gao_info = Contribution.query.filter_by(id=id).first()
        if not gao_info:
            return redirect(reback_url)

        resp_data['gao_info'] = gao_info

        return ops_render("feedback/gao_info.html",resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0
    feedback_lib = req['feedback'] if 'feedback' in req else ''


    if id ==0:
        resp['code'] = -1
        resp['msg'] = "数据的id获取失败~~"
        return jsonify(resp)

    if feedback_lib is None or len(feedback_lib) < 2:
        resp['code'] = -1
        resp['msg'] = "请填写规范的回复~~"
        return jsonify(resp)

    model_info = Contribution.query.filter_by(id=id).first()


    model_info.feedback_lib = feedback_lib


    db.session.add(model_info)
    db.session.commit()

    return jsonify(resp)

@route_feedback.route("/ops",methods = [ "POST" ])
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

    book_info = Feedback.query.filter_by(id=id).first()
    if not book_info:
        resp['code'] = -1
        resp['msg'] = "指定对象不存在~~"
        return jsonify(resp)

    if act == "remove":
        book_info.status = 0
    elif act == "recover":
        book_info.status = 1

    db.session.add(book_info)
    db.session.commit()
    return jsonify(resp)