import hashlib,base64

class UserService():
    #这里genePwd是将输入的密码和秘钥进行加密的，由于数据库中的密码目前并没有加密，所以这个方法暂时不用，待两边加密都搞好后再启用这个方法

    @staticmethod
    def genePwd(pwd,salt):
        m=hashlib.md5()
        str="%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt )
        m.update(str.encode("utf-8"))
        return m.hexdigest()
    #这里是为了验证用户是否有改变cookie去登录进网页
    @staticmethod
    def geneAuthCode(user_info):
        m=hashlib.md5()
        str="%s-%s-%s-%s"%(user_info.uid,user_info.login_name,user_info.login_pwd,user_info.login_salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

