#ecoding:utf-8
import sys
import MySQLdb
import json
import traceback
reload(sys)
sys.setdefaultencoding("utf-8")

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

        return self._execute(sql_query, list(itervalues(values)) + list(where_values))

    def _delete(self, tablename=None, where="1=0", where_values=[]):
        tablename = self.escape(tablename or self.__tablename__)
        sql_query = "DELETE FROM %s" % tablename
        if where:
            sql_query += " WHERE %s" % where
        #logger.debug("<sql: %s>", sql_query)

        return self._execute(sql_query, where_values)


class DB(BaseDB):
    __tablename__ = "shici"

    def __init__(self):
        config = {'host': '172.21.139.2',  # 默认127.0.0.1
                  'user': 'atlas_rw',
                  'password': 'atlas_rw',
                  'port': 1234,  # 默认即为3306
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

#conn = MySQLdb.connect(host="127.0.0.1",user="atlas_rw",passwd="atlas_rw",db="zhanqun", charset="utf8", port = 1234)

def process():
    #cursor = conn.cursor()
    for line in open(u'/Users/bjhl/Documents/诗词/shici2_liuxue86_full'):
        _dict = json.loads(line.replace('\\\\','\\'))
        url= _dict['url']
        name= _dict['name']
        type= _dict['type']
        tags= _dict['tags']
        author= _dict['author']
        author_url = _dict['author_url']
        dynasty= _dict['dynasty']
        content= _dict['content']
        translation_note= _dict['translation_note']
        parse_appreciation= _dict['parse_appreciation']
        art_appreciation= _dict['art_appreciation']
        _dict.pop('author_url')
        print url
        try:
            # sql = """
            #     select id from shiren where url='%s'""" % (author_url)
            # cursor.execute(sql)
            # for id in cursor.fetchall():
            #     print id
            where = '`url`=%s' % db.placeholder
            where_values = (author_url,)
            what = ['id']
            for each in db._select2dic(tablename='shiren',what=what,where=where,where_values=where_values):
                _dict['author_id'] = each['id']
                #print each['id']
        except:
            traceback.print_exc()
        try:
            # sql = """
            #     insert into  shici (url, name, type, tags, author,author_id, dynasty, content, translation_note, parse_appreciation, art_appreciation)
            #      values (%s,%s, %s, %s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)
            # """ % (url, name, type, tags, author,author_id, dynasty, content, translation_note, parse_appreciation, art_appreciation)
            db._insert(**_dict)
            #cursor.execute(sql)
            #conn.commit()
        except:
            traceback.print_exc()
if __name__ == '__main__':
    process()