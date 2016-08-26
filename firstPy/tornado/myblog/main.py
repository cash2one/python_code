#coding:utf-8
import random
import os,sys
import json,time

reload(sys)
sys.setdefaultencoding("utf-8")

import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

import MySQLdb,urllib
conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="root",db="myblog", charset="utf8", port = 3306)
cursor = conn.cursor()

from elasticsearch import Elasticsearch,helpers
es = Elasticsearch()
api_status = {
    "expires_day": "2018-12-25",
    "host": '127.0.0.1',
    "version": "v1",
    "status": "active"
}
PER_PAGE_MAX = 20
PAGE_NUM_MAX = 10

class ErrorHandler(tornado.web.RequestHandler):
    # def get(self):
    #     self.write_error(404)

    def write_error(self, status_code, **kwargs):
        if status_code == 404 or status_code == 405:
            self.render('404.html')
        elif status_code == 500:
            self.render('404.html')
        else:
            self.write('error:' + str(status_code))

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        sql = '''select * from myblog'''
        cursor.execute(sql)
        posts = []
        for (id, title, category, summury,body, timestamp,source,status) in cursor.fetchall():
            _dict = {}
            _dict['id'] = id
            _dict['title'] = title
            _dict['category'] = json.loads(category)
            _dict['summury'] = summury
            _dict['body'] = body
            _dict['timestamp'] = timestamp
            posts.append(_dict)
        self.render(
            "index.html",
            posts=posts,
            categorys=[
                {
                    'tag':'company',
                    'count':1
                },
                {
                    'tag': 'python',
                    'count': 1
                },
            ],
        )

class PostHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('id')
        sql = '''select * from myblog where id=%s''' % id
        cursor.execute(sql)
        _dict = {}
        for (id, title, category, summury, body, timestamp,source,status) in cursor.fetchall():
            _dict['id'] = id
            _dict['title'] = title
            _dict['category'] = json.loads(category)
            _dict['summury'] = summury
            _dict['body'] = body
            _dict['timestamp'] = timestamp
        post = _dict
        self.render("post.html",post = post)

class CategoryHandler(tornado.web.RequestHandler):
    def get(self):
        tag = self.get_argument('tag')
        sql = '''select * from myblog where category like "%%%s%%"''' % tag
        cursor.execute(sql)
        posts = []
        for (id, title, category, summury, body, timestamp,source,status) in cursor.fetchall():
            _dict = {}
            _dict['id'] = id
            _dict['title'] = title
            _dict['category'] = json.loads(category)
            _dict['summury'] = summury
            _dict['body'] = body
            _dict['timestamp'] = timestamp
            posts.append(_dict)
        self.render("category_search.html",
                    posts = posts,
                    categorys=[
                        # {
                        #     'tag':'company',
                        #     'count':1
                        # },
                        # {
                        #     'tag': 'python',
                        #     'count': 1
                        # },
                        ],
                    )

class AboutHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("about.html",liked = {'like_count':0})

class EditHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("edit.html")

class WriteHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("write.html",the_category=[{'tag':'company'},{'tag':'python'}])

class WriteokHandler(tornado.web.RequestHandler):
    def post(self):
        title = self.get_argument('title')
        body = self.get_argument('body')
        summury = self.get_argument('summury')
        category = json.dumps({'tag':self.get_argument('category')})
        sql = '''insert into myblog (title, category, summury, body, timestamp) values ('%s','%s','%s','%s',now())''' \
              % (title, category, summury, body)
        cursor.execute(sql)
        conn.commit()
        _dict = {}
        _dict['id'] = id
        _dict['title'] = title
        _dict['category'] = json.loads(category)
        _dict['summury'] = summury
        _dict['body'] = body
        _dict['timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        post = _dict
        self.render("post.html", post=post)

class SearchHandler(tornado.web.RequestHandler):

    def get_retrieve_param(self, param):
        if 'raw' in param:
            raw = param['raw']
        else:
            raw = False

        if 'fields' in param:
            fields = param['fields']
        else:
            fields = ["title^3", "content"]

        if 'req_fields' in param:
            req_fields = param['req_fields']
        else:
            req_fields = None

        if 'query' in param:
            query = param['query']
        else:
            query = None

        if 'query_list' in param:
            query_list = param['query_list']
        else:
            query_list = None

        if 'subject' in param:
            subject = param['subject']
        else:
            subject = None

        if subject and type(subject) != list:
            subject = [subject]

        if 'req_class' in param:
            req_class = param['req_class']
        else:
            req_class = None

        if 'tag' in param:
            tag = param['tag']
        else:
            tag = None

        size = min(PER_PAGE_MAX, int(param.get('size', 20)))
        offset = min(PAGE_NUM_MAX * PER_PAGE_MAX, int(param.get('offset', 0)))
        print "size", size, "offset", offset

        if 'except_subject' in param:
            except_subject = param['except_subject']
        else:
            except_subject = None

        except_class = param.get('except_class', None)

        random = param.get('random', None)

        b_body = {"bool": {"must": [], "should": [], "must_not": []}}
        if subject:
            b_body["bool"]["must"].append(
                {
                    "constant_score": {
                        "filter": {
                            "terms": {"subject": subject}
                        },
                    }
                }
            )

        if tag:
            b_body["bool"]["must"].append({"filtered": {"filter": {"terms": {"bread": tag}}}})

        if req_class:
            b_body["bool"]["must"].append({"filtered": {"filter": {"terms": {"class": req_class}}}})

        if query:
            b_body["bool"]["must"].append(
                {"multi_match":
                    {
                        "query": query,
                        "type": "most_fields",
                        "fields": fields
                    }
                }
            )

        if query_list:
            for query in query_list:
                b_body["bool"]["must"].append(
                    {"multi_match":
                        {
                            "query": query,
                            "type": "most_fields",
                            "fields": fields
                        }
                    }
                )

        if except_subject:
            b_body["bool"]["must_not"].append(
                {
                    "constant_score": {
                        "filter": {
                            "terms": {"subject": except_subject}
                        },
                    }
                }
            )

        if except_class:
            b_body["bool"]["must_not"].append(
                {
                    "constant_score": {
                        "filter": {
                            "terms": {"class": except_class}
                        },
                    }
                }
            )

        b_body["bool"]["must_not"].append({"terms": {"status": ["3"]}})  # delete

        b_body["bool"]["should"].append(
            {
                "function_score": {
                    "functions": [
                        {
                            "filter": {
                                "term": {"status": "1"}
                            },
                            "weight": 10
                        }
                    ],
                    "score_mode": "sum",
                }
            }
        )

        sort_method = []

        sort_method.append({"_score": {"order": "desc"}})
        # sort_method.append({"_id" : "desc"})

        b_body = {"query": b_body,
                  "sort": sort_method
                  # "highlight": {
                  #        "pre_tags" : ['<b style="color:black;background-color:#ffff66">'],
                  #        "post_tags" : ["</b>"],
                  #        "fields" : {
                  #            "title" : {}
                  #        }
                  #
                  # }
                  }
        if random:
            b_body["sort"] = {
                "_script": {
                    "script": "Math.random() * (100 - 1) + 1",
                    "type": "number",
                    "params": {},
                    "order": "desc"
                }
            }

        if offset != None and size != None:
            b_body['from'] = offset
            b_body['size'] = size

        if req_fields:
            b_body['fields'] = req_fields

        return b_body

    def get(self):
        #self.set_header('Content-Type', 'application/json')
        query = self.get_argument('query', None)
        params = {
        "query": query,
        "fields": ["title","body","category"],
        "offset": 0,
        "size": 50
        }

        result = {"code": -1, "data": None, "api": api_status, "message": ""}
        result["api"]["timestamp"] = time.time()

        if not params:
            result["error"] = "params error"
            self.write(json.dumps(result))
            return

        ts = time.time()
        b_body = self.get_retrieve_param(params)

        nolimit = params.get("nolimit", False)
        if nolimit:
            size = int(params.get('size', 20))
            offset = int(params.get('offset', 0))
        else:
            size = min(PER_PAGE_MAX, int(params.get('size', 20)))
            offset = min(PAGE_NUM_MAX * PER_PAGE_MAX, int(params.get('offset', 0)))

        if 'query' in params and params['query']:
            query = params['query'].strip()
        else:
            query = None

        if 'index' in params and params['index']:
            indexname = params['index']
        else:
            indexname = 'myblog'


        shards_route_str = ""
        if 'query' in params and params['query']:
            shards_route_str += params['query']

        if 'subject' in params and params['subject']:
            shards_route_str += str(params['subject'])

        ua = params.get("ua", None)

        amount = 0
        ret = {"message": "", "code": 0}
        records = []
        print ("%s" % json.dumps(b_body, indent=4))
        try:
            res = es.search(
                index=indexname,
                body=b_body,
                # search_type='dfs_query_then_fetch',
                preference=shards_route_str)
            #amount = res['hits']['total']
        except Exception as e:
            print e


        #self.write(json.dumps(res))
        posts = []
        if len(res['hits']['hits'])>0:
            print 'ok'
            for each in res['hits']['hits']:
                post = {}
                post = each['_source']
                post['category'] = json.loads(post['category'])
                posts.append(post)
        else:
            posts = []

        self.render(
            "index.html",
            posts=posts,
            categorys=[
                {
                    'tag': 'company',
                    'count': 1
                },
                {
                    'tag': 'python',
                    'count': 1
                },
            ],
        )

        #return

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers = [(r'/',IndexHandler),(r'/post?',PostHandler),(r'/category?',CategoryHandler)
            ,(r'/about',AboutHandler),(r'/edit',EditHandler),(r'/write',WriteHandler),(r'/writeok',WriteokHandler)
            , (r'/search/?', SearchHandler),('/.*', ErrorHandler)],
        template_path = os.path.join(os.path.dirname(__file__),'templates'),
        static_path = os.path.join(os.path.dirname(__file__),'static'),
        debug = True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()