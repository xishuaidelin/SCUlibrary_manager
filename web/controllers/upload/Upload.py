# -*- coding: utf-8 -*-
from flask import Blueprint,request,jsonify
from application import  app
import re,json
from common.model.images_test import Image
from common.lib.UploadService import UploadService
from common.lib.UrlManager import UrlManager

route_upload = Blueprint('upload_page', __name__)

'''
参考文章：https://segmentfault.com/a/1190000002429055
'''

@route_upload.route("/ueditor",methods = [ "GET","POST" ])
def ueditor():

	req = request.values
	action = req['action'] if 'action' in req else ''

	if action == "config":
		root_path = app.root_path
		config_path = "{0}/web/static/plugins/ueditor/upload_config.json".format( root_path )
		with open( config_path,encoding="utf-8" ) as fp:
			try:
				config_data =  json.loads( re.sub( r'\/\*.*\*/' ,'',fp.read() ) )
			except:
				config_data = {}
		return  jsonify( config_data )

	if action == "uploadimage":
		return uploadImage()

	if action == "listimage":
		return listImage()

	return "upload"

@route_upload.route("/pic",methods = [ "GET","POST" ])   #这个是上传封面图采用的路径
def uploadPic():     #点击上传图片就会调用这个方法，由于方法里面有UploadService.uploadByFile(upfile)就会直接图片存进服务器同时会将路径加到到数据库中
	file_target = request.files
	upfile = file_target['pic'] if 'pic' in file_target else None
	callback_target = 'window.parent.upload'  #这个东西和html里面的iframe相关，详情需要查看iframe的用法
	if upfile is None:
		return "<script type='text/javascript'>{0}.error('{1}')</script>".format( callback_target,"上传失败" )

	ret = UploadService.uploadByFile(upfile)
	if ret['code'] != 200:
		return "<script type='text/javascript'>{0}.error('{1}')</script>".format(callback_target, "上传失败：" + ret['msg'])

	return "<script type='text/javascript'>{0}.success('{1}')</script>".format(callback_target,ret['data']['file_key'] )

def uploadImage():
	resp = { 'state':'SUCCESS','url':'','title':'','original':'' }
	file_target = request.files
	upfile = file_target['upfile'] if 'upfile' in file_target else None
	if upfile is None:
		resp['state'] = "上传失败"
		return jsonify(resp)

	ret = UploadService.uploadByFile( upfile )
	if ret['code'] != 200:  #根据UploadService.uploadByFile方法里面返回的code值进行判断，如果不是200就说明这个文件类型不合格
		resp['state'] = "上传失败：" + ret['msg']
		return jsonify(resp)
    #如果没有出现失败的情况，就说明 成功了，然后点返回一个图片上传存放的地址回去
	resp['url'] = UrlManager.buildImageUrl( ret['data']['file_key'] )#这里在UrlManager.buildImageUrl进行了图片展示地址的拼接
	return jsonify( resp )

def listImage():     #从数据库里面取数据进行 展示，服务于在线管理那个里面，里面的start和id的结合是为了进行图片页面分类
	resp = { 'state':'SUCCESS','list':[],'start':0 ,'total':0 }

	req = request.values

	start = int( req['start']) if 'start' in req else 0
	page_size = int( req['size']) if 'size' in req else 20

	query = Image.query
	if start > 0:
		query = query.filter( Image.id < start )

	list = query.order_by( Image.id.desc() ).limit( page_size ).all()
	images = []

	if list:
		for item in list: #取出数据，是将数据库中的地址挨个放进一个列表里面
			images.append( { 'url': UrlManager.buildImageUrl( item.file_key ) } )
			start = item.id
	resp['list'] = images
	resp['start'] = start
	resp['total'] = len( images )
	return jsonify( resp )


