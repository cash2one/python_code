#!/usr/bin/env python
#coding: utf8
import re
import json
import urllib
import datetime
from elasticsearch import helpers
from elasticsearch import Elasticsearch
from generate_doc import generate_doc,get_schema
import os,sys
reload(sys)
sys.setdefaultencoding("utf-8")
root_base =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_base+'/lib/')
sys.path.append(root_base)
#from search_instance import elastic_sao

elastic_sao = Elasticsearch()
luna_sql_service = None


suffix = ""
INDEX_NAME = 'corpora_index_v2' + suffix
REDIS_KEY_DBUFFER_POINTER = 'luna_dbuffer_pointer_online' + suffix


PROCESS_CLASS = None

DOC_TYPE = 'normal'

THREAD_NUM = 2
CHUNK_SIZE = 500
LINES = 1000

import MySQLdb
conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="root",db="myblog", charset="utf8", port = 3306)
cursor = conn.cursor()

def hdfs2local():
    today = str(datetime.datetime.now()).split(" ")[0].replace("-","")
    path = "/Users/bjhl/Documents/zhanqun/%s/*" % today
    #print (path)
    
    output = "/Users/bjhl/Documents/test/sina_gaokao"
    
    
    #if FLAGS.ielts:
    #    cmd = "awk -F  '{ if ($2== 17 || $2 ==18 || $2 == 47) print $0}' data2process.ori.dat >data2process.dat"
    #    print (cmd)
    #    os.system(cmd)
    #    output = "data2process.dat"
    print ("using local file: %s" % output)
    return output 

def genereate_actions(records,index_name):
    for record in records:
        yield {
            '_index': index_name,
            '_type': DOC_TYPE,
            '_id': record['id'],
            '_source': record }

def bulk_index(index_name, records, debug = False):
    count = 0
    # for content in genereate_actions(records, index_name, schema_id2name):
    #     count += 1
    #     print count
    #     print json.dumps(content)
    try:
        #print 'ok'
        for success, info in helpers.parallel_bulk(es,
               genereate_actions(records, index_name),
               thread_count=THREAD_NUM,
               raise_on_error=False,
               chunk_size=CHUNK_SIZE):
            if not success:
                #print ('Doc failed %s' % info)
                print 'Doc failed %s' % info
                #break
            else:
                if debug:
                    print info
                print '执行成功'
                #break
                count +=1
    except Exception, w:
        print w

    return count

def indexing(index_name):
    total = 0
    sql = '''select * from myblog'''
    cursor.execute(sql)
    lines= []
    for (id, title, category, summury, body, timestamp,source,status) in cursor.fetchall():
        doc = {}
        doc["id"] = id
        doc["title"] = title
        doc["category"] = category
        doc["summury"] = summury
        doc["timestamp"] = timestamp
        doc["source"] = source
        doc["body"] = body
        doc["status"] = status

        lines.append(doc)
        if len(lines) > LINES:
            total += bulk_index(index_name, lines)
            lines = []
        #print len(lines)
        #print  schema_id2name
    if len(lines) > 0:
        print '已执行。。'
        total += bulk_index(index_name, lines)

def put_mapping(es, index_name):
    newbody = '''
        {
            "normal": {
                "properties": {
                    "title": {
                        "type": "string",
                        "store": "no",
                        "term_vector": "with_positions_offsets",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart",
                        "include_in_all": "true",
                        "boost": 5
                    },
                    "summury":{
                        "type":"string",
                        "index":"no"
                    },
                    "timestamp":{
                        "type":"string",
                        "index":"not_analyzed"
                    },
                    "status":{
                        "type":"integer"
                    },
                    "source":{
                        "type":"string",
                        "index":"not_analyzed"
                    },
                    "body": {
                        "type": "string",
                        "store": "no",
                        "term_vector": "with_positions_offsets",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart",
                        "include_in_all": "true",
                        "boost": 1
                    },
                    "category": {
                        "type": "string",
                        "store": "no",
                        "term_vector": "with_positions_offsets",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_smart",
                        "include_in_all": "true",
                        "boost": 8
                    }
                }
            }
        }
    '''
    '''Elasticsearch可以根据数据中的新字段来创建新的映射.
    在正式数据写入之前我们可以自己定义Mapping, 等数据写入时，会按照定义的Mapping进行映射。
    如果后续数据有其他字段时，Elasticsearch会自动进行处理。'''

    es.indices.put_mapping(doc_type = DOC_TYPE, index = index_name, body = newbody, ignore_unavailable = True, allow_no_indices = True)
    print 'ok'


if __name__ == '__main__':
    begin = '-' * 8 + 'BEGIN' + '-' * 8
    end = '-' * 8 + 'END' + '-' * 8
    print (begin)

    es = elastic_sao

    master = "a"
    slave = "b"

    actual_index_name = 'myblog'
    print ("index_name %s" % actual_index_name)


    cmd = '''curl -XPUT http://localhost:9200/%s/_settings -d '{
                    "index" : {
                        "refresh_interval" : "-1"
                    }
             }'
          ''' % actual_index_name
    # cmd = '''curl -XPUT http://localhost:9200/%s/ -d '{
    #                 "settings":{
    #                 }
    #    }'
    #     ''' % actual_index_name
    # cmd = '''curl -XDELETE http://localhost:9200/%s/ -d '{
    #                 "settings":{
    #                 }
    #    }'
    # ''' % actual_index_name
    #print (cmd)
    os.system(cmd)

    put_mapping(es, actual_index_name)

    output = hdfs2local()
    indexing(actual_index_name)

    cmd = '''curl -XPUT http://localhost:9200/%s/_settings -d '{
                    "index" : {
                        "refresh_interval" : "1s"
                    }
             }'
          ''' % actual_index_name
    print (cmd)
    os.system(cmd)
    #
    es.indices.refresh(index=actual_index_name)

    print (end)
