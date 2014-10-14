import tornado.ioloop
import tornado.web
import json

from urllib import urlopen, urlencode

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        #self.write("Hello, world")
        print 'auth'
        print self.request.arguments
        echostr = self.get_argument('echostr', None)
        code = self.get_argument('code', None)

        if echostr:
            self.write(echostr)
            return
        if code:
           base_uri_raw = r'https://api.weixin.qq.com/sns/oauth2/access_token?appid=wxf28d9ef7f73a7660&secret=ca00f89852eeaed6181a87a5654b899e&grant_type=authorization_code&'
           base_uri = base_uri_raw + 'code='+code + '&'
           data_raw = urlopen(base_uri).read()
           print 'data_raw', data_raw
           if data_raw:
               data = json.loads(data_raw)
               print data
               access_token = data.get('access_token', '')
               openid = data.get('openid', '')
               print access_token,'-----------------', openid
               if access_token and openid:
                   args = {
                       'access_token': access_token,
                       'openid': openid,
                       'lang': 'zh_CN',
                   }
                   request_info_uri = r'https://api.weixin.qq.com/sns/userinfo?' + urlencode(args)
                   print 'request_user info url:', request_info_uri
                   data_raw = urlopen(request_info_uri).read()
                   print 'data_raw', data_raw
                   user_info = json.loads(data_raw)
                   self.render('login.html', name=user_info['nickname'], sex=user_info['sex'], city=user_info['city'],
                                     country=user_info['country'], headimgurl=user_info['headimgurl'])



class LoginHandler(tornado.web.RequestHandler):
    def get(self):
    print 'get login';
    self.write('<a href="https://open.weixin.qq.com/connect/oauth2/authorize?scope=snsapi_userinfo&redirect_uri=http%3A%2F%2Fmissus.wang%2Fauth&response_type=code&appid=wxf28d9ef7f73a7660#wechat_redirect">auth</a>')

application = tornado.web.Application([
    (r"/auth", MainHandler),
    (r"/login", LoginHandler),
    ], debug=True,
)

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
