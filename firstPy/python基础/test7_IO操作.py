#-*- coding: UTF-8 -*-
#print raw_input("请输入:")
#input([prompt]) 函数和 raw_input([prompt]) 函数基本类似，但是 input 可以接收一个Python表达式作为输入，并将运算结果返回。
#print input("请输入")
import os
rootdir = '/usr/local/'
for parent, dirnames,  filenames in os.walk(rootdir):
    for dirname in dirnames:
        print dirname
        # for s_parent, s_dirnames, s_filenames in os.walk(rootdir +dirname+'/'):
        #     for filename in s_filenames:
        #         # print filename

# print fo.name
# print fo.closed
# print fo.mode
# print fo.softspace
# print "当前文件位置:",fo.tell()
#读写不能放一起
#fo.write("www.bjhl.com")
# try:
#     #print fo.read(5)
#     print fo.readline()
#     #换行符都读取出来了
#     #s = fo.readlines()
# except IOError:
#     print "Error: 没有找到文件或读取文件失败"
    # else:
    #     print "内容读取成功"
# print s
# print s[0]
# print "当前文件位置:",fo.tell()
# fo.seek(0)
# print "当前文件位置:",fo.tell()
# fo.close()
#
# import os
# #os.rename("test.txt","test_改名.txt")
# # os.rename("test_改名.txt","test.txt")
# print os.getcwd()

