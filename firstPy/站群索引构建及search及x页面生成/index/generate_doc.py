#!/usr/bin/env python
#coding: utf8
import urllib
import re
import datetime
import json
import HTMLParser
html_remove = re.compile(r'<[^>]+>',re.S)
html_parser=HTMLParser.HTMLParser()

def get_schema():
    schema_info = "http://schema.baijiahulian.com/get_schema_info/"
    schema_attr = "http://schema.baijiahulian.com/get_schema_attr/"

    schema_info_json = json.loads(urllib.urlopen(schema_info).read())
    schema_attr_json = json.loads(urllib.urlopen(schema_attr).read())

    schema_id2name = {}
    for item in schema_info_json:
        pid = schema_info_json[item]["id"]
        name =  schema_info_json[item]["desc"]
        schema_id2name[str(pid)] = name
    return schema_id2name

def pure_title(title):
    title = title.replace("跟谁学雅思","").strip()
    title = html_remove.sub('',html_parser.unescape(title))
    title = title.strip()
    return title

def generate_doc(record, schema_id2name):
    if 'content' in record and record['content']:
        content = record['content']
    else:
        print ("L1-content is None [%s]" % record)
        return None
    title = content.get('title', None)
    if title == None:
        print ("title is None [%s]" % record)
        return None
    else:
        title = pure_title(title)
    if 'content' in content: 
        index_content = content.get('content', None)
        if index_content == None:
            print ("content is None [%s]" % record)
            return None
    else:
        index_content = ""

    subject = content.get('subject', None)
    if subject == None:
        print ("subject is None, return [%s]" % record)
        return None
    
    date = content.get('date', None)
    if not date:
        date = content.get('publish_time', '2015-01-01')

    date = re.findall('[0-9]+-[0-9]+-[0-9]+',date)
    if len(date) != 1:
        date = '2015-01-01'
    else:
        date = date[0]
    try:
        date = str(datetime.datetime.strptime(date,'%Y-%m-%d')).split(' ')[0]
        date = date.strip()
    except Exception,w:
        print (w)
        return None 
    

    db_id = record['id']
    if db_id == None:
        print ("db_id is None [%s]" % record)
        return None
    
    tag_tmp = content.get('tag', [])
    tag = []
    for i in tag_tmp:
        if i.strip() != "":
            tag.append(i)

    # 0 init
    # 1 top
    # 2 manual
    # 3 delete
    status = int(content.get('status', 0))

    bread_tmp = content.get('bread', [])
    bread = []
    for i in bread_tmp:
        if i.strip() != "":
            bread.append(i)

    db_id = str(db_id)
    c_class = str(record['class'])

    class_name = schema_id2name[c_class]

    class_list = []
    if c_class != "":
        class_list.append(c_class)
    
    subject += " %s" % class_name 

    index_content = html_remove.sub('',html_parser.unescape(index_content))
    
    if 'date' in record['content']:
        record['content']['date'] = date

    if 'publish_time' in record['content']:
        record['content']['publish_time'] = date
    
    record_json = json.JSONEncoder().encode(record)


    res = { 
            "id":db_id,
            "title":title,
            "subject":subject.strip(),
            "content":index_content.strip(),
            "tag":tag,
            "status":status,
            "date":date,
            "bread":bread,
            "original": record_json,
            "class":class_list,
            "source":content.get('source', '')
    }

    return res


def generate_wenda_tiku_doc(record, schema_id2name):
    if 'content' in record and record['content']:
        content = record['content']
    else:
        print ("L1-content is None [%s]" % record)
        return None
    title = content.get('title', None)
    if title == None:
        print ("title is None [%s]" % record)
        return None
    else:
        title = pure_title(title)
    if 'content' in content: 
        index_content = content.get('content', None)
        if index_content == None:
            print ("content is None [%s]" % record)
            return None
    else:
        index_content = ""

    subject = content.get('subject', None)
    if subject == None:
        print ("subject is None, return [%s]" % record)
        return None
   
    degree = content.get('degree', 0)
    category_id = content.get('category_id', 0)
    date = content.get('date', None)
    if not date:
        date = content.get('publish_time', '2015-01-01')

    date = re.findall('[0-9]+-[0-9]+-[0-9]+',date)
    if len(date) != 1:
        date = '2015-01-01'
    else:
        date = date[0]
    try:
        date = str(datetime.datetime.strptime(date,'%Y-%m-%d')).split(' ')[0]
        date = date.strip()
    except Exception,w:
        print (w)
        return None 
    

    db_id = record['id']
    if db_id == None:
        print ("db_id is None [%s]" % record)
        return None
    
    tag_tmp = content.get('tag', [])
    tag = []
    for i in tag_tmp:
        if i.strip() != "":
            tag.append(i)

    # 0 init
    # 1 top
    # 2 manual
    # 3 delete
    status = int(content.get('status', 0))

    bread_tmp = content.get('bread', [])
    bread = []
    for i in bread_tmp:
        if i.strip() != "":
            bread.append(i)

    db_id = str(db_id)
    c_class = str(record['class'])

    class_name = schema_id2name[c_class]

    #class_list = []
    #if c_class != "":
    #    class_list.append(c_class)
    
    #subject += " %s" % class_name 

    index_content = html_remove.sub('',html_parser.unescape(index_content))
    
    if 'date' in record['content']:
        record['content']['date'] = date

    if 'publish_time' in record['content']:
        record['content']['publish_time'] = date
    
    record_json = json.JSONEncoder().encode(record)


    res = { 
            "id":db_id,
            "title":title,
            "subject":subject.strip(),
            "degree":degree,
            "category_id":category_id,
            "status":status,
            "date":date,
            "original": record_json,
            "class":c_class
    }

    return res

