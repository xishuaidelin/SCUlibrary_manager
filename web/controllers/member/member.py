from flask import Blueprint,request,jsonify,redirect
from common.lib.Helper import ops_render,getCurrentDate,iPagination
from common.model.lending_lib.lending import Lending
from application import  app,db
from sqlalchemy import  or_,and_
from common.lib.UrlManager import UrlManager


route_member=Blueprint('member_page',__name__)

@route_member.route("/index")
def borrow():
    resp_data = {}
    query = Lending.query
    query.count()  # 这个就是取得总的页数
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1


    if 'mix_kw' in req:
        rule = or_(Lending.title.ilike("%{0}%".format(req['mix_kw'])),
                   Lending.lending_name.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Lending.status == int(req['status']))

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

    list = query.order_by(Lending.id.asc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['lending_status'] = app.config['LENDING_STATUS']
    resp_data['current'] = 'borrow'

    return ops_render("member/index.html",resp_data)


@route_member.route("/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = UrlManager.buildUrl("/member/index")

    if id < 1:
        return redirect(reback_url)

    lending_info = Lending.query.filter_by(id=id).first()
    if not lending_info:
        return redirect(reback_url)

    resp_data['lending_info'] = lending_info

    return ops_render("member/info.html",resp_data)


@route_member.route("/back")
def back():
    resp_data = {}
    query = Lending.query
    query.count()  # 这个就是取得总的页数
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

   # if 'mix_kw' in req:
    #     rule = or_(Lending.title.ilike("%{0}%".format(req['mix_kw'])),
    #              Lending.lending_name.ilike("%{0}%".format(req['mix_kw'])))
    #   query = query.filter(rule)

    #    if 'status' in req and int(req['status']) > -1:
    #   query = query.filter(Lending.status == int(req['status']))

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

    #这里进行条件查询，查询逾期未还的
    list = query.filter(Lending.status==1).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    #resp_data['search_con'] = req
    #resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['current'] = 'back'
    resp_data['cur_date'] = getCurrentDate()

    return ops_render("member/back.html",resp_data)


@route_member.route("/ops",methods = [ "POST" ])
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

    lending_info =Lending .query.filter_by(id=id).first()
    if not lending_info:
        resp['code'] = -1
        resp['msg'] = "指定信息不存在~~"
        return jsonify(resp)

    if act == "remove":
        lending_info.status = 0
    elif act == "recover":
        lending_info.status = 1

    db.session.add(lending_info)
    db.session.commit()
    return jsonify(resp)
