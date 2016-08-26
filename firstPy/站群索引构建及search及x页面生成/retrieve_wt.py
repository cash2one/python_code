#!/usr/bin/env python
# -*- coding:utf-8-*-

from elasticsearch import Elasticsearch,helpers
es = Elasticsearch()
import time,sys,json,datetime
reload(sys)
sys.setdefaultencoding('utf8')
indexname = "corpora_index_v2_b"
api_status = {
    "expires_day": "2018-12-25",
    "host": u"无",
    "version": "v1",
    "status": "active"
}
PER_PAGE_MAX = 20
PAGE_NUM_MAX = 10

token_pool = {
    "ee07935be825aae6199247804f8231ee":"zhanqun_fe_luna",
    "fa7d15c7cbdc15799a1ae3b65d4d8d9c":"sns_manager",
    "0e2fa653de0d5659660279a326e80a83":"online_test",
    "50b725294a4f32c229ee4455c7302f11":"aliyun_monitor",
    "570d99e4c85914470d914170d1e95144":"cms",
    "05a66d05007c4dbd5f9d92c4c8709de1":"kaoyan_app",
    "8b087a63f0761241b3be34cd530d41cf":"seo_shenjie",
    "e386bd2c08c82f97d28a6fb4b9427519":"hehongmei",

    "030000cf9f3bdec7189390cda9398dca":"query_landingpage",
    "091c230ebfe5beceb934addc0fdfdc0f":"yuanxiaoku",
    "e3947909092b355bc1496f48e85c4a19":"habo_zhanqun",
    "005a806011a1d331db57d1e33e79b884":"tiku",
    "c6d6839beff81b1a67966a5f55cfaad2":"wenda",
    "a73c0bb34ebbc85e8ee32e1b7c54d81b":"jingyan",
    "d98d7173a8e47e9e57fb0a8f61c3d9f7":"zhanqun_admin"
}


def verify_token(req_token):
    if req_token and req_token.strip() in token_pool:
        return token_pool[req_token.strip()]
    else:
        return False

def remove_field( p, key):
    if key in p:
        del p[key]

def __query_index_name():
    index_name = 'corpora_index_v2'
    master = "b"
    slave = "a"
    actual_index_name = index_name + '_' + master
    return actual_index_name

def get_retrieve_param(param):
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

    today = str(datetime.datetime.now()).split(" ")[0]
    b_body["bool"]["should"].append(
        {
            "function_score": {
                "script_score": {
                    "params": {"now": int(1000 * time.time())},
                    "script": "(0.08 / ((3.16*pow(10,-11)) * abs(now-doc['date'].date.getMillis()) + 0.05)) + 1.0"
                },
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


def get_subject(param):
    if 'subject' in param:
        subject = param['subject']
    else:
        subject = None

    if subject and type(subject) != list:
        subject = [subject]

    return subject


def retreive(params):
    
    result = {"code": -1, "data": None, "api": api_status, "message": ""}
    result["api"]["timestamp"] = time.time()
    if not params:
        result["error"] = "params error"
        print "params error"
        return
    try:
        params = json.loads(params)
    except Exception as w:
        print w
        result["message"] = "%s" % w
        result["code"] = 1
        return
    
    
    ts = time.time()
    b_body = get_retrieve_param(params)

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
        indexname = __query_index_name()

    subject = get_subject(params)

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
        amount = res['hits']['total']

        if 'raw' in params:
            return res

        for hit in res['hits']['hits']:
            id = hit['_source']['id']
            original = json.JSONDecoder().decode(hit['_source'].get('original', '{}'))
            hit['_source']['content'] = original['content']
            hit['_source']['es_score'] = hit['_score']
            if 'highlight' in hit:
                hit['_source']['highlight'] = hit['highlight']

            hit["_source"]['taskid'] = original['taskid']
            hit["_source"]['update_time'] = original['update_time']
            if 'class' in hit['_source']['content']:

                hit['_source']['class'] = hit['_source']['content']['class']
            else:
                hit['_source']['class'] = int(hit['_source']['class'][0])

            hit["_source"]["content"]["subject"] = hit["_source"]["subject"]

            remove_field(hit['_source'], 'original')
            remove_field(hit['_source'], 'title')
            remove_field(hit['_source'], 'source')
            remove_field(hit['_source'], 'tag')
            remove_field(hit['_source'], 'bread')
            remove_field(hit['_source'], 'date')
            remove_field(hit['_source'], 'subject')
            remove_field(hit['_source']['content'], 'class')
            remove_field(hit['_source']['content'], 'subject_class')
            remove_field(hit['_source']['content'], 'status')

            records.append(hit['_source'])

        ret['took'] = res['took']
        ret['total_amount'] = amount
        ret['records'] = records[:size]
    except Exception, w:
        print (w)
        ret['took'] = 0
        ret['code'] = 2
        ret['message'] = "%s" % w
        ret['total_amount'] = 0
        ret['records'] = []

    ret['size'] = len(ret['records'])
    te = time.time()
    total_time = (te - ts) * 1000.0

    if subject:
        subject_str = ','.join(subject)
    else:
        subject_str = None

    # print (
    #     "TYPE[retrieve]-TIME[%d]-ES_TIME[%d]-AMOUNT[%d]-QUERY[%s]-SUBJECT[%s]-TOKEN_SRC[%s]-PARAMS[%s]-UA[%s]" % (
    #     total_time, ret['took'], amount, params.get('query', None), subject_str, params.get("token_source", None), b_body,
    #     ua))

    #return ret
    
        
        
        
        
    result["data"] = ret

    result["code"] = result["data"]["code"]
    result["message"] = result["data"]["message"]
    del result["data"]["code"], result["data"]["message"]
    return json.dumps(result)
########################################################################################
def get_retrieve_wt_param(param):
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

    if 'subject' in param:
        subject = param['subject']
    else:
        subject = None

    if subject and type(subject) != list:
        subject = [subject]

    if 'tag' in param:
        tag = param['tag']
    else:
        tag = None

    size = min(PER_PAGE_MAX, int(param.get('size', 20)))
    offset = min(PAGE_NUM_MAX * PER_PAGE_MAX, int(param.get('offset', 0)))

    random = param.get('random', None)
    req_class = param.get('class', None)
    degree = param.get('degree', None)
    category_id = param.get('category_id', None)

    b_body = {"bool": {"must": [], "should": [], "must_not": []}}

    if req_class:
        b_body["bool"]["must"].append({"filtered": {"filter": {"terms": {"class": req_class}}}})

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

    if category_id:
        b_body["bool"]["must"].append({"filtered": {"filter": {"terms": {"category_id": category_id}}}})

    if degree:
        b_body["bool"]["must"].append({"filtered": {"filter": {"terms": {"degree": degree}}}})

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

    b_body["bool"]["must_not"].append({"terms": {"status": ["3"]}})  # delete

    sort_method = []

    # sort_method.append({"_score": { "order": "desc" }})
    sort_method.append({"_id": "desc"})

    # b_body = { "function_score" : {"query":b_body} ,"random_score" : {} }

    b_body = {
        "query": b_body,
        "sort": sort_method
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


def retrieve_wt(token, params):

    result = {"code": -1, "data": None, "api": api_status, "message": ""}
    result["api"]["timestamp"] = time.time()

    token_source = verify_token(token)
    if not token_source:
        result["message"] = "verify token faild"
        result["code"] = 1
        print "verify token faild"
        return

    if not params:
        result["error"] = "params error"
        print "params error"
        return
    try:
        params = json.loads(params)
        params["token_source"] = token_source
    except Exception as w:
        print w
        result["message"] = "%s" % w
        result["code"] = 1
        return

    ts = time.time()
    b_body = get_retrieve_wt_param(params)

    size = min(PER_PAGE_MAX, int(params.get('size', 20)))
    offset = min(PAGE_NUM_MAX * PER_PAGE_MAX, int(params.get('offset', 0)))

    if 'query' in params and params['query']:
        query = params['query'].strip()
    else:
        query = None

    if 'index' in params and params['index']:
        indexname = params['index']
    else:
        indexname = "wenda_tiku_v1"

    if 'content_fields' in params:
        content_fields = params['content_fields']
    else:
        content_fields = None

    subject = get_subject(params)

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
        amount = res['hits']['total']

        if 'raw' in params:
            return res

        for hit in res['hits']['hits']:
            id = hit['_source']['id']
            original = json.JSONDecoder().decode(hit['_source'].get('original', '{}'))
            hit['_source']['content'] = original['content']
            hit['_source']['es_score'] = hit['_score']
            if 'highlight' in hit:
                hit['_source']['highlight'] = hit['highlight']

            hit["_source"]['taskid'] = original['taskid']
            hit["_source"]['update_time'] = original['update_time']
            if 'class' in hit['_source']['content']:

                hit['_source']['class'] = hit['_source']['content']['class']
            else:
                hit['_source']['class'] = int(hit['_source']['class'][0])

            hit["_source"]["content"]["subject"] = hit["_source"]["subject"]

            remove_field(hit['_source'], 'original')
            remove_field(hit['_source'], 'title')
            remove_field(hit['_source'], 'source')
            remove_field(hit['_source'], 'tag')
            remove_field(hit['_source'], 'bread')
            remove_field(hit['_source'], 'date')
            remove_field(hit['_source'], 'subject')
            remove_field(hit['_source']['content'], 'class')
            remove_field(hit['_source']['content'], 'subject_class')
            remove_field(hit['_source']['content'], 'status')

            if content_fields:
                new_doc = {}
                for f in content_fields:
                    if f not in hit['_source']['content']:
                        continue
                    new_doc[f] = hit['_source']['content'][f]
            else:
                new_doc = hit['_source']['content']

            hit['_source']['content'] = new_doc
            records.append(hit['_source'])

        ret['took'] = res['took']
        ret['total_amount'] = amount
        ret['records'] = records[:size]
    except Exception, w:
        print (w)
        ret['took'] = 0
        ret['code'] = 2
        ret['message'] = "%s" % w
        ret['total_amount'] = 0
        ret['records'] = []

    ret['size'] = len(ret['records'])
    te = time.time()
    total_time = (te - ts) * 1000.0

    if subject:
        subject_str = ','.join(subject)
    else:
        subject_str = None

    # print (
    #     "TYPE[retrieve_wt]-TIME[%d]-ES_TIME[%d]-AMOUNT[%d]-QUERY[%s]-SUBJECT[%s]-TOKEN_SRC[%s]-PARAMS[%s]-UA[%s]" % (
    #     total_time, ret['took'], amount, params.get('query', None), subject_str, params.get("token_source", None), b_body,
    #     ua))

    #return ret
    
    
    result["data"] = ret

    result["code"] = result["data"]["code"]
    result["message"] = result["data"]["message"]
    del result["data"]["code"], result["data"]["message"]

    return json.dumps(result)

if __name__ == '__main__':
    token = "030000cf9f3bdec7189390cda9398dca"
    query = u'请问高考历史网络课堂和平时课堂笔记'
    sitename = u'高考'
    params = {
        "query": query,
        "query_list": [sitename],
        "fields": ["title"],
        "offset": 0,
        "size": 50
        }

    print u"搜索结果: "+retrieve_wt(token, json.dumps(params))