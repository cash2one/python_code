#!/usr/bin/env python
#-*- coding:utf-8-*-
from celery import Celery
from urllib3 import HTTPConnectionPool
import random
import multiprocessing
import hashlib
import urllib
import os,re
import json
import sys
import HTMLParser
import datetime
from elasticsearch import helpers
root_base =  os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_base+'/lib/')
sys.path.append(root_base)
from zhanqun_sitename import zhanqun_resource_dict
from kombu import Exchange, Queue
from mooncake_log import log
from search_instance import elastic_sao
from search_instance import bs_searcher as searcher
from snownlp import SnowNLP
from pygflags import gflags
from esm import esm
import traceback
TOKEN="030000cf9f3bdec7189390cda9398dca"

Q_INDEX = 'zhanqun_celery_landingpage_index'
Q_SITE = 'zhanqun_celery_landingpage_site'
Q_DOC = 'zhanqun_celery_landingpage_doc'

CELERY_DEFAULT_QUEUE = 'zhanqun_celery'
CELERY_QUEUES = (
    Queue(Q_INDEX, Exchange('zhanqun_celery'), routing_key=Q_INDEX+'.'),
    Queue(Q_DOC, Exchange('zhanqun_celery'), routing_key=Q_DOC+'.'),
    Queue(Q_SITE, Exchange('zhanqun_celery'), routing_key=Q_SITE+'.')
)

reload(sys)
sys.setdefaultencoding('utf8')

fw = open('/apps3/yuebin/zhanqun-search/f.log', 'a')
app = Celery('celery_landingpage',
        broker='redis://52a34c024547489a:0s9j09sHSj1sdf1oL@52a34c024547489a.m.cnbja.kvstore.aliyuncs.com:6379/4')

logger = log.init_log(True ,"query_landing_page")

FLAGS = gflags.FLAGS

html_remove = re.compile(r'<[^>]+>',re.S)
parser=HTMLParser.HTMLParser()

pool = HTTPConnectionPool('internal-zhanqun-search.baijiahulian.com', maxsize=100)

zhanqun_dict = {
    "yuanxiao": u"院校",
    "org": u"机构",
    "zhongkao": u"中考",
    "zkyuwen": u"中考语文",
    "zkshuxue": u"中考数学",
    "zkyingyu": u"中考英语",
    "zkwuli": u"中考物理",
    "zkhuaxue": u"中考化学",
    "zkshengwu": u"中考生物",
    "zklishi": u"中考历史",
    "zkzhengzhi": u"中考政治",
    "gaokao": u"高考",
    "gkyuwen": u"高考语文",
    "gkshuxue": u"高考数学",
    "gkyingyu": u"高考英语",
    "gkwuli": u"高考物理",
    "gkhuaxue": u"高考化学",
    "aoshu": u"奥数",
    "xiaoxue": u"小学",
    "yikao": u"艺考",
    "chengrengaokao": u"成人高考",
    "gre": u"GRE",
    "gmat": u"GMAT",
    "sat": u"SAT",
    "act": u"ACT",
    "ielts": u"雅思",
    "tofel": u"托福",
    "toefl": u"托福",
    "wudao": u"舞蹈",
    "shufa": u"书法",
    "changge": u"唱歌",
    "huihua": u"绘画",
    "biaoyan": u"表演",
    "taodi": u"陶笛",
    "sakesi": u"萨克斯",
    "guzheng": u"古筝",
    "gangqin": u"钢琴",
    "xiaotiqin": u"小提琴",
    "shoufengqin": u"手风琴",
    "gu": u"鼓",
    "erhu": u"二胡",
    "kaoyan": u"考研",
    "siliuji": u"四六级",
    "english": u"英语",
    "french": u"法语",
    "japanese": u"日语",
    "german": u"德语",
    "korean": u"韩语",
    "italian": u"意大利语",
    "spanish": u"西班牙语",
    "cook": u"烹饪",
    "xingzuo": u"星座",
    "taluo": u"塔罗牌",
    "tiaojiu": u"调酒",
    "chahua": u"插花",
    "mofang": u"魔方",
    "coffee": u"咖啡",
    "yuanyi": u"园艺",
    "memory": u"记忆力",
    "dongman": u"动漫",
    "zhouyi": u"周易",
    "coding": u"编程",
    "magic": u"魔术",
    "youshengxiao": u"幼升小",
    "kongshoudao": u"空手道",
    "pingpang": u"乒乓球",
    "mba": u"MBA",
    "guoxue": u"国学",
    "youyong": u"游泳",
    "yujia": u"瑜伽",
    "sheji": u"设计",
    "licai": u"理财",
    "diaosu": u"雕塑",
    "erge": u"儿歌",
    "wushu": u"武术",
    "tutor": u"家教",
    "gongwuyuan": u"公务员",
    "daoyou": u"导游",
    "yingyangshi": u"营养师",
    "dianzishangwu": u"电子商务",
    "putonghua": u"普通话",
    "jiashiyuan": u"驾驶员",
    "kuaiji": u"会计",
    "jingjishi": u"经济师",
    "shenjishi": u"审计师",
    "shuiwushi": u"税务师",
    "licaishi": u"理财规划师",
    "jingsuanshi": u"精算师",
    "jianzaoshi": u"建造师",
    "acca": u"ACCA",
    "jisuanjidengji": u"计算机等级认证",
    "ncre": u"计算机等级认证",
    "microsoft": u"微软认证",
    "cisco": u"思科认证",
    "yishi": u"执业医师",
    "hushi": u"护士",
    "zhongyi": u"中医医师",
    "zhuanshengben": u"专升本",
    "bec": u"商务英语",
    "pets": u"公共英语",
    "toeic": u"托业",
    "fanyi": u"口译笔译",
    "jita": u"吉他",
    "yasi": u"雅思",
    "zuowen": u"作文",
    "qiuzhi": u"求职",
    "cet": u"四六级",
    "sifa": u"司法考试",
    "ntce": u"教师资格证",
    "jzs2": u"二级建造师",
    "xlzx": u"心理咨询师",
    "sheying": u"摄影",
    "dota": u"刀塔",
    "article": u"原创文章",
    "bxb": u"补习班",
    "kztk": u"考证题库",
    "cxy": u"程序员"
    }
zhanqun_dict = dict((value, key) for key, value in zhanqun_dict.iteritems())


def generate_common_doc(query, prefix, sitename):
    img_ptr = random.randint(1,20)
    if img_ptr == 8:
        img_ptr=1
    img_url = "http://file.gsxservice.com/zhanqun/static/images/list/%s.jpg" % img_ptr
    
    merge_content = '<img src="%s"  alt="%s %s"/>' % (img_url,query, sitename)
    
    m = hashlib.md5()
    m.update(query)
    qid = m.hexdigest()
    
    param = {
        "query":query,
        "query_list":[sitename],
        "fields":["title"],
        "offset":0,
        "size":50
    }

    if prefix != "zuowen":
        param["except_subject"] = ["作文 作文"]

    r = pool.request('GET', '/v1/retrieve' ,fields = {"token":TOKEN,"params":urllib.quote_plus(json.dumps(param))})
    r = json.loads(r.data)

    records = r["data"]['records']
    original_records = r['data']['records']
    if len(records) == 0:
        return  None

    #random.seed(qid)
    records = random.sample(records, min(5,len(records)))
     
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

        content = html_remove.sub('',parser.unescape(content)).strip()
        
        try:
            s = SnowNLP(content)
            sents = s.summary(10) 
        except:
            continue

        sub_content = "，".join(sents)
        xurl = 'http://www.genshuixue.com/i-%s/p/%s' % (prefix,doc['id'])

        merge_content += '''
        <a class='link-x' href='http://www.genshuixue.com/i-%s/p/%s'><h3><b>%s [点击查看原文]</b></h3></a>
        <hr>
        <div>%s...</div>
        <br>
        ''' % (prefix,doc['id'],title,sub_content)
        
    
    current_datetime = str(datetime.datetime.now()).split('.')[0]
    
    extra_records = random.sample(original_records, min(15,len(original_records)))
    merge_content += '<br>【%s】推荐阅读<br><div class="clearfix">' % query
    for r in extra_records:
        title =  r["content"]['title']
        merge_content+= '''<a href="http://www.genshuixue.com/i-%s/p/%s" class="link-x-a-highlight" target="_blank">%s</a>''' %(prefix,r['id'],title)

    merge_content+='</div>'
    
    param = {
        "query":query,
        "subject":"%s 问答" % sitename,
        "offset":0, "size":10
    }

    m.update(query)

    #r = searcher.retrieve(param)
    r = pool.request('GET', '/v1/retrieve' ,fields = {"token":TOKEN,"params":urllib.quote_plus(json.dumps(param))})
    r = json.loads(r.data)
    records = r["data"]['records']
    
    extra_records = random.sample(records, min(5,len(records)))
    merge_content += '<br>【%s】相关问答<br><br><div class="clearfix">' % query
    for r in extra_records:
        if 'highlight' in doc:
            title = doc['highlight']['title'][0]
        else:
            title = doc["content"]['title']
        title = "【%s】%s [点击查看原文]" %(title,r['content']['question_detail'])

        qa_content = ''
        ans = r['content']['answers']
        random.shuffle(ans) 
        for q in ans[:2]:
            try:
                qcontent = html_remove.sub('',parser.unescape(q['content'])).strip()
                qa_content+= '<div>%s</div>' % qcontent[:200]
            except:
                traceback.print_exc()
        
        xurl = 'http://www.genshuixue.com/i-%s/p/%s' % (prefix, r['id'])
        qa = '''
        <a class='link-x' href='http://www.genshuixue.com/i-%s/p/%s'><h3><b>%s</b></h3></a>
        <hr>
        <div>%s</div>
        <br>''' % (prefix,r['id'],title,qa_content.strip())
        merge_content+=qa

    merge_content+='</div>'


    extra_records = random.sample(records, min(10,len(records)))
    merge_content += '<br>【%s】推荐问答<br><div class="clearfix">' % query
    for r in extra_records:
        title =  r['content']['title']
        merge_content+= '''<a href="http://www.genshuixue.com/i-%s/p/%s" class="link-x-a-highlight" target="_blank">%s</a>''' %(prefix,r['id'],title)

    merge_content+='</div>'
    
    merge_content += '<br>【%s】推荐搜索<br><div class="clearfix">' % query

    oq_params = {"query":query, "size":10, "extra":sitename,"token_src":"query_landingpage"}
    r = pool.request('GET', '/v1/original_query' ,fields = {"token":TOKEN,"params":urllib.quote_plus(json.dumps(oq_params))})
    r = json.loads(r.data)

    query_keywords = []
    
    for q in r["data"]["records"]:
        q = q['query']
        query_keywords.append(q)
        m = hashlib.md5()
        m.update(q)
        inner_qid = m.hexdigest()
        merge_content+= '''<a href="http://www.genshuixue.com/i-%s/x/%s.html" class="link-x-a-highlight" target="_blank">%s</a>''' %(prefix,inner_qid,q)
    merge_content += '</div>'
    
    final_record['status'] = 3
    final_record['title'] = query
    final_record['id'] = qid
    final_record['content'] = merge_content
    final_record['source'] = 'QLP'
    final_record['date'] = current_datetime.split(' ')[0]
    final_record['subject'] = '%s@跟谁学' % sitename
    final_record['class'] = 'QLPV2'
    
    original = {"content":{},"taskid":"","update_time":""}
    
    original['content']['keywords'] = ",".join(query_keywords[:10])

    original['content']['class'] = "QLPV2"
    original['content']['title'] = query
    original['content']['content'] = merge_content
    original['content']['date'] = final_record['date']
    original['content']['source'] = '%s@跟谁学' % sitename

    final_record['original'] = json.JSONEncoder().encode(original)
    return final_record

def generate_jita_doc(query,prefix,sitename):
    img_urls= [
        "http://file.gsxservice.com/zhanqun/static/images/jita/jay.jpg",
        "http://file.gsxservice.com/zhanqun/static/images/jita/banner.png",
        "http://file.gsxservice.com/zhanqun/static/images/jita/xuwei.jpg",
        "http://file.gsxservice.com/zhanqun/static/images/jita/zhangxuan.jpg"]
    img_url = random.sample(img_urls,1)[0]
    merge_content = '<img src="%s"  alt="%s"/>' % (img_url,query)
    param = {
        "query":query,
        "subject":"吉他 吉他谱",
        "offset":0, "size":20
    }
    m = hashlib.md5()
    m.update(query)
    qid = m.hexdigest()
    r = pool.request('GET', '/v1/retrieve' ,fields = {"token":TOKEN,"params":urllib.quote_plus(json.dumps(param))})
    r = json.loads(r.data)
    
    jita_records = r['data']['records']
    jita_records = random.sample(jita_records, min(10,len(jita_records)))
    
    merge_content += '<br><a href="http">【%s】推荐吉他谱</a><br><div class="clearfix">' % query
    for r in jita_records:
        merge_content+= '''<a href="http://www.genshuixue.com/i-%s/p/%s" class="link-x-a-highlight" target="_blank">%s</a>''' %(prefix,r['id'],r['content']['title'])
    merge_content += '</div><hr><br>'
    param = {
        "query":query,
        "subject":"吉他 吉他资讯",
        "offset":0, "size":20
    }

    #r = searcher.retrieve(param)
    r = pool.request('GET', '/v1/retrieve' ,fields = {"token":TOKEN,"params":urllib.quote_plus(json.dumps(param))})
    r = json.loads(r.data)
    records = r["data"]['records']
    original_records = r['data']['records']
    
    #random.seed(qid)
    records = random.sample(records, min(5,len(records)))
    final_record = None
    for doc in records:
        if 'highlight' in doc:
            title = doc['highlight']['title'][0]
        else:
            title = doc['content']['title']
        content = doc['content']['content']
        content = html_remove.sub('',parser.unescape(content)).strip()
        try:
            s = SnowNLP(content)
            sents = s.summary(10) 
        except:
            continue

        sub_content = "，".join(sents)
        merge_content += '''
        
        <a class='link-x' href='http://www.genshuixue.com/i-%s/p/%s'><h3><b>%s [点击查看全文]</b></h3></a>
        <hr>
        <div>%s...</div>
        <br>
        ''' % (prefix,doc['id'],title,sub_content)
        
        final_record = doc
    
    current_datetime = str(datetime.datetime.now()).split('.')[0]
    
    extra_records = random.sample(original_records, min(15,len(original_records)))
    merge_content += '<br><a href="http">【%s】推荐阅读</a><br><div class="clearfix">' % query
    for r in extra_records:
        title =  r['content']['title']
        merge_content+= '''<a href="http://www.genshuixue.com/i-%s/p/%s" class="link-x-a-highlight" target="_blank">%s</a>''' %(prefix,r['id'],title)
    merge_content+='</div>'
    
    param = {
        "query":query,
        "subject":"吉他 问答",
        "offset":0, "size":10
    }

    m.update(query)

    #r = searcher.retrieve(param)
    r = pool.request('GET', '/v1/retrieve' ,fields = {"token":TOKEN,"params":urllib.quote_plus(json.dumps(param))})
    r = json.loads(r.data)
    records = r['data']['records']
    
    extra_records = random.sample(records, min(5,len(records)))
    merge_content += '<br>【%s】问答<br><div class="clearfix">' % query
    for r in extra_records:
        if 'highlight' in doc:
            title = doc['highlight']['title'][0]
        else:
            title = doc['content']['title']
        title = "【%s】%s [点击查看全文]" %(title,r['content']['question_detail'])
        qa_content = ''
        ans = r['content']['answers']

        random.shuffle(ans) 
        for q in ans[:2]:
            qcontent = html_remove.sub('',parser.unescape(q['content'])).strip()
            qa_content+= '%s...' % qcontent[:200]

        qa = '''
        <a class='link-x' href='http://www.genshuixue.com/i-%s/p/%s'><h3><b>%s</b></h3></a>
        <hr>
        <div>%s...</div>
        <br>''' % (prefix,r['id'],title,qa_content)
        merge_content+=qa

    merge_content+='</div>'

    extra_records = random.sample(records, min(10,len(records)))
    merge_content += '<br>【%s】推荐问答<br><div class="clearfix">' % query
    for r in extra_records:
        title =  r['content']['title']
        merge_content+= '''<a href="http://www.genshuixue.com/i-%s/p/%s" class="link-x-a-highlight" target="_blank">%s</a>''' %(prefix,r['id'],title)

    merge_content+='</div>'
    
    merge_content += '<br>【%s】推荐搜索<br><div class="clearfix">' % query
    
    oq_params = {"query":query, "size":10, "extra":sitename,"token_src":"query_landingpage"}

    r = pool.request('GET', '/v1/original_query' ,fields = {"token":TOKEN,"params":urllib.quote_plus(json.dumps(oq_params))})
    r = json.loads(r.data)
    query_keywords = [] 
    for q in r["data"]["records"]:
        q = q['query']
        query_keywords.append(q)
        m = hashlib.md5()
        m.update(q)
        inner_qid = m.hexdigest()
        merge_content+= '''<a href="http://www.genshuixue.com/i-%s/x/%s.html" class="link-x-a-highlight" target="_blank">%s</a>''' %(prefix,inner_qid,q)
    merge_content += '</div>'
    

    final_record['status'] = 3
    final_record['title'] = query
    final_record['id'] = qid
    final_record['content'] = ""
    final_record['source'] = '吉他@跟谁学'
    final_record['date'] = current_datetime.split(' ')[0]
    final_record['subject'] = '吉他@跟谁学'
    final_record['class'] = 'QLPV2'
    
    
    original = {"content":{},"taskid":"","update_time":""}
    
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
        #try:
        if 1:
            doc = generate_jita_doc(query,'jita',"吉他")    
            print elastic_sao.index(body=doc, index='corpora_index_v2_b',doc_type='normal',id = doc['id'])
        #except Exception,w:
        #    logger.info(w)
        #    continue
        exit()

def load_query_black_list(query_black_index):
    filename = "./data/blackquery.dat"
    logger.info("load black query from %s" % filename)
    with open(filename,'r') as f:
        data = f.readlines()
        logger.info("total size %s" % len(data))
        for i in data:
            query = i.strip()
            query_black_index.enter(query)
        query_black_index.fix() 

#@app.task(queue = Q_INDEX)
def indexing(doc):
    ret = elastic_sao.index(body=doc, index='corpora_index_v2_b',doc_type='normal',id = doc['id'])
    logger.info(ret)
    return ret

def get_site(query):

    b_body={
        "sort": [
            {
                "_id": "desc"
            }
        ],
        "query": {
            "bool": {
                "should": [],
                "must_not": [
                    {
                        "terms": {
                            "status": [
                                "3"
                            ]
                        }
                    }
                ],
                "must": [
                    {
                        "multi_match": {
                            "query": query,
                            "type": "most_fields",
                            "fields": [
                                "title"
                            ]
                        }
                    }
                ]
            }
        },
        "from": 0,
        "size": 50
    }
    res = elastic_sao.search(index='corpora_index_v2_b',body=b_body)
    _dict = {}
    for each in res['hits']['hits']:
        k = each['_source']['subject'].split()[0]
        if _dict.has_key(k):
            _dict[k] +=1
        else:
            _dict[k] = 1
    max_name = ''
    max_count = 0
    for k,v in _dict.iteritems():
        if v > max_count: 
            max_name = k
            max_count = v
    site_prefix = ''
    sitename = ''
    if zhanqun_dict.has_key(max_name):
        site_prefix = zhanqun_dict[max_name]
        sitename = max_name
    return site_prefix,sitename

#@app.task(queue = Q_DOC)
def gen_doc_for_query(query):
    #get_site(query)
    site_prefix,sitename = get_site(query)
    if not sitename:
        return
    try:
        if site_prefix == "jita":
            doc = generate_jita_doc(query,site_prefix,sitename)
        else:
            doc = generate_common_doc(query,site_prefix,sitename)
        if doc:
            url = "http://www.genshuixue.com/i-%s/x/%s.html" % (site_prefix,doc['id'])
            indexing(doc)
            print json.dumps(doc)
            print url
            #fw.write(url + '\n')
            #fw.flush()
    except:
        traceback.print_exc()

#@app.task(queue = Q_SITE)
def gen_site(site_prefix, sitename):
    sitename = sitename.strip()
    query_black_index = esm.Index()
    load_query_black_list(query_black_index)

    r = searcher.dump_query(sitename)
    for i in r:
        query = i['_source']['query']
        
        size = len(query_black_index.query(query))
        if size > 0:
            logger.info("[%s] DELETE %s" % (sitename,query))
            continue
        else:
            logger.info("[%s] ACCEPT %s" % (sitename,query))
        gen_doc_for_query(query,site_prefix, sitename)

if __name__ == '__main__':
    FLAGS(sys.argv)
    ignore = ['172','tofel']
    # for site, value in sorted(zhanqun_resource_dict.items(), key=lambda x: random.random()):
    #     if site in ignore:
    #         logger.info("ignore %s" % site)
    #         continue
    #     site_prefix = site
    #     sitename = value['name']
    #     gen_site(site_prefix,sitename)
    #     print "####%s" % sitename
    for line in open('/apps3/yuebin/zhanqun-search/else_rmnum_unip.txt'):
        query = unicode(line.strip())
        gen_doc_for_query(query)
        break
