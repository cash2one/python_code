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

def process_time(date):
    if u'今天' in date or u'小时' in date or u'分钟' in date:
        return '2016-06-27'
    if u'昨天' in date:
        return '2016-06-26'
    return date.replace('.', '-')

category_id_dic = {
u'中国古代史': ['266','302','306'],
u'教师交流': ['-1',],
u'高考地理': ['342',],
u'高中学习讲义': ['266','1245'],
u'大学英语': ['387',],
u'高考': ['342',],
u'初中语文': ['161','167'],
u'高考指南卡': ['342',],
u'师生关系': ['-1',],
u'初中历史': ['161',],
u'大学政治': ['387','410','418'],
u'高考数学': ['342','343','344'],
u'世界近现代史': ['266','302','306'],
u'问吧频道': ['0',],
u'初中物理': ['161',],
u'政治生活': ['-1',],
u'高考物理': ['342','353','354'],
u'高二生物': ['342','359','360'],
u'高校咨询': ['-3',],
u'同学关系': ['0',],
u'必修课程': ['266','267',],
u'青春叛逆': ['897','1196','1199'],
u'高考政治': ['342',],
u'自主招生': ['342',],
u'高考题库系列': ['342',],
u'阅读理解': ['266','272'],
u'区域地理': ['324','349','350'],
u'选修课程': ['266','267'],
u'师范国防': ['342',],
u'其他分类': ['-3',],
u'电脑常识': ['573',],
u'有机物': ['266','297'],
u'高一生物': ['266','307'],
u'初中英语': ['161','172'],
u'初中生物': ['161','212'],
u'电磁学': ['266','292'],
u'高招政策': ['342',],
u'元素化合物': ['266','297'],
u'高考化学': ['342','355','356'],
u'初中政治': ['161','212'],
u'艺体高考': ['342',],
u'心理调节': ['897','1196','1199'],
u'考试答案交流区': ['266','1245'],
u'基础知识': ['-1',],
u'初中数学': ['161','162'],
u'哲学生活': ['0',],
u'高考复习讲义': ['342',],
u'奥数竞赛': ['-1',],
u'写作指引': ['-1',],
u'初中地理': ['161','212'],
u'高考英语': ['342',],
u'试题调研系列': ['266','1245'],
u'家长咨询': ['-1',],
u'经济生活': ['-3',],
u'化学实验': ['266','297'],
u'基本概念、规律': ['266','297'],
u'人文地理': ['324','349','350'],
u'专题调研系列': ['266','1245'],
u'高考语文': ['342',],
u'海外留学': ['783',],
u'大学数学': ['387','410','414'],
u'书面表达': ['-1',],
u'高考冲刺讲义': ['342',],
u'热光原': ['266','292'],
u'中国近现代史': ['266','302','306'],
u'高三生物': ['266','307'],
u'自然地理': ['324','349','350'],
u'疯狂阅读系列': ['266','1245'],
u'校园早恋': ['0',],
u'高中力学': ['266','292'],
u'广西公务员':['817',],
u'江西公务员':['817',],
u'河北公务员':['817',],
u'宁夏公务员':['817',],
u'重庆公务员':['817',],
u'河南公务员':['817',],
u'辽宁公务员':['817',],
u'浙江公务员':['817',],
u'甘肃公务员':['817',],
u'四川公务员':['817',],
u'山西公务员':['817',],
u'青海公务员':['817',],
u'广东公务员':['817',],
u'山东公务员':['817',],
u'新疆公务员':['817',],
u'云南公务员':['817',],
}
del_res = [
    u'资源平台',
    u'网络课堂',
    u'虚拟货币咨询',
    u'高考指南卡',
]
def read(data):
    dic = defaultdict(int)
    sub_class = 34
    fw = open('%s.res'%(data.split('/')[-1]), 'w')
    for line in open(data):
        try:
            (taskid, result) = line.strip().split('$$$$$')
            data = json.loads(result.replace('\\\\','\\'))
            title = data.get('title', '')
            if not title:
                continue
            #type = data.get('type', '')
            category = data.get('category_id', '')
            if category in del_res:
                continue
            update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            source = data['source']
            category_id_list = category_id_dic.get(category, ['0', ])
            data['category_id'] = category_id_list
            id = get_id(taskid)
            _list = [str(id), str(sub_class), json.dumps(data), source, update_time, taskid]
            fw.write('\x01'.join(_list) + '\n')
            fw.flush()
        except:
            print taskid

def sta(data):
    dic = defaultdict(int)
    sub_class = 34
    #fw = open('%s.res'%(data.split('/')[-1]), 'w')
    dic = defaultdict(int)
    for line in open(data):
        try:
            (taskid, result) = line.strip().split('$$$$$')
            data = json.loads(result.replace('\\\\','\\'))
            #print data
            title = data.get('title', '')
            if not title:
                continue
            #type = data.get('category_id', '')
            category = data.get('category_id', '')
            if category in del_res:
                continue
            dic[category] += 1
            '''
            update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            source = data['source']
            category_id_list = category_id_dic.get(type, ['0', ])
            data['category_id'] = category_id_list
            id = get_id(taskid)
            _list = [str(id), str(sub_class), json.dumps(data), source, update_time, taskid]
            fw.write('\x01'.join(_list) + '\n')
            fw.flush()
            '''
        except:
            print taskid
    for k, v in dic.iteritems():
        print 'u\''+k+'\':[\'\',],'
        #print k, v

if __name__ == '__main__':
    filename = sys.argv[1]
    read(filename)
    #sta(filename)
