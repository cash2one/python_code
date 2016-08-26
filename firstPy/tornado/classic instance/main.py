#!/bin/env python
# encoding = utf-8
import os
import time
import base
from subprocess import call
import tornado.ioloop
import tornado.httpserver
from tornado.web import StaticFileHandler, authenticated, HTTPError, asynchronous, RequestHandler, Application
from tornado import escape  # 因为我定义了很多操作，其中html文件都在本脚本实现，隐藏属性_xsrf 需要自定义获取 所以根据源码修改了获取方式
from tornado.options import define, options
import tornado.database  # tornado结合mysql的class
from  parse import Parse

# define("debug", default=True, type=bool)
flag = 0
flag2 = 0
Flag = 1
src = ''


class BaseHandler(RequestHandler):  # 自定义继承RequestHandler类，修改get_current_user方法
    def get_current_user(self):
        return self.get_secure_cookie("user")  # 这里我根据cookie的信息，去数据库对比看是不是在我的table中，证明登录验证是否成功

    def check_user(self):  # 在相应页面使用这个方法，检验是否登录，假如没有cookie说明未登录，自动跳转到/login
        if not self.current_user:
            self.redirect("/login")
            return


class MyRequestHandler(RequestHandler):  # 我使用了xsrf特性，但是有个路径是接受客户端post数据，有xsrf很不好实现，那么就让这个路径不检查xsrf_cookie
    def check_xsrf_cookie(self):
        pass


class HomeHandler(BaseHandler):  # 这是根目录的相应类，发现未登录，自动跳转
    def get(self):
        self.check_user()
        self.render("static/index.html")  # 检查登录后，将页面指向我根目录下static/index.html ，页面显示那里面的内容


class MailHandler(BaseHandler):  # 根据index.html跳转到 /mail
    def get(self):
        self.check_user()
        self.render("static/fort.html")  # 检查登录后，将页面指向我根目录下static/fort.html ，页面显示那里面的内容


class CheckHandler(BaseHandler):
    def get(self):
        self.check_user()
        self.render("static/forp.html")


class MysqlHander:  # 定义的数据库操作类
    def __init__(self):
        self.db = tornado.database.Connection("localhost", \
                                              "test1", "user12", "qwertyu")  # 初始化连接数据库，用户名 user12，密码 qwertyu，库名 test1

    def delete(self, table):  # 删除table
        self.db.execute("drop table %s" % table)

    def getuser(self, usr):  # 测试用，我登录输入用户和输入密码使用了2个页面，但是table是一个，字段不同，这2个其实可以合并
        if self.db.execute_rowcount("select * from user where User = '%s'" % usr) == 1:
            return 1
        else:
            return 0  # 当发现有符合的条目，返回1 否则返回0

    def getpasswd(self, passwd):
        if self.db.execute_rowcount("select * from user where Passwd = '%s'" % passwd) == 1:
            return 1
        else:
            return 0

    def update(self, table, dict):  # 修改table的数据
        for i in dict.keys():
            self.db.execute(
                "UPDATE %s SET Sended = %d WHERE Email = '%s'" % (table, dict[i], i))  # 本来想使用 executemany，但是不知道为啥总报语法错误

    def taprint(self, table, flag=0, send=1):  # 返回一个字符串，包含符合要求的条目结果，这个会传给js格式化
        str = ''
        for i in self.db.query("select * from %s where Flag = %d and Send !=%d" % (table, flag, send)):
            str += '%s,%s,' % (i['Email'], i['Send'])
        return str[:-1]

    def gettotal(self, table):
        count = self.db.execute_rowcount("select * from %s" % table)
        flagcount = self.db.execute_rowcount("select * from %s where Flag =1" % table)  # 计算一些符合要求的数目的条数
        send = {}
        for i in range(6):
            data = self.db.execute_rowcount("select * from %s where Flag =1 and Sended =%d" % (table, i))
            send[i] = data
        return count, flagcount, send

    def getdb(self, table):  # 获取想要table的某字段的所有数据，返回拼接的字符串
        str = ''
        for i in self.db.query("select Cf from %s" % table):
            str += i['Cf'] + ','
        return str[:-1]

    def check(self, table):  # 检查是否存在某table  存在返回1 否则0
        flag = 0
        for i in self.db.query("check table %s" % table):
            if i['Msg_type'] == 'status' and i['Msg_text'] == 'OK':
                flag = 1
        return flag


class UploadDbCheckHandler(BaseHandler):  # 这个类主要用来上传文件后执行了数据库插入，对这个table进行预览，看是不是想要的效果
    def get(self, id):
        self.check_user()
        if id == '':
            self.write("Please upload files to create a database!")
            self.render("static/jump.html")
        try:
            db = MysqlHander()
            data = db.getdb(id)
            self.render("static/print.html", num='1', str=data)  # 这里会传递到一个html，里面有一个js，对data数据格式化显示 num 表示 、
            # 每行显示1条 （因为获取的是一个字段）
        except:
            self.write("Database Error!")


class WebgetHandler(BaseHandler):  # 这个类主要用来查询某个table的数据，是根据path实现的
    def get(self, id):  # 获取path路径符合要求的字段，作为table的名称，这个路径，是从application 实现，
        # 根据不同路径作不同的操作，上一级根据要查询的table名字，
        # 让他自动跳转到这个页面，触发这个类
        self.check_user()
        try:
            db = MysqlHander()
            str = db.taprint(id)
            self.render("static/print.html", num='2', str=str)  # 这个操作是查询table里面的2个字段，所以num＝2，每行显示2个字段
        except:
            self.write("Don't have this table!")


class PostHandler(MyRequestHandler):  # 上面说的我设计的获取post数据的类
    def post(self):
        uri = self.request.body
        mydict = eval(base.decode(uri, 'mpzpie94fK,cY'))  # post方法获取数据，因为我的post是根据自己的base模块加密的，所以这里先解密
        # mydict = {}     #一下这几段注释的，是我在不加密的时候传送过来的解析方法，根据"&"格式化
        # for i in uri.split('&'):
        #    data = i.split('=')
        #    mydict[data[0]]=data[1]
        print mydict.keys()
        self.write("chenggong")  # 当客户端post完成，会在客户端那里显示"chenggong", 证明操作成功，记录日志，方便派错


class WebHandler(BaseHandler):
    def get(self, id):
        self.check_user()
        try:
            db = MysqlHander()
            total = db.gettotal(id)
            totalmail = total[0]
            sendedmail = total[1]
            if sendedmail == 0:
                sendedmail = 1
                for i in range(6):
                    total[2][i] = 0
            items = []
            items.append("Total Mails:%d" % totalmail)
            items.append("Process Mails:%d" % sendedmail)
            items.append("Success Send Mails:%d  Send success rate:%6.2f" \
                         % (total[2][1], total[2][1] / sendedmail))
            items.append("Deferred Send Mails:%d  Send deferred rate:%6.2f" \
                         % (total[2][2], total[2][2] / sendedmail))
            items.append("Bounced Send Mails:%d  Send bounced rate:%6.2f" \
                         % (total[2][3], total[2][3] / sendedmail))
            items.append("Deferral Send Mails:%d  Send deferral rate:%6.2f" \
                         % (total[2][4], total[2][4] / sendedmail))
            items.append("Reject Send Mails:%d  Send reject rate:%6.2f" \
                         % (total[2][5], total[2][5] / sendedmail))  # 这里主要是根据查询数据库结果，显示一个html，里面有固定格式
            title = '%s Mail Statistics' % id
            call('python chart.py %d %d %d %d %d' %  \  # 这个chart.py是pychat模块，画图类，生成一个图表 可能更加直观。
            # 但是我使用import chart时候没有起效果，所以将数据作为命令参数方式直接执行脚本以
            # 实现每次先更新图像，再展示展示html
            (int(total[2][1] / sendedmail), \
             int(total[2][2] / sendedmail), int(total[2][3] / sendedmail), \
             int(total[2][4] / sendedmail), int(total[2][5] / sendedmail)) \
                , shell = True)
            self.render("static/total.html", title=title, ontitle=title,
                        items=items)  # render到static/total.html,这是一个模板文件
        except:
            self.write("Don't have this table!")


class Handler(BaseHandler):  # 因为我的登录输入帐号和密码是2个路径，他们的展示类似（值是login和passwd的不同，这里写了一个基类，实现代码重用）
    def get(self):
        self.write('<html><body><form action="/%(str)s" method="post">'
                   '%(str)s: <input type="text" name="%(str)s">'
                   '<input type="submit" value="Sign in">'
                   '<input type="hidden" name="_xsrf" value="%(xsrf)s">'
                   '</form></body></html>' % {'str': self.action,
                                              'xsrf': escape.xhtml_escape(self.xsrf_token)})  # 通过在self.write里面使用
        # escape.xhtml_escape获取xsrf字符串，因为self.action多次用，
        # 使用了这样的方式 而不是'%s %s' % (self.action,self.action)

    def post(self):
        name = self.get_argument(self.action)  # 获取输入的值
        try:
            db = MysqlHander()
            flag = getattr(db, self.check)(name)
            使用getattr
            大家细看
        except:
            self.write("database error!")
        if flag:
            if self.cookie:
                self.set_secure_cookie("user", name)
                self.redirect("/passwd")
            else:
                self.redirect("/")
        else:
            self.redirect("/%s" % self.action)


class DeleteHandler(RequestHandler):
    def get(self):
        self.write('<html><body><form action="" method="post">'
                   'Delete (html/table): <input type="text" name="delete">'
                   '<input type="submit" onclick="return confirm(\'Are you sure?\')" name ="opert" value="Delete table"/>'
                   '<input type="submit" onclick="return confirm(\'Are you sure?\')" name ="operf" value="Delete file"/>'
                   '<input type="hidden" name="_xsrf" value="%(xsrf)s">'
                   '</form></body></html>' % {'xsrf': escape.xhtml_escape(self.xsrf_token)})  # 这里用了2个html的弹出框，以确认我的操作

    def get_argument(self, name, strip=True):
        default = []
        args = self.get_arguments(name, strip=strip)
        if not args:
            return default
        return args[-1]  # 重写了get_argument，因为我删除文件或者table是不同的操作，按那个删除键 把相应的输入结果当成table或者文件做不同操作
        # 但是一次只有一个get_argument有结果，另外一个会'miss',所以我修改了这个方法，不让它raise

    def post(self):
        try:
            data = self.get_argument("delete")
        except:
            self.write("Please enter the information you want to delete !")
            self.render("static/jump.html")  # 里面主要是一个js脚本，主要是为了倒计时跳转（倒计时是为了防止恶刷）
        if self.get_argument("opert"):  # 根据点击的按键，做不同类的删除
            d = MysqlHander()
            if not d.check(data):
                self.write("Don't have this table!")
                return -1
            try:
                d.delete(data)
            except:
                self.write("Database Error!")
            self.write("Table has been deleted!")
            self.render("static/jump.html")
        if self.get_argument("operf"):
            try:
                os.remove("uphtml/" + data)
            except:
                self.write("Error!")
                return -1
            self.write("Html File has been deleted!")
            self.render("static/jump.html")


class PasswdHandler(Handler):  # 这是上面活的login和passwd的2个页面的操作类
    def __init__(self, application, request, **kwargs):  # 初始化上层类
        Handler.__init__(self, application, request, **kwargs)
        Handler.action = 'passwd'
        Handler.check = 'getpasswd'  # 根据不同的self.check，调用不同的数据库相应同名方法（同名直接调用的好处大家想）
        Handler.cookie = False


class LoginHandler(Handler):
    def __init__(self, application, request, **kwargs):
        Handler.__init__(self, application, request, **kwargs)
        Handler.action = 'login'
        Handler.check = 'getuser'
        Handler.cookie = True


class UploadHandler(RequestHandler):  # 这是一个上传文件的响应类
    def get(self):
        self.write('<html><body><form action="" \
                    enctype="multipart/form-data" method="post">'
                   '<input type="radio" name="choose" value=0 />upload database<br />'
                   '<input type="radio" name="choose" value=1 />upload html<br />'
                   '<input type="hidden" name="_xsrf" value="%s">'
                   '<input type="submit" value="Submit" name="upload"></form></body></html>' \
                   % escape.xhtml_escape(self.xsrf_token))

    def post(self):
        try:
            choose = self.get_argument("choose")  # 这里是radio方式的选择，单选。但是不选会异常处理。
        except HTTPError:
            self.write("Please choose !")
            self.render("static/jump.html")
            return -1
        if int(choose):
            self.redirect("upload/html")
        else:
            self.redirect("upload/db")  # 根据不同的选择跳转到不同的页面


class UploadHtmlHandler(RequestHandler):  # 上传文件类
    def get(self, src=None):  # src是我设计的一个"变异"，当我第一次调用时是空，view按键是不能点的（点了异常处理），
        # 但是调用完会嵌套选择，这样，根据选择结果，view按键就知道view什么了 ，下面会手动self.get(src)
        if not src:
            src = ''
        self.write('<html><head><script type="text/javascript" \
                   src="https://127.0.0.1/static/common.js"></script>\  #外部自定了一个js文件，代码重用
                   < / head > < body > < form
        action = ""
        enctype = "multipart/form-data"
        method = "post" > '
                          '<input name="myfile" type="file"/> <br />'
                          '<input type="hidden" name="_xsrf" value="%s">'
                          '<input type="submit" value="Submit" name="upload">' \
                          '<input type="button" value="view" onclick="HTMLButton(\'%s\')"></form></body></html>' \
                          % (escape.xhtml_escape(self.xsrf_token), src))
        def post(self):
            try:
                try:
                    myfile = self.request.files['myfile']
                except:
                    self.write("Please enter the file's address!")
                    self.render("static/jump.html")
                    return -1
                for f in myfile:
                    hz = os.path.splitext(f['filename'])[1][1:]  # 只支持html后缀文件
                    if hz != 'html':
                        self.write("Temporarily only to receive the  formats of the html file!")
                        self.render("static/jump.html")
                        return -1
                    src = "uphtml/" + f['filename']
                    with open(src, 'w+') as c:  # 将上传的文件保存在服务器的某个目录下，文件同名
                        c.write(f['body'])
                self.write("file upload OK! You have upload:%s" % f['filename'])
            except:
                self.write("file upload ERROR! try again")
                self.render("static/jump.html")
                return -1
            self.get(f['filename'])  # 重新回调，这样就能点击view了，然后会打开一个新窗口显示上传的html文件预览

    class UploadDbHandler(RequestHandler):  # 另外一个上传文件类，只要是根据文件将文件内数据入库
        def get(self, src=None):
            if not src:
                src = ''
            self.write('<html><head><script type="text/javascript" \
                   src="https://127.0.0.1/static/common.js"></script>\
                   </head><body><form action="" enctype="multipart/form-data" method="post">'
                       '<input name="myfile" type="file"/> <br />'
                       '<input type="radio" name="choose" value=1 />create database<br />'  # 这里也有一个radio方式的选择，可以上传文件的同时就自动把数据导入库中
                       '<input type="radio" name="choose" value=0 />no create database<br />'
                       '<input type="hidden" name="_xsrf" value="%s">'
                       '<input type="submit" value="Submit" name="upload">' \
                       '<input type="button" value="view" onclick="DBButton(\'%s\')"></form></body></html>' \
                       % (escape.xhtml_escape(self.xsrf_token), src))

        def choose(self, flag, table):
            if flag == 1:
                d = MysqlHander()
                d.delete(table)

        def post(self):
            global flag, flag2, Flag, src
            if flag:
                flag = 0
                try:
                    flag2 = int(self.get_argument("ch"))
                except:
                    self.write("Please choose whether or not")
                    flag2 = 2
            if Flag:
                try:
                    choose = self.get_argument("choose")
                except HTTPError:
                    self.write("Please choose whether or not to create a database")
                    self.render("static/jump.html")
                    return -1
                try:
                    try:
                        myfile = self.request.files['myfile']
                    except:
                        self.write("Please enter the file's address!")
                        self.render("static/jump.html")
                        return -1
                    for f in myfile:
                        hz = os.path.splitext(f['filename'])[1][1:]
                        if (hz != 'txt') and (hz != 'xls') and (hz != 'csv'):  # 判断是不是.txt .csv xls为后缀的文件
                            self.write("Temporarily only to receive the three formats of the csv / txt / xls file!")
                            self.render("static/jump.html")
                            return -1
                        src = "upload/" + f['filename']
                        with open(src, 'w+') as c:
                            c.write(f['body'])
            self.write("file upload OK! You have upload:%s<br />" % f['filename'])
            except:
            self.write("file upload ERROR! try again")
            self.render("static/jump.html")
            return -1

        self.data()
        if int(choose):
            sql = MysqlHander()
            check = sql.check(os.path.splitext(os.path.basename(src))[0])  # 检查数据库是不是已经有这个table
            if check:  # 已经有这个table，那么可以选择 覆盖，叠加，以及 取消
                flag = 1
                Flag = 0
                self.write('<form action="" enctype="multipart/form-data" method="post">'
                           '<input type="radio" name="ch" value=1 />Cover<br />'
                           '<input type="radio" name="ch" value=2 />Superposition<br />'
                           '<input type="radio" name="ch" value=0 />Cancel<br />'
                           '<input type="hidden" name="_xsrf" value="%s">'
                           '<input type="submit" value="Submit" name="upload">' \
                           % escape.xhtml_escape(self.xsrf_token))
                return -1
        else:
            print 'no create'
            self.get(os.path.splitext(os.path.basename(src))[0])
            return -1

    if flag2 or Flag:
        self.choose(flag2, os.path.splitext(os.path.basename(src))[0])
        Flag = 1
        d = Parse(src)  # 这是数据库插入数据类
        if not d.work():  # self.work()自动根据文件后缀使用不同的方法查库，也是getsttr，减少代码量
            self.write("Possible format problems, the database operation fails")
            return -1
        else:
            self.write("Database operation was successful<br />")
    self.get(os.path.splitext(os.path.basename(src))[0])


def data(self):  # 显示目录下已经上传的文件信息
    self.write("Has been uploaded files:<br />")
    for root, dirs, files in os.walk('./upload'):
        self.write("%s<br />" % files)


settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),  # 指定静态文件目录，而且比如我的favicon.ico放在这个目录下，
    # 直接使用/favicon.ico就能访问
    "upload_path": os.path.join(os.path.dirname(__file__), "upload"),  # 自动上传文件目录
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
}

application = Application([  # 根据不同的路径  触发不同的响应
    (r"/post_path", PostHandler),
    (r"/del", DeleteHandler),
    (r"/mail", MailHandler),
    (r"/mail/(.*)", WebHandler),
    (r"/check", CheckHandler),
    (r"/check/(.*)", WebgetHandler),
    (r"/", HomeHandler),
    (r"/login", LoginHandler),
    (r"/passwd", PasswdHandler),
    (r"/upload", UploadHandler),
    (r"/upload/db", UploadDbHandler),
    (r"/upload/db/(.*)", UploadDbCheckHandler),
    (r"/upload/html", UploadHtmlHandler),
    (r"/uphtml/(.*)", StaticFileHandler, dict(path=settings['upload_path'])),  # view 上传的文件，不设计这个，是访问不了的
], **settings)

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application, ssl_options={  # 指定使用ssl加密，具体加密方法以及自己的参考其他资料
        "certfile": os.path.join(os.path.abspath("."), "server.crt"),  # 也可以使用前端的反向代理，比如zxtm上面去做ssl，指向这些tornado客户端
        "keyfile": os.path.join(os.path.abspath("."), "server.key"),  # 方法请参看我51cto的博客
    })
    http_server.listen(443)
    tornado.ioloop.IOLoop.instance().start()