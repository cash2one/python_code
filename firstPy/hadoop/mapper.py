#!/usr/bin/env python
#!coding: utf-8

import os,sys
import json
import re
import time,traceback
reload(sys)
sys.setdefaultencoding("utf-8")

class StrategyMR():
    def __init__(self):
        self.record = {}

    def threadInit(self):
        self.record = {}

    def threadDestroy(self):
        pass
    
    def set(self, key, value):
        self.record[key] = value

    def get(self, key):
        if self.record.has_key(key):
            return self.record[key]
        else:
            return None

    def run(self, s):
        for line in sys.stdin:
            try:
                line = line.strip()
                self.threadInit()
                res = self.parseLine(line)
                if res == -1:
                    continue
                flag = s.process()
                if flag == 1:
                    key = self.record['key']
                    value = self.record['value']
                    print '%s\t%s' %(key, value)
                self.threadDestroy()
            except:
                traceback.print_exc(sys.stdout)


    def parseLine(self, line):
        line = line.strip()
        f = line.split('')
        if len(f) != 6:
            return -1
        try:
            id = f[0]
            cls = f[1]
            content = json.loads(f[2])
            source = f[3]
            update_time = f[4]
            taskid = f[5]
            self.record['id'] = id
            self.record['class'] = cls
            self.record['content'] = content
            self.record['source'] = source
            self.record['update_time'] = update_time
            self.record['taskid'] = taskid
            self.record['key'] = taskid
            self.record['value'] = line
        except:
            traceback.print_exc(sys.stdout)
            return -1
        return 1
    
    def writeBck(self):
        try:
         #   ISOTIMEFORMAT='%Y-%m-%d %X'
         #   update_time = time.strftime( ISOTIMEFORMAT, time.localtime() )
         #   self.record['update_time'] = update_time
            id = self.record['id']
            cls = self.record['class']
            content = self.record['content']
            source = self.record['source']
            update_time = self.record['update_time']
            taskid = self.record['taskid']
            print '%s%s%s%s%s%s' %(id, cls, json.dumps(content), source, update_time, taskid)
            return 1
        except:
            traceback.print_exc(sys.stdout)
            return -1


class MergeStrategy(StrategyMR):
    def process(self):
        key = self.get('id')
        self.set('key', key)
#        self.set('value', 1)
        return 1
        

if __name__=='__main__':
    s = MergeStrategy()
    s.run(s)
