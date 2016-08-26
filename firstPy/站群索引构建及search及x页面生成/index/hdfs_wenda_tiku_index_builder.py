#!/usr/bin/env python
#coding: utf8
import re
import json
import urllib
import datetime
from elasticsearch import helpers
from elasticsearch import Elasticsearch
from generate_doc import generate_wenda_tiku_doc,get_schema
import os,sys

root_base =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_base+'/lib/')
sys.path.append(root_base)
from search_instance import elastic_sao


suffix = ""
INDEX_NAME = 'wenda_tiku_v1' + suffix

DOC_TYPE = 'normal'

THREAD_NUM = 2
CHUNK_SIZE = 500
LINES = 1000

def hdfs2local():
    today = str(datetime.datetime.now()).split(" ")[0].replace("-","")

    output = "/Users/bjhl/Documents/test/wenda2_xdf.res"

    print ("using local file: %s" % output)
    return output 

def genereate_actions(records,index_name,schema_id2name):
    for record in records:
        #try:
            try:
                record = generate_wenda_tiku_doc(record, schema_id2name)
            except Exception,w:
                print ("%s %s" %(w,record))
                continue

            if not record:
                continue
            yield {
                '_index': index_name,
                '_type': DOC_TYPE,
                '_id': record['id'],
                '_source': record }

def bulk_index(index_name, records, schema_id2name, debug = False):
    count = 0
    try:
        for success, info in helpers.parallel_bulk(es, 
                genereate_actions(records, index_name, schema_id2name),
                thread_count = THREAD_NUM,
                raise_on_error = False,
                chunk_size = CHUNK_SIZE):
            if not success: 
                #print ('Doc failed %s' % info)
                print ('Doc failed %s' % info)
            else:
                if debug:
                    print (info)
                count +=1
    except Exception, w:
        print (w)

    return count

def indexing(index_name, filename):
    schema_id2name = get_schema()
    total = 0
    with open(filename, 'r') as infile:
        lines = []
        for line in infile:
            item = line.strip().split("")
            if len(item)!=6:
                print ("error format: [%s]" % line)
                continue
            doc_class = item[1]

            doc = {}
            doc["id"] = item[0]
            doc["class"] = doc_class
            try:
                doc["content"] = json.JSONDecoder().decode(item[2])
            except:
                continue
            doc["source"] = item[3]
            doc["update_time"] = item[4]
            doc["taskid"] = item[5]

            lines.append(doc)
            if len(lines) > LINES:
                total += bulk_index(index_name, lines,schema_id2name)
                lines = []
                print ("current processed %s docs" % total)

        if len(lines) > 0:
            total += bulk_index(index_name, lines,schema_id2name)
    print ("total indexed [%s] docs" % total)

def put_mapping(es, index_name):
    newbody = '''
        {
            "normal": {
                "dynamic":"strict",
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
                    "original":{
                        "type":"string",
                        "index":"no"
                    },
                    "status":{
                        "type":"integer"
                    },
                    "degree":{
                        "type":"string",
                        "index":"not_analyzed"
                    },
                    "class":{
                        "type":"string",
                        "index":"not_analyzed"
                    },
                    "id":{
                        "type":"string",
                        "index":"not_analyzed"
                    },
                    "date":{
                        "type":"date"
                    },
                    "category_id": {
                        "type": "string",
                        "index":"not_analyzed"
                    },
                    "subject": {
                        "type": "string",
                        "index":"not_analyzed",
                        "boost": 8
                    }
                }
            }
        }
    '''
    es.indices.put_mapping(doc_type = DOC_TYPE, index = index_name, body = newbody, ignore_unavailable = True, allow_no_indices = True)


if __name__ == '__main__':
    begin =  '-' * 8 + 'BEGIN' + '-' * 8
    end =  '-' * 8 + 'END' + '-' * 8
    print (begin)

    es = elastic_sao

    actual_index_name = INDEX_NAME
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
    # ''' % actual_index_name

    print (cmd)
    os.system(cmd)


    put_mapping(es, actual_index_name)

    output = hdfs2local()
    indexing(actual_index_name, output)

    cmd = '''curl -XPUT http://localhost:9200/%s/_settings -d '{
                    "index" : {
                        "refresh_interval" : "1s"
                    }
             }'
          ''' % actual_index_name
    print (cmd)
    os.system(cmd)

    es.indices.refresh(index = actual_index_name)

    print (end)
