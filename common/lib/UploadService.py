# -*- coding: utf-8 -*-
from werkzeug.utils import secure_filename
from application import app,db
from common.lib.Helper import getCurrentDate
from common.model.images_test import Image
import datetime
import  os,stat,uuid

class UploadService():
	@staticmethod
	def uploadByFile( file ):     #保存到服务器目录的同时将路径的存储到数据库中
		config_upload = app.config['UPLOAD']
		resp = { 'code':200,'msg':'操作成功~~','data':{} }
		filename = secure_filename( file.filename ) #获取文件名，这个引入的方法可以获取安全的文件名
		app.logger.info(filename)#排除不能上传时文件名的问题
		ext = filename.split(".",1)[1]   #获取扩展文件的扩展名，通过切割.来进行获取。0代表前面的文件名，1代表后面的扩展
		if ext not in config_upload['ext']:   #判断是否是我们定义的文件类型，根据文件的扩展名进行判断
			resp['code'] = -1
			resp['msg'] = "不允许的扩展类型文件"
			return resp


		root_path = app.root_path + config_upload['prefix_path'] #定义存放路径，app.root_path是app下面的一个方法
		#不使用getCurrentDate创建目录，为了保证其他写的可以用，这里改掉，服务器上好像对时间不兼容
		file_dir = datetime.datetime.now().strftime("%Y%m%d")#生成文件，这里是按照时间生成文件
		save_dir = root_path + file_dir       #图片存放路径
		if not os.path.exists( save_dir ):   #查看这个文件路径是不是存在
			os.mkdir( save_dir )              #如果不存在就创建一个
			os.chmod( save_dir,stat.S_IRWXU | stat.S_IRGRP |  stat.S_IRWXO )  #选择这个目录的操作权限，直接网上查

		file_name = str( uuid.uuid4() ).replace("-","") + "." + ext    #拼接文件名，uuid是根据硬件和时间生成唯一的一个字符串
		file.save( "{0}/{1}".format( save_dir,file_name ) )#将这个文件完整的存放起来，路径加文件名就可以存放

		model_image = Image()
		model_image.file_key = file_dir + "/" + file_name   #这里存的只是从日期文件目录那里开始的文件路径，并不是完全的全部路径
		#model_image.file_key = save_dir + "/" + file_name    #这里存的是完全的路径：就是C:\pytest\appconstruction/web/static/这种的。
		model_image.created_time = getCurrentDate()
		db.session.add( model_image)#
		db.session.commit()

		resp['data'] = {
			'file_key':  model_image.file_key   #file_key就是日期加上文件名  ,这里的值model_image.file_key可以替换为save_dir + "/" + file_name
		}
		return resp