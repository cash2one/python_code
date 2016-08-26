#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import six
from six import iteritems
from six import itervalues
import mysql.connector

class BaseDB:

    '''
    BaseDB
    dbcur should be overwirte
    '''
    __tablename__ = None
    placeholder = '%s'

    @staticmethod
    def escape(string):
        return '`%s`' % string

    @property
    def dbcur(self):
        raise NotImplementedError

    def _execute(self, sql_query, values=[]):
        dbcur = self.dbcur
        print dbcur.execute(sql_query, values)
        return dbcur

    def _select(self, tablename=None, what="*", where="", where_values=[], offset=0, limit=None):
        tablename = self.escape(tablename or self.__tablename__)
        if isinstance(what, list) or isinstance(what, tuple) or what is None:
            what = ','.join(self.escape(f) for f in what) if what else '*'

        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where:
            sql_query += " WHERE %s" % where
        if limit:
            sql_query += " LIMIT %d, %d" % (offset, limit)
        #logger.debug("<sql: %s>", sql_query)

        for row in self._execute(sql_query, where_values):
            yield row

    def _select2dic(self, tablename=None, what="*", where="", where_values=[],
                    order=None, offset=0, limit=None):
        tablename = self.escape(tablename or self.__tablename__)
        if isinstance(what, list) or isinstance(what, tuple) or what is None:
            what = ','.join(self.escape(f) for f in what) if what else '*'

        sql_query = "SELECT %s FROM %s" % (what, tablename)
        if where:
            sql_query += " WHERE %s" % where
        if order:
            sql_query += ' ORDER BY %s' % order
        if limit:
            sql_query += " LIMIT %d, %d" % (offset, limit)
        #logger.debug("<sql: %s>", sql_query)

        dbcur = self._execute(sql_query, where_values)
        fields = [f[0] for f in dbcur.description]

        for row in dbcur:
            yield dict(zip(fields, row))

    def _replace(self, tablename=None, **values):
        tablename = self.escape(tablename or self.__tablename__)
        if values:
            _keys = ", ".join(self.escape(k) for k in values)
            _values = ", ".join([self.placeholder, ] * len(values))
            sql_query = "REPLACE INTO %s (%s) VALUES (%s)" % (tablename, _keys, _values)
        else:
            sql_query = "REPLACE INTO %s DEFAULT VALUES" % tablename
        #logger.debug("<sql: %s>", sql_query)

        if values:
            dbcur = self._execute(sql_query, list(itervalues(values)))
        else:
            dbcur = self._execute(sql_query)
        return dbcur.lastrowid

    def _insert(self, tablename=None, **values):
        tablename = self.escape(tablename or self.__tablename__)
        if values:
            _keys = ", ".join((self.escape(k) for k in values))
            _values = ", ".join([self.placeholder, ] * len(values))
            sql_query = "INSERT INTO %s (%s) VALUES (%s)" % (tablename, _keys, _values)
        else:
            sql_query = "INSERT INTO %s DEFAULT VALUES" % tablename
        #logger.debug("<sql: %s>", sql_query)

        if values:
            dbcur = self._execute(sql_query, list(itervalues(values)))
        else:
            dbcur = self._execute(sql_query)
        return dbcur.lastrowid

    def _update(self, tablename=None, where="1=0", where_values=[], **values):
        tablename = self.escape(tablename or self.__tablename__)
        _key_values = ", ".join([
            "%s = %s" % (self.escape(k), self.placeholder) for k in values
        ])
        sql_query = "UPDATE %s SET %s WHERE %s" % (tablename, _key_values, where)
        #print ("<sql: %s>", sql_query)
        dbcur = self._execute(sql_query, list(itervalues(values)) + list(where_values))
        return dbcur.lastrowid
        #return self._execute(sql_query, list(itervalues(values)) + list(where_values))

    def _delete(self, tablename=None, where="1=0", where_values=[]):
        tablename = self.escape(tablename or self.__tablename__)
        sql_query = "DELETE FROM %s" % tablename
        if where:
            sql_query += " WHERE %s" % where
        #logger.debug("<sql: %s>", sql_query)

        return self._execute(sql_query, where_values)


class DB(BaseDB):
    __tablename__ = "primary_school_info"

    def __init__(self):
        config = {'host': '127.0.0.1',  # 默认127.0.0.1
                  'user': 'zhanqun',
                  'password': 'wdlPD40xjO5',
                  'port': 3305,  # 默认即为3306
                  'database': 'zhanqun',
                  'charset': 'utf8' ,
                  'autocommit' : True
                  }

        self.conn = mysql.connector.connect(**config)
        self.database_name = 'zhanqun'

    @property
    def dbcur(self):
        try:
            if self.conn.unread_result:
                self.conn.get_rows()
            return self.conn.cursor()
        except (mysql.connector.OperationalError, mysql.connector.InterfaceError):
            self.conn.ping(reconnect=True)
            self.conn.database = self.database_name
            return self.conn.cursor()



db = DB()

mapper_dict = {'1': '一',
               '0': '零',
               '2': '二',
               '3': '三',
               '4': '四',
               '5': '五',
               '6': '六',
               '7': '七',
               '8': '八',
               '9': '九',
               # '10':'十'
               }


def mapper_fun(val):
    if val.isdigit() and val in mapper_dict:
        return mapper_dict[val]
    return val


import traceback,re

update_db = DB()
from fuzzywuzzy import fuzz

update_where = '`name` = %s' % db.placeholder
name = u'沈阳市东陵区王滨乡中心校后沟分校'
update_dict = {}
update_dict['district'] = u'东陵区1'
print update_db._update(where=update_where, where_values=(name,), **update_dict)
where = '`name` = %s' % db.placeholder
for each in db._select2dic(where=where, what=['name'], where_values=(name,)):
    print each





#print len(_dict)
# for k,v in _dict.items():
#     score_dict = {}
#     score_dict['score'] = v
#     print k,db._update(where=where,where_values=(k,),**score_dict)

# update_db = DB()
# import os
# import os.path
# import json
# from urllib import  quote
# os.chdir('/Users/bjhl1/Downloads/hexing')
# key = list()
# with open('en.txt','r') as f:
#     for line in f:
#         if line :
#             line = line.strip()
#             arr = line.split()
#             for each in arr:
#                 if each not in key:
#                     key.append(each)
#
# print json.dumps(key)

# one = list()
# two = list()
# three = list()
# mapper = dict()
# with open('area.txt','r') as f:
#     for line in f:
#         if line :
#             line = line.strip()
#             arr = line.split()
#             #name = arr[1]
#             level = arr[3]
#             if int(level) == 1:
#                 one.append(arr[1])
#             if int(level) == 2:
#                 two.append(arr[1])
#                 #print arr[6]
#                 mapper[unicode(arr[6],'utf-8')] = arr[1]
#             if int(level) == 3:
#                 three.append(arr[6])
#                 #mapper[arr[6]] = arr[1]



# where = '`school_type`!= "" and `school_type` is not null'
# uniq = list()
# for each in db._select2dic(what=['province','city','district','name'],where=where):
#     province = each.get('province')
#     city = each.get('city')
#     district = each.get('district')
#     name= each.get('name')
#     info = province +  city + district
    # if info not in uniq:
    #     if province and province not in one:
    #             print province,each['name'],'1'
    #     if city  and city not in two:
    #             print city,each['name'],'2'
    #             where = '`name` = %s'%update_db.placeholder
    #             update_db._delete(where=where,where_values=(name,))
    #     if district and district not in three:
    #             print district,each['name'],'3'
    #             # if district in mapper:
    #             #     _dict = {}
    #             #     _dict['city'] = mapper[city]
    #             where = '`name` = %s' % update_db.placeholder
    #             update_db._delete(where=where, where_values=(name,))
    #     uniq.append(info)
    # where = '`name` = %s' % update_db.placeholder
    # _dict = {}
    # _dict['school_type'] = u'公办'
    # update_db._update(where=where, where_values=(name,),**_dict)

# where = "`school_type` != '' and `school_type` is not null"
# id_where = '`name` = %s'%update_db.placeholder
# uniq = list()
# for each in db._select2dic(what=['province','city','district','name','school_type'],where=where) :
#     name = each.get('name')
#     #province = each.get('province','')
#     #city = each.get('city', '')
#     #district = each.get('district') if each.get('district') else ''
#     school_type = each.get('school_type')
#     _dict  = {}
#     if  u'公办' in school_type:
#         _dict['school_type'] = u'公办'
#     elif u'普通' in school_type:
#         _dict['school_type'] = u'普通'
#     elif u'示范' in school_type:
#         _dict['school_type'] = u'示范校'
#     elif u'重点' in school_type:
#         _dict['school_type'] = u'重点'
#     elif u'民办' in school_type:
#         _dict['school_type'] = u'民办'
#     else:
#         _dict['school_type'] = u'公办'
#     print name
#     update_db._update(where=id_where,where_values=(name,),**_dict)
#
#
# print json.dumps(uniq)
    # if info not in uniq:
    #     if province and province not in one:
    #                 print province,each['name']
    #     if city  and city not in two:
    #                 print city,each['name']
    #     if district and district not in three:
    #                 print district,each['name']
    #     uniq.append(info)





