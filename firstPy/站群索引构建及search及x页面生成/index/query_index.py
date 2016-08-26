#!/usr/bin/env python
#-*- coding:utf-8-*-
import hashlib
import os
import sys
from elasticsearch import helpers,Elasticsearch
reload(sys)
sys.setdefaultencoding('utf8')

DOC_TYPE = 'query'

THREAD_NUM = 3
CHUNK_SIZE = 200
LINES =2000

es = Elasticsearch()

m = hashlib.md5()


def genereate_actions(records,index_name):
    for record in records:
        #try:
            yield {
                '_index': index_name,
                '_type': DOC_TYPE,
                '_id': record['id'],
                '_source': record }

def bulk_index(index_name, records, debug = False):
    count = 0
    try:
        for success, info in helpers.parallel_bulk(es, 
                genereate_actions(records, index_name),
                thread_count = THREAD_NUM,
                raise_on_error = False,
                chunk_size = CHUNK_SIZE):
            if not success: 
                print ('Doc failed %s' % info)
            else:
                if debug:
                    print (info)
                count +=1
    except Exception, w:
        print (w)

    return count

def indexing(index_name, filename):
    total = 0
    with open(filename, 'r') as infile:
        lines = []
        for line in infile:
            item = line.strip().split("\t")
            query = item[0].strip()
            try:
                pc_pv = int(item[1])
                pc_adpv = int(item[2])
                pc_show = int(item[3])

                wise_pv = int(item[4])
                wise_adpv = int(item[5])
                wise_show = int(item[6])
                pv = pc_pv+wise_pv

            except:
                continue
            m.update(query)
            qid = m.hexdigest()

            doc = {
                    'query':query.decode(),
                    'pv':pv,
                    'id':qid,
                    'pc_pv':pc_pv,
                    'pc_adpv':pc_adpv,
                    'pc_show':pc_show,
                    'wise_pv':wise_pv,
                    'wise_adpv':wise_adpv,
                    'wise_show':wise_show
            }
            
            lines.append(doc)
            if len(lines) > LINES:
                total += bulk_index(index_name, lines)
                lines = []
                print ("current processed %s docs" % total)

        if len(lines) > 0:
            total += bulk_index(index_name, lines)
    print ("total indexed [%s] docs" % total)


def create(INDEX_NAME):
    es.indices.delete(index = INDEX_NAME, ignore = [404])
    es.indices.create(index = INDEX_NAME)
    mapping = '''
    {
      "query":{
        "properties":{
            "query": {
                        "boost": 5.0,
                        "store": "no",
                        "analyzer" : "ik_max_word",
                        "search_analyzer": "ik_smart",
                        "include_in_all": "true",
                        "type": "string",
                        "term_vector" : "with_positions_offsets"},
            "pv": {"boost": 1.0,
                         "store": "yes",
                         "type": "integer"
                         },
            "wise_pv": {"boost": 1.0,
                         "store": "yes",
                         "type": "integer"
                         },
            "wise_adpv": {"boost": 1.0,
                         "store": "yes",
                         "type": "integer"
                         },
            "wise_show": {"boost": 1.0,
                         "store": "yes",
                         "type": "integer"
                         },
            "pc_pv": {"boost": 1.0,
                         "store": "yes",
                         "type": "integer"
                         },
            "pc_adpv": {"boost": 1.0,
                         "store": "yes",
                         "type": "integer"
                         },
            "pc_show": {"boost": 1.0,
                         "store": "yes",
                         "type": "integer"
                         }
        }
      }
    }
    '''
    print mapping
    es.indices.put_mapping(doc_type = DOC_TYPE, index = INDEX_NAME, body = mapping.strip(), ignore_unavailable = True, allow_no_indices = True)


if __name__ == '__main__':
    index_name = "original_query"
    #create(index_name)

    indexing(index_name,'/Users/bjhl/Documents/test/query.utf8')
