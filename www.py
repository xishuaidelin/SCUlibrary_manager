from application import app

"""统一拦截器：用于没登录无法进入主页面"""
from web.interceptors.AuthInterceptor import *


"""蓝图功能，对所有的url进行蓝图功能配置"""


from web.controllers.index import route_index
from web.controllers.user.user import route_user
from web.controllers.dong_tai.dong_tai import route_dong_tai
from web.controllers.books_lib.books_lib import route_books_lib
from web.controllers.feedback.feedback import route_feedback
from web.controllers.member.member import route_member
from web.controllers.static import route_static
from web.controllers.stat.stat import route_stat
from web.controllers.chart import route_chart
from web.controllers.upload.Upload import route_upload

app.register_blueprint( route_upload,url_prefix = "/upload" )
app.register_blueprint( route_index,url_prefix="/")
app.register_blueprint( route_user,url_prefix="/user")
app.register_blueprint( route_dong_tai,url_prefix="/dong_tai")
app.register_blueprint( route_books_lib,url_prefix="/books_lib")
app.register_blueprint( route_feedback,url_prefix="/feedback")
app.register_blueprint( route_member,url_prefix="/member")
app.register_blueprint( route_static,url_prefix="/static")
app.register_blueprint( route_stat,url_prefix="/stat")
app.register_blueprint( route_chart,url_prefix="/chart")