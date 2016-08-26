#!/usr/bin/env python
# -*- coding:utf-8-*-
from celery import Celery
from urllib3 import HTTPConnectionPool
import random
import multiprocessing
import hashlib
import urllib
import os, re
import json
import sys
import HTMLParser
import datetime
from elasticsearch import helpers

root_base = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_base + '/lib/')
sys.path.append(root_base)
from zhanqun_sitename import zhanqun_resource_dict
from kombu import Exchange, Queue
from search_instance import bs_searcher as searcher
from snownlp import SnowNLP
from detail_wt import *
from elasticsearch import Elasticsearch

elastic_sao = Elasticsearch()

TOKEN = "030000cf9f3bdec7189390cda9398dca"

Q_INDEX = 'zhanqun_celery_landingpage_index'
Q_SITE = 'zhanqun_celery_landingpage_site'
Q_DOC = 'zhanqun_celery_landingpage_doc'

CELERY_DEFAULT_QUEUE = 'zhanqun_celery'
CELERY_QUEUES = (
    Queue(Q_INDEX, Exchange('zhanqun_celery'), routing_key=Q_INDEX + '.'),
    Queue(Q_DOC, Exchange('zhanqun_celery'), routing_key=Q_DOC + '.'),
    Queue(Q_SITE, Exchange('zhanqun_celery'), routing_key=Q_SITE + '.')
)

reload(sys)
sys.setdefaultencoding('utf8')

app = Celery('celery_landingpage',
             broker='redis://localhost:6379/4')

html_remove = re.compile(r'<[^>]+>', re.S)
parser = HTMLParser.HTMLParser()

pool = HTTPConnectionPool('internal-zhanqun-search.baijiahulian.com', maxsize=100)


def generate_common_doc(query, prefix, sitename):
    img_ptr = random.randint(1, 20)
    if img_ptr == 8:
        img_ptr = 1
    img_url = "http://file.gsxservice.com/zhanqun/static/images/list/%s.jpg" % img_ptr

    merge_content = '<img src="%s"  alt="%s %s"/>' % (img_url, query, sitename)

    m = hashlib.md5()
    m.update(query)
    qid = m.hexdigest()

    param = {
        "query": query,
        "query_list": [sitename],
        "fields": ["title"],
        "offset": 0,
        "size": 50
    }

    if prefix != "zuowen":
        param["except_subject"] = ["作文 作文"]

    #r = pool.request('GET', '/v1/retrieve', fields={"token": TOKEN, "params": urllib.quote_plus(json.dumps(param))})
    r = retreive(json.dumps(param))
    #r = json.loads(r.data)
    r = json.loads(r)
    records = r["data"]['records']
    original_records = r['data']['records']
    if len(records) == 0:
        return None

    # random.seed(qid)
    records = random.sample(records, min(5, len(records)))

    final_record = records[0]

    for doc in records:
        if 'highlight' in doc:
            title = doc['highlight']['title'][0]
        else:
            title = doc["content"]['title']

        try:
            content = doc['content']['content']
        except:
            continue

        content = html_remove.sub('', parser.unescape(content)).strip()

        try:
            s = SnowNLP(content)
            sents = s.summary(10)
        except:
            continue

        sub_content = "，".join(sents)
        xurl = 'http://www.genshuixue.com/i-%s/p/%s' % (prefix, doc['id'])

        merge_content += '''
        <a class='link-x' href='http://www.genshuixue.com/i-%s/p/%s'><h3><b>%s [点击查看原文]</b></h3></a>
        <hr>
        <div>%s...</div>
        <br>
        ''' % (prefix, doc['id'], title, sub_content)

    current_datetime = str(datetime.datetime.now()).split('.')[0]

    extra_records = random.sample(original_records, min(15, len(original_records)))
    merge_content += '<br>【%s】推荐阅读<br><div class="clearfix">' % query
    for r in extra_records:
        title = r["content"]['title']
        merge_content += '''<a href="http://www.genshuixue.com/i-%s/p/%s" class="link-x-a-highlight" target="_blank">%s</a>''' % (
        prefix, r['id'], title)

    merge_content += '</div>'

    param = {
        "query": query,
        "subject": "%s 问答" % sitename,
        "offset": 0, "size": 10
    }

    m.update(query)

    # r = searcher.retrieve(param)
    #r = pool.request('GET', '/v1/retrieve', fields={"token": TOKEN, "params": urllib.quote_plus(json.dumps(param))})
    r = retreive(json.dumps(param))
    r = json.loads(r)
    #r = json.loads(r.data)
    records = r["data"]['records']

    extra_records = random.sample(records, min(5, len(records)))
    merge_content += '<br>【%s】相关问答<br><br><div class="clearfix">' % query
    for r in extra_records:
        if 'highlight' in doc:
            title = doc['highlight']['title'][0]
        else:
            title = doc["content"]['title']
        title = "【%s】%s [点击查看原文]" % (title, r['content']['question_detail'])

        qa_content = ''
        ans = r['content']['answers']
        random.shuffle(ans)
        for q in ans[:2]:
            qcontent = html_remove.sub('', parser.unescape(q['content'])).strip()
            qa_content += '<div>%s</div>' % qcontent[:200]

        xurl = 'http://www.genshuixue.com/i-%s/p/%s' % (prefix, r['id'])
        qa = '''
        <a class='link-x' href='http://www.genshuixue.com/i-%s/p/%s'><h3><b>%s</b></h3></a>
        <hr>
        <div>%s</div>
        <br>''' % (prefix, r['id'], title, qa_content.strip())
        merge_content += qa

    merge_content += '</div>'

    extra_records = random.sample(records, min(10, len(records)))
    merge_content += '<br>【%s】推荐问答<br><div class="clearfix">' % query
    for r in extra_records:
        title = r['content']['title']
        merge_content += '''<a href="http://www.genshuixue.com/i-%s/p/%s" class="link-x-a-highlight" target="_blank">%s</a>''' % (
        prefix, r['id'], title)

    merge_content += '</div>'

    merge_content += '<br>【%s】推荐搜索<br><div class="clearfix">' % query

    oq_params = {"query": query, "size": 10, "extra": sitename, "token_src": "query_landingpage"}
    r = original_query(TOKEN, json.dumps(oq_params), 1000)
    r = json.loads(r)
    # r = pool.request('GET', '/v1/original_query',
    #                  fields={"token": TOKEN, "params": urllib.quote_plus(json.dumps(oq_params))})
    #r = json.loads(r.data)

    query_keywords = []

    for q in r["data"]["records"]:
        q = q['query']
        query_keywords.append(q)
        m = hashlib.md5()
        m.update(q)
        inner_qid = m.hexdigest()
        merge_content += '''<a href="http://www.genshuixue.com/i-%s/x/%s.html" class="link-x-a-highlight" target="_blank">%s</a>''' % (
        prefix, inner_qid, q)
    merge_content += '</div>'

    final_record['status'] = 3
    final_record['title'] = query
    final_record['id'] = qid
    final_record['content'] = merge_content
    final_record['source'] = 'QLP'
    final_record['date'] = current_datetime.split(' ')[0]
    final_record['subject'] = '%s@跟谁学' % sitename
    final_record['class'] = 'QLPV2'

    original = {"content": {}, "taskid": "", "update_time": ""}

    original['content']['keywords'] = ",".join(query_keywords[:10])

    original['content']['class'] = "QLPV2"
    original['content']['title'] = query
    original['content']['content'] = merge_content
    original['content']['date'] = final_record['date']
    original['content']['source'] = '%s@跟谁学' % sitename

    final_record['original'] = json.JSONEncoder().encode(original)
    return final_record


def generate_jita_doc(query, prefix, sitename):
    img_urls = [
        "http://file.gsxservice.com/zhanqun/static/images/jita/jay.jpg",
        "http://file.gsxservice.com/zhanqun/static/images/jita/banner.png",
        "http://file.gsxservice.com/zhanqun/static/images/jita/xuwei.jpg",
        "http://file.gsxservice.com/zhanqun/static/images/jita/zhangxuan.jpg"]
    img_url = random.sample(img_urls, 1)[0]
    merge_content = '<img src="%s"  alt="%s"/>' % (img_url, query)
    param = {
        "query": query,
        "subject": "吉他 吉他谱",
        "offset": 0, "size": 20
    }
    m = hashlib.md5()
    m.update(query)
    qid = m.hexdigest()
    # 疑问2
    r = pool.request('GET', '/v1/retrieve', fields={"token": TOKEN, "params": urllib.quote_plus(json.dumps(param))})
    r = json.loads(r.data)

    jita_records = r['data']['records']
    jita_records = random.sample(jita_records, min(10, len(jita_records)))

    merge_content += '<br><a href="http">【%s】推荐吉他谱</a><br><div class="clearfix">' % query
    for r in jita_records:
        merge_content += '''<a href="http://www.genshuixue.com/i-%s/p/%s" class="link-x-a-highlight" target="_blank">%s</a>''' % (
        prefix, r['id'], r['content']['title'])
    merge_content += '</div><hr><br>'
    param = {
        "query": query,
        "subject": "吉他 吉他资讯",
        "offset": 0, "size": 20
    }

    # r = searcher.retrieve(param)
    r = pool.request('GET', '/v1/retrieve', fields={"token": TOKEN, "params": urllib.quote_plus(json.dumps(param))})
    r = json.loads(r.data)
    records = r["data"]['records']
    original_records = r['data']['records']

    # random.seed(qid)
    records = random.sample(records, min(5, len(records)))
    final_record = None
    for doc in records:
        if 'highlight' in doc:
            title = doc['highlight']['title'][0]
        else:
            title = doc['content']['title']
        content = doc['content']['content']
        content = html_remove.sub('', parser.unescape(content)).strip()
        try:
            s = SnowNLP(content)
            sents = s.summary(10)
        except:
            continue

        sub_content = "，".join(sents)
        # 疑问3
        merge_content += '''

        <a class='link-x' href='http://www.genshuixue.com/i-%s/p/%s'><h3><b>%s [点击查看全文]</b></h3></a>
        <hr>
        <div>%s...</div>
        <br>
        ''' % (prefix, doc['id'], title, sub_content)

        final_record = doc

    current_datetime = str(datetime.datetime.now()).split('.')[0]

    extra_records = random.sample(original_records, min(15, len(original_records)))
    merge_content += '<br><a href="http">【%s】推荐阅读</a><br><div class="clearfix">' % query
    for r in extra_records:
        title = r['content']['title']
        merge_content += '''<a href="http://www.genshuixue.com/i-%s/p/%s" class="link-x-a-highlight" target="_blank">%s</a>''' % (
        prefix, r['id'], title)
    merge_content += '</div>'

    param = {
        "query": query,
        "subject": "吉他 问答",
        "offset": 0, "size": 10
    }

    m.update(query)

    # r = searcher.retrieve(param)
    r = pool.request('GET', '/v1/retrieve', fields={"token": TOKEN, "params": urllib.quote_plus(json.dumps(param))})
    r = json.loads(r.data)
    records = r['data']['records']

    extra_records = random.sample(records, min(5, len(records)))
    merge_content += '<br>【%s】问答<br><div class="clearfix">' % query
    for r in extra_records:
        if 'highlight' in doc:
            title = doc['highlight']['title'][0]
        else:
            title = doc['content']['title']
        title = "【%s】%s [点击查看全文]" % (title, r['content']['question_detail'])
        qa_content = ''
        ans = r['content']['answers']
        random.shuffle(ans)
        for q in ans[:2]:
            qcontent = html_remove.sub('', parser.unescape(q['content'])).strip()
            qa_content += '%s...' % qcontent[:200]

        qa = '''
        <a class='link-x' href='http://www.genshuixue.com/i-%s/p/%s'><h3><b>%s</b></h3></a>
        <hr>
        <div>%s...</div>
        <br>''' % (prefix, r['id'], title, qa_content)
        merge_content += qa

    merge_content += '</div>'

    extra_records = random.sample(records, min(10, len(records)))
    merge_content += '<br>【%s】推荐问答<br><div class="clearfix">' % query
    for r in extra_records:
        title = r['content']['title']
        merge_content += '''<a href="http://www.genshuixue.com/i-%s/p/%s" class="link-x-a-highlight" target="_blank">%s</a>''' % (
        prefix, r['id'], title)

    merge_content += '</div>'

    merge_content += '<br>【%s】推荐搜索<br><div class="clearfix">' % query

    oq_params = {"query": query, "size": 10, "extra": sitename, "token_src": "query_landingpage"}

    r = pool.request('GET', '/v1/original_query',
                     fields={"token": TOKEN, "params": urllib.quote_plus(json.dumps(oq_params))})
    r = json.loads(r.data)
    query_keywords = []
    for q in r["data"]["records"]:
        q = q['query']
        query_keywords.append(q)
        m = hashlib.md5()
        m.update(q)
        inner_qid = m.hexdigest()
        merge_content += '''<a href="http://www.genshuixue.com/i-%s/x/%s.html" class="link-x-a-highlight" target="_blank">%s</a>''' % (
        prefix, inner_qid, q)
    merge_content += '</div>'

    final_record['status'] = 3
    final_record['title'] = query
    final_record['id'] = qid
    final_record['content'] = ""
    final_record['source'] = '吉他@跟谁学'
    final_record['date'] = current_datetime.split(' ')[0]
    final_record['subject'] = '吉他@跟谁学'
    final_record['class'] = 'QLPV2'

    original = {"content": {}, "taskid": "", "update_time": ""}

    original['content']['keywords'] = ",".join(query_keywords[:10])
    original['content']['class'] = "QLPV2"
    original['content']['title'] = query
    original['content']['content'] = merge_content
    original['content']['date'] = final_record['date']
    original['content']['source'] = '吉他@跟谁学'

    final_record['original'] = json.JSONEncoder().encode(original)
    return final_record


def jita():
    data = open("./data/jita.dat").readlines()
    for line in data:
        line = line.strip().split("\t")
        query = line[0].strip()
        # try:
        if 1:
            doc = generate_jita_doc(query, 'jita', "吉他")
            print elastic_sao.index(body=doc, index='corpora_index_v2_b', doc_type='normal', id=doc['id'])
        # except Exception,w:
        #    print (w)
        #    continue
        exit()


def load_query_black_list(query_black_index):
    filename = "./data/blackquery.dat"
    print ("load black query from %s" % filename)
    with open(filename, 'r') as f:
        data = f.readlines()
        print ("total size %s" % len(data))
        for i in data:
            query = i.strip()
            query_black_index.enter(query)
        query_black_index.fix()


def indexing(doc):
    ret = elastic_sao.index(body=doc, index='corpora_index_v2_b', doc_type='normal', id=doc['id'])
    #print (ret)
    return ret


def gen_doc_for_query(query, site_prefix, sitename):
    if site_prefix == "jita":
        doc = generate_jita_doc(query, site_prefix, sitename)
    else:
        doc = generate_common_doc(query, site_prefix, sitename)
    if doc:
        url = "http://www.genshuixue.com/i-%s/x/%s.html" % (site_prefix, doc['id'])
        indexing(doc)
        print url
        print '###########################'
        print json.dumps(doc)
        print '###########################'


def gen_site(site_prefix, sitename):
    sitename = sitename.strip()
    # 疑问1
    #print sitename
    r = searcher.dump_query(sitename)
    #print json.dumps(r)
    for i in r:
        query = i['_source']['query']
        #print json.dumps(i)

        print ("[%s] ACCEPT %s" % (sitename,query))
        #gen_doc_for_query(query,site_prefix, sitename)


if __name__ == '__main__':
    ignore = ['172', 'tofel']
    i=0
    for site, value in sorted(zhanqun_resource_dict.items(), key=lambda x: random.random()):
        if site in ignore:
            print ("ignore %s" % site)
            continue
        site_prefix = site
        sitename = value['name']
        gen_site(site_prefix, sitename)
        print "####%s\t%s" % (site_prefix,sitename)
        i += 1
        if i == 2:
            break

    import datetime

    starttime = datetime.datetime.now()
    # long running
    gen_doc_for_query('高考','gaokao', '高考')

    endtime = datetime.datetime.now()
    print (endtime - starttime).seconds

