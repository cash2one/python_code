#ecoding:utf-8
import json
import traceback
import sys
import datetime
import redis
from collections import defaultdict

reload(sys)
sys.setdefaultencoding("utf-8")

#db_spider = factory.get_db('spider')

ID_GEN = 'zhanqun_id_generator'
ID_RECORD = 'zhanqun_taskid_record'
client = redis.StrictRedis(host='52a34c024547489a.m.cnbja.kvstore.aliyuncs.com', port=6379, db=12, password='52a34c024547489a:0s9j09sHSj1sdf1oL')

HOST = '52a34c024547489a.m.cnbja.kvstore.aliyuncs.com'
DB = 12
PORT = 6379
PASSWD='52a34c024547489a:0s9j09sHSj1sdf1oL'
client = redis.StrictRedis(host=HOST, port=PORT, db=DB, password=PASSWD)
img_url_rec = 'zhanqun_pic_rec'

def get_id(task_id):
    if client.hexists(ID_RECORD, task_id):
        return client.hget(ID_RECORD, task_id)
    else:
        id = client.incr(ID_GEN)
        client.hset(ID_RECORD, task_id, id)
        return id

def parse_source(url):
    _list = ['114', 'xdf', 'baidu', '360', 'so', 'iask']
    for s in _list:
        if s in url:
            return s
    return 'other'

#category_id_dic = db_spider.fetch_by_map("select id, map_id from db_external.wenda_category", "id", "map_id")

category_id_dic = {
    u'语文': ['161', '167'],
    u'高等院校': [],
    u'化学': ['266', '297'],
    u'资格考试': [],
    u'工程学': [],
    u'升学入学': [],
    u'农业': [],
    u'中小学作业': [],
    u'留学出国': [],
    u'外语': [],
    u'学习方法': [],
    u'公务员': [],
    u'生物': [],
    u'校园话题': [],
    u'数学': [],
    u'人文社科': [],
    u'理工学科': [],
    u'家庭教育': [],
    u'物理': [],
}
def read(data):
    dic = defaultdict(int)
    sub_class = 34
    fw = open('%s.res'%(data.split('/')[-1]), 'w')
    for line in open(data):
        (taskid, result) = line.strip().split('$$$$$')
        data = json.loads(result)
        title = data.get('title', '')
        if not title:
            continue
        #type = data.get('type', '')
        category = data.get('category_id','')
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        source = data.get('source', '')
        category_id_list = category_id_dic.get(category, [])
        answers = data.get('answers', [])
        if not answers:#or len(answer) < 20:
            continue
        answer_list = []
        for _data in answers:
            _dic = {
                'content': _data['content'],
                'create_time': _data['date'],
                'user_name':  _data['name'],
                'is_accept': 0,
            }
            print _data['date']
            answer_list.append(_dic)
        #id = get_id(taskid)
        print data.get('create_date', '')
        content_dic = {
            'category_id': category_id_list,    #类目ID列表
            'url': data['url'],
            'title': title,                     #标题
            'subject': '主站问答',
            'class': sub_class,
            'data_weight': 0,
            'question_detail': data.get('question_detail', ''),         #问题描述
            'create_time': data.get('create_date', ''),
            'create_user': '',
            'source': source,
            'answers': answer_list,
        }
        if not content_dic['answers']:
            content_dic['status'] = 3
        #_list = [str(id), str(sub_class), json.dumps(content_dic), source, update_time, taskid]
        #fw.write('\x01'.join(_list) + '\n')
        fw.flush()

if __name__ == '__main__':
    filename = sys.argv[1]#'/Users/bjhl/Downloads/360taskid.xls'
    read(filename)
