from flask import Blueprint,request,jsonify,redirect
from application import app,db
from sqlalchemy import  or_
from common.model.books_lib.books import Books
from common.lib.Helper import ops_render,getCurrentDate,iPagination
from common.lib.UrlManager import UrlManager

route_books_lib=Blueprint('books_lib_page',__name__)

@route_books_lib.route("/index")
def list():
    resp_data = {}
    query = Books.query
    query.count()  # 这个就是取得总的页数
    req = request.values
    lib_location=app.config['LIB_LOCATION']
    page = int(req['p']) if ('p' in req and req['p']) else 1

    #将字符类型的book_type转换为int类型


    if 'mix_kw' in req:
        rule = or_(Books.title.ilike("%{0}%".format(req['mix_kw'])),
                   Books.author.ilike("%{0}%".format(req['mix_kw'])))
        query = query.filter(rule)

    if 'status' in req and int(req['status']) > -1:
        query = query.filter(Books.status == int(req['status']))

    if 'cat' in req and int(req['cat']) > -1:
        query = query.filter(Books.book_type == int(req['cat']))

    if 'location' in req and int(req['location']) > -1:
        query = query.filter(Books.location==lib_location[req['location']])

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

    list = query.order_by(Books.id.asc()).all()[offset:limit]

    #将int类型book_type转换为str类型
    books_type = app.config['BOOK_TYPES']
    for item in list:
        type_int=item.book_type
        type=str(type_int)
        type_str=books_type[type]
        item.book_type=type_str

    resp_data['list'] = list
    resp_data['pages'] = pages
    resp_data['search_con'] = req
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']
    resp_data['book_types'] = app.config['BOOK_TYPES']
    resp_data['lib_location'] = app.config['LIB_LOCATION']


    #return ops_render("books_lib/index.html",{"current":"Academic_communication"})
    return ops_render("books_lib/index.html",resp_data)



@route_books_lib.route("/info")
def info():
    resp_data = {}
    req = request.args
    id = int(req.get("id", 0))
    reback_url = UrlManager.buildUrl("/books_lib/index")

    if id < 1:
        return redirect(reback_url)

    book_info = Books.query.filter_by(id=id).first()
    if not book_info:
        return redirect(reback_url)

    # 转换book_type
    books_type = app.config['BOOK_TYPES']
    type_int = book_info.book_type
    type = str(type_int)
    type_str = books_type[type]
    book_info.book_type = type_str

    resp_data['book_info'] = book_info
    # resp_data['news_info'] = news_info


    return ops_render("books_lib/info.html",resp_data)

@route_books_lib.route("/set")
def item_set():
    return ops_render("books_lib/set.html")

@route_books_lib.route("/new_set",methods=['GET','POST'])#可以集成修改和新建的功能
def new_set():
    if request.method == "GET":
        resp_data = {}
        req = request.args
        id = int( req.get('id',0) )
        info = Books.query.filter_by( id = id ).first()
        if info and info.status != 1:
            return redirect( UrlManager.buildUrl("/books_lib/index") )
        resp_data['info'] = info
        resp_data['lib_location'] = app.config['LIB_LOCATION']
        resp_data['book_types'] = app.config['BOOK_TYPES']
        return ops_render("books_lib/new_set.html", resp_data)

    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    id = int(req['id']) if 'id' in req and req['id'] else 0
    cat_id = int(req['cat_id']) if 'cat_id' in req and req['cat_id'] else 0
    title = req['title'] if 'title' in req else ''
    author = req['author'] if 'author' in req else ''
    press = req['press'] if 'press' in req else ''
    intro = req['intro'] if 'intro' in req else ''
    location = req['location'] if 'location' in req else ''
    amount = int(req['amount']) if 'amount' in req and req['amount'] else 0
    image = req['image'] if 'image' in req else ''

    if image is None or len(image) < 3:
        resp['code'] = -1
        resp['msg'] = "请上传封面图~~"
        return jsonify(resp)

    book_info = Books.query.filter_by(id=id).first()
    if book_info:
        model_info = book_info
        model_info.current_amount = amount  # 现在的数量，只有修改已有书籍的时候的才能修改
    else: #这里铁定的是第一次上新才能修改
        model_info = Books()
        model_info.status = 1
        model_info.current_amount = amount  #第一次上新在馆数量和上新数量是一样的
        model_info.update_amount = amount   #上新数量，只能 第一次 上新书才能更改,不允许出错，因为涉及到新书推荐的地方
        model_info.update_time = getCurrentDate()  #上新时间，只能第一次上新才能更改

    # 这6个均可修改的原因是有可能第一次上新的时候输错了书籍信息

    model_info.book_type = cat_id
    model_info.title = title
    model_info.author = author
    model_info.image = image
    model_info.press = press
    model_info.intro = intro
    model_info.location = location

    db.session.add(model_info)
    db.session.commit()

    return jsonify(resp)



@route_books_lib.route("/ops",methods = [ "POST" ])
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

    book_info = Books.query.filter_by(id=id).first()
    if not book_info:
        resp['code'] = -1
        resp['msg'] = "指定讲座不存在~~"
        return jsonify(resp)

    if act == "remove":
        book_info.status = 0
    elif act == "recover":
        book_info.status = 1

    db.session.add(book_info)
    db.session.commit()
    return jsonify(resp)
