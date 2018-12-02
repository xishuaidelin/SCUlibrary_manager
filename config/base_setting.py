SERVER_PORT=8999
#因为bug原因先调为true
DEBUG=True
SQLALCHEMY_ECHO=False

PAGE_SIZE = 10
PAGE_DISPLAY = 10

APP_MAKER='大川图书'

STATUS_MAPPING = {
    "1":"正常",
    "0":"已删除"
}
LOST_MAPPING={
    "1":"拾到",
    "0":"丢失"
}

BOOK_TYPES={
    "1":"文学",
    "2":"历史",
    "3":"理工",
    "4":"医学",
    "0":"其他"
}

LENDING_STATUS={
    "1":"在借",
    "0":"已还"

}

ORDER={
    "1":"顺序",
    "2":"倒序"

}

LIB_LOCATION={
    "1":"江安图书馆",
    "2":"望江工学馆",
    "3":"望江文理馆",
    "4":"华西医学馆"
}

UPLOAD = {
    'ext':[ 'jpg','gif','bmp','jpeg','png' ],#允许上传的图片类型的后缀
    'prefix_path':'/web/static/images/upload/', #图片 存放的前缀地址
    'prefix_url':'/static/images/upload/' #图片展示前缀，用于获取图片的地址
}

APP = {
    'domain':'http://localhost:8999'  #自己域名配置 ，这里因为是本地访问就配置的是本地访问端口的网址
}

AUTH_COOKIE_NAME="library"

#本来是local里面的东西，现在为了将warning先去掉暂时将这个作为默认设置
SQLALCHEMY_DATABASE_URI='mysql://root:@127.0.0.1:3306/manager?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS=False



"""过滤URL"""
IGNORE_URLS=[
    "/user/login"
]
IGNORE_CHECK_LOGIN_URLS=[
    "/static",
    "/favicon.ico"

]