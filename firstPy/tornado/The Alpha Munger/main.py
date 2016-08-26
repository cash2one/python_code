#coding:utf-8
import random
import os,sys
import json

reload(sys)
sys.setdefaultencoding("utf-8")

import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8989, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class MungedPageHandler(tornado.web.RequestHandler):
    def map_by_first_letter(self, text):
        mapped = dict()
        for line in text.split('\r\n'):
            for word in [x for x in line.split(' ') if len(x) > 0]:
                if word[0] not in mapped:
                    mapped[word[0]] = []
                mapped[word[0]].append(word)
        return mapped

    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)
        change_lines = text_to_change.split('\r\n')
        #可以传递函数给模板
        self.render('munged.html', source_map=source_map, change_lines=change_lines,
                choice=random.choice)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    #你可能注意到了debug=True的使用。
    # 它调用了一个便利的测试模式：tornado.autoreload模块，
    # 此时，一旦主要的Python文件被修改，Tornado将会尝试重启服务器，
    # 并且在模板改变时会进行刷新。对于快速改变和实时更新这非常棒，但不要再生产上使用它，因为它将防止Tornado缓存模板！
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/poem', MungedPageHandler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

#那么为什么使用static_url而不是在你的模板中硬编码呢？有如下几个原因。
# 其一，static_url函数创建了一个基于文件内容的hash值，并将其添加到URL末尾（查询字符串的参数v）。
# 这个hash值确保浏览器总是加载一个文件的最新版而不是之前的缓存版本。
# 无论是在你应用的开发阶段，还是在部署到生产环境使用时，都非常有用，因为你的用户不必再为了看到你的静态内容而清除浏览器缓存了。

#另一个好处是你可以改变你应用URL的结构，而不需要改变模板中的代码。
# 例如，你可以配置Tornado响应来自像路径/s/filename.ext的请求时提供静态内容，而不是默认的/static路径。
# 如果你使用static_url而不是硬编码的话，你的代码不需要改变。
# 比如说，你想把静态资源从我们刚才使用的/static目录移到新的/s目录。
# 你可以简单地改变静态路径由static变为s，然后每个使用static_url包裹的引用都会被自动更新。
# 如果你在每个引用静态资源的文件中硬编码静态路径部分，你将不得不手动修改每个模板。