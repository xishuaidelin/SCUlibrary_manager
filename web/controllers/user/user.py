from flask import Blueprint,request,jsonify,make_response,redirect,g
import json
from common.model.user import User
from common.lib.user.UserService import UserService
from common.lib.Helper import ops_render
from application import app,db
from common.lib.UrlManager import UrlManager

route_user=Blueprint('user_page',__name__)

@route_user.route("/login",methods=["GET","POST"])
def login():
    if request.method =="GET":
        resp_data={}
        config=app.config['APP_MAKER']
        resp_data['config']=config
        return ops_render("user/login.html",resp_data)

    resp={'code':200,'msg':'登录成功','data':{}}
    #这里是获取输入的东西
    req=request.values
    login_name=req['login_name'] if 'login_name' in req else''
    login_pwd=req['login_pwd'] if 'login_pwd' in req else''

    #测试是否获得输入值，如果有没输入的就直接返回错误
    #return "%s-%s" %(login_name,login_pwd)测试成功
    if login_name is None or len(login_name)<1:
        resp['code']=-1
        resp['msg']= "请输入正确的登录用户名"
        return jsonify(resp)

    if login_pwd is None or len(login_pwd)<1:
        resp['code']=-1
        resp['msg']= "请输入正确的登录密码"
        return jsonify(resp)

    user_info=User.query.filter_by( login_name=login_name ).first()  #查询匹配的方法
    #确认输入的账户是在数据库中存在的
    if not user_info:
        resp['code'] = -1
        resp['msg'] = "请输入正确的登录用户名和密码-1"
        return jsonify(resp)
    #确认密码对的上账户
    #这里是将数据库中的密码（这个密码就是经过MD5与秘钥进行加密过的，不可逆加密） 与 输入的密码通过数据库中的秘钥进行加密得出的密码 进行比对
    #由于数据库中的密码并没有进行加密操作，所以这里的比对先直接进行明文比对
    #if user_info.login_pwd != UserService.genePwd(login_pwd,user_info.login_salt):
    if user_info.login_pwd != login_pwd:
         resp['code'] = -1
         resp['msg'] = "请输入正确的登录用户名和密码-2 "
         return jsonify(resp)

    response=make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'],'%s#%s' % (UserService.geneAuthCode(user_info),user_info.uid),60*60*24*120)#保存120天
    return response


@route_user.route("/edit",methods=["GET","POST"])
def edit():
    if request.method=="GET":
        return ops_render("user/edit.html",{"current":"edit"})

    resp={'code':200,'msg':'操作 成功','data':{}}
    req=request.values
    nickname=req['nickname'] if 'nickname' in req else ''
    email = req['email'] if 'email' in req else ''

    if nickname is None or len(nickname) < 1:
        resp['code']=-1
        resp['msg']="请输入符合规范的姓名"
        return jsonify(resp)
    if email is None or len(email) < 1:
        resp['code']=-1
        resp['msg']="请输入符合规范的邮箱"
        return jsonify(resp)

    user_info=g.current_user
    user_info.nickname=nickname
    user_info.email=email

    app.logger.info(user_info)

    db.session.add(user_info)
    db.session.commit()
    return jsonify(resp)

@route_user.route("/reset-pwd",methods=["GET","POST"])
def reset_Pwd():
    if request.method == "GET":
        return ops_render("user/reset_pwd.html",{"current":"reset_pwd"})

    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    old_password = req['old_password'] if 'old_password' in req else ''
    new_password = req['new_password'] if 'new_password' in req else ''
    #参数有效性的再次判断的
    if old_password is None or len( old_password ) < 6:
        resp['code']=-1
        resp['msg']="请输入符合规范的原始密码~~"
        return jsonify(resp)

    if new_password is None or len(new_password) < 6:
        resp['code'] = -1
        resp['msg'] = "请输入符合规范的新密码~~"
        return jsonify(resp)

    if old_password==new_password:
        resp['code'] = -1
        resp['msg'] = "请重新输入新密码，新密码不能和原密码相同~~"
        return jsonify(resp)

    user_info=g.current_user
    #更改这里的时候不是简单地更改，需要使用封装的办法进行加密保存更改
    #user_info.login_pwd=UserService.genePwd(new_password,user_info.login_salt)使用新密码和这个人本来加密随机字符串进行保存加密
    #这里为了后面的简单比对并没有进行加密保存，需要注意
    user_info.login_pwd =new_password
    #数据库提交
    db.session.add(user_info)
    db.session.commit()
    #更新cookie值
    response = make_response(json.dumps(resp))
    response.set_cookie(app.config['AUTH_COOKIE_NAME'], '%s#%s' % (UserService.geneAuthCode(user_info), user_info.uid),
                        60 * 60 * 24 * 120)  # 保存120天
    return response




@route_user.route("/logout")
def logout():
    response = make_response(redirect(UrlManager.buildUrl("/user/login")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response