from flask import Blueprint,request,jsonify,redirect
from common.lib.Helper import ops_render,getCurrentDate,iPagination
from common.lib.UrlManager import UrlManager
from application import app,db
from common.model.bulletin_lost.news import News
from common.model.bulletin_lost.lost import Lost
from sqlalchemy import  or_

route_index = Blueprint('index_page',__name__)

@route_index.route("/")
def index():

    resp_data = {}
    query = News.query
    query.count()#这个就是取得总的页数
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    if 'mix_kw' in req:
        rule = or_(News.title.ilike("%{0}%".format(req['mix_kw'])), News.id.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(News.status == int(req['status']))

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

    list = query.order_by(News.id.asc()).all()[ offset:limit ]

    resp_data['list'] = list
    resp_data['pages']=pages
    resp_data['current']='bulletin'
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("index/index.html",resp_data)

@route_index.route("/lost")
def lost():
    resp_data = {}
    query = Lost.query
    query.count()  # 这个就是取得总的页数
    req = request.values
    page = int(req['p']) if ('p' in req and req['p']) else 1

    if 'mix_kw' in req:
        rule = or_(Lost.title.ilike("%{0}%".format(req['mix_kw'])), Lost.id.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Lost.cat == int(req['status']))

    if 'lost' in req and int(req['lost']) > -1:
        query = query.filter(Lost.status == int(req['lost']))

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

    list = query.order_by(Lost.id.asc()).all()[offset:limit]

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['current'] = 'lost'
    resp_data['search_con'] = req
    resp_data['lost_mapping'] = app.config['LOST_MAPPING']
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    return ops_render("index/lost.html",resp_data)

@route_index.route("/new_set",methods=["GET","POST"])
def new_set():
    if request.method == "GET":
        resp={}
        resp['lib_location']=app.config['LIB_LOCATION']
        return ops_render("index/new_set.html",resp)

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    title = req['title'] if 'title' in req else ''
    location = req['location'] if 'location' in req else ''
    content = req['content'] if 'content' in req else ''
    # 参数有效性的再次判断的 之前判断了title字数不能小于2，地点名不能少于5个字和content不能为空，这里就暂时鸡肋地随便判断下
    if title is None or len(title) > 20:
        resp['code'] = -1
        resp['msg'] = "请输入规范的标题名~~"
        return jsonify(resp)

    if location  is None or len(location) > 15:
        resp['code'] = -1
        resp['msg'] = "请输入规范的校区图书馆名~~"
        return jsonify(resp)

    bulletin=News()
    bulletin.title= title
    bulletin.content=content
    bulletin.location= location
    bulletin.created_time=getCurrentDate()
    # 数据库提交
    db.session.add(bulletin)
    db.session.commit()

    return jsonify(resp)


@route_index.route("/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = UrlManager.buildUrl("/")

    if id < 1:
        return redirect(reback_url)

    info = News.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

   # news_info = News.query.filter(News.id == id).order_by(News.id.asc()).all()

    resp_data['info'] = info
    #resp_data['news_info'] = news_info

    return ops_render("index/info.html", resp_data)

@route_index.route("/lost_info")
def lost_info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = UrlManager.buildUrl("/lost")

    if id < 1:
        return redirect(reback_url)

    info = Lost.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

   # news_info = News.query.filter(News.id == id).order_by(News.id.asc()).all()

    resp_data['info'] = info
    #resp_data['news_info'] = news_info

    return ops_render("index/lost_info.html", resp_data)




@route_index.route("/set",methods=["GET","POST"])
def set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = req['id'] if 'id' in req else ''
        reback_url = UrlManager.buildUrl("/")
        info = News.query.filter_by(id=id).first()
        if not info:
            return redirect(reback_url)

        # news_info = News.query.filter(News.id == id).order_by(News.id.asc()).all()

        resp_data['info'] = info
        resp_data['lib_location'] = app.config['LIB_LOCATION']
        return ops_render("index/set.html",resp_data)


    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req else 0
    title = req['title'] if 'title' in req else ''
    location = req['location'] if 'location' in req else ''
    content = req['content'] if 'content' in req else ''
    # 参数有效性的再次判断的 之前判断了title字数不能小于2，地点名不能少于5个字和content不能为空，这里就暂时鸡肋地随便判断下
    if title is None or len(title) > 20:
        resp['code'] = -1
        resp['msg'] = "请输入规范的标题名~~"
        return jsonify(resp)

    if location is None or len(location) > 15:
        resp['code'] = -1
        resp['msg'] = "请输入规范的校区图书馆名~~"
        return jsonify(resp)

    bulletin_info = News.query.filter_by(id=id).first()
    bulletin_info.title = title
    bulletin_info.content = content
    bulletin_info.location = location
    bulletin_info.created_time = getCurrentDate()
    # 数据库提交
    db.session.add(bulletin_info)
    db.session.commit()

    return jsonify(resp)


@route_index.route("/ops",methods = [ "POST" ])
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

    news_info = News.query.filter_by(id=id).first()
    if not news_info:
        resp['code'] = -1
        resp['msg'] = "指定对象不存在~~"
        return jsonify(resp)

    if act == "remove":
        news_info.status = 0
    elif act == "recover":
        news_info.status = 1

    news_info.created_time = getCurrentDate()
    db.session.add(news_info)
    db.session.commit()
    return jsonify(resp)



@route_index.route("/lost_ops",methods = [ "POST" ])
def lost_ops():
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

    lost_info = Lost.query.filter_by(id=id).first()
    if not lost_info:
        resp['code'] = -1
        resp['msg'] = "指定对象不存在~~"
        return jsonify(resp)

    if act == "remove":
        lost_info.status = 0
    elif act == "recover":
        lost_info.status = 1

    #lost_info.created_time = getCurrentDate()
    db.session.add(lost_info)
    db.session.commit()
    return jsonify(resp)
