#!coding: utf-8
import json,time
with open('/Users/bjhl/Documents/genshuixue/es/demo.log', 'a') as f:
    for i in range(2000, 3000):
        _dict = {}
        _dict = {'k1': str(i),'k2':str(i+1)}
        f.write(json.dumps(_dict)+'\n')
        f.flush()
        time.sleep(0.1)
