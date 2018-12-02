# -*- coding: utf-8 -*-
from application import app
class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl( path ):
        return path

    @staticmethod
    def buildStaticUrl(path):
        ver = "%s"%( 22222222 )
        path =  "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl( path )

    @staticmethod
    def buildImageUrl(  path ):   #拼接图片用以展示的地址
        app_config = app.config['APP']
        #url= 域名+图片前缀地址+ key
        url = app_config['domain'] + app.config['UPLOAD']['prefix_url'] + path
        return url