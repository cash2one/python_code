#coding=utf-8
from __future__ import unicode_literals, division, absolute_import
import sys,json,oss2,urllib2
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import six
from six import iteritems
from six import itervalues
import mysql.connector
import os
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
        dbcur.execute(sql_query, values)
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
import urllib
update_db = DB()
from fuzzywuzzy import fuzz
import socket
socket.setdefaulttimeout(300)
update_where = '`name` = %s and display_image like "%%default%%"' % db.placeholder
count = 0
for each in open('/Users/bjhl/Documents/xiaoxue_img_add'):

    try:
        #print  each['name']
        each = each.strip().split('$$$$$')[1]
        each = json.loads(each.replace('\\\\','\\'))
        name = each['school_name']
        display_image = each['logo'][0]
        update_dict = {}
        update_dict['display_image'] = display_image
        update_db._update(where=update_where, where_values=(name,), **update_dict)
        #print flag
        #if flag !=0:
        count += 1
        request = urllib2.Request(display_image)
        request.add_header('User-Agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
        response = urllib2.urlopen(request)
        resp = response.read()
        print name, display_image
        filename = '/Users/bjhl/Documents/imgs_add/' + name + '.jpg'
        with open(filename,'wb') as f:
            f.write(resp)
            f.flush()

    except:
        traceback.print_exc()
        continue
print count




