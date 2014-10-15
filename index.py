""" Demo for Tencent Wechat Oauth
"""
import tornado.ioloop
import tornado.web
import json

from urllib import urlopen, urlencode


REQUEST_ACCESTOKEN = r'https://api.weixin.qq.com/sns/oauth2/access_token?'
REQUEST_USERINFO = r'https://api.weixin.qq.com/sns/userinfo?'
APPSECRET = 'ca00f89852eeaed6181a87a5654b899e'
APPID = 'wxf28d9ef7f73a7660'
DEBUG = True

""" wechat callback.Check and get the user info
"""
class AuthHandler(tornado.web.RequestHandler):
    def get(self):
        code = self.get_argument('code', None)

        debug('code:' + code)
        if code: #if sucess wechat will return a 'code'
            accesstoken_args = {
                'appid': APPID,
                'secret': APPSECRET,
                'grant_type': 'authorization_code',
                'code': code,
            }
            uri = make_uri(REQUEST_ACCESTOKEN, **accesstoken_args)
            access_token_data = get_uri_data(uri)
            if access_token_data:
                access_info = json.loads(access_token_data)
                access_token = access_info.get('access_token', '')
                openid = access_info.get('openid', '')

                if access_token and openid:
                    userinfo_args = {
                        'access_token': access_token,
                        'openid': openid,
                        'lang': 'zh_CN',
                    }
                    request_userinfo_uri = make_uri(REQUEST_USERINFO, **userinfo_args)
                    user_info_data = get_uri_data(request_userinfo_uri)
                    user_info = json.loads(user_info_data)

                    login_info = self.make_login_info(user_info)
                    self.render('login.html', **login_info)
                    return None

        #Any error happend
        self.write('Get UserInfo Error')

    def make_login_info(self, user_info=None):
        """
           name=user_info['nickname'], sex=user_info['sex'], city=user_info['city'],
           country=user_info['country'], headimgurl=user_info['headimgurl'])
        """
        login_info = {}

        if not isinstance(user_info, dict):
             user_info = {}

        login_info['name'] = user_info.get('nickname', '<font color="red"> Not Geted</font>')
        login_info['sex'] = user_info.get('sex', 'Unknown')
        login_info['city'] = user_info.get('city', 'Unkown')
        login_info['country'] = user_info.get('country', 'Unkown')
        login_info['headimgurl'] = user_info.get('headimgurl', '')

        return login_info


"""
"""
class WechatHandler(tornado.web.RequestHandler):

    def get(self):
        print 'wechat url auth'
        echostr = self.get_argument('echostr', '')
        self.write(echostr)


def make_uri(base_url, **kargs):
    uri = base_url + urlencode(kargs)
    debug('uri: --' + uri + '--')
    return uri
    

def get_uri_data(uri):
    data =  urlopen(uri).read()
    debug('get_uri_data:--'+ data+ '--\n')
    return data

def debug(string):
    if DEBUG:
        print string

application = tornado.web.Application([
    (r"/auth", AuthHandler),
    (r"/wechat", WechatHandler),
    ], debug=True,
)

if __name__ == "__main__":
    print 'start......'
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
