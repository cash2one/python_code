#-*- coding: UTF-8 -*-
#执行系统命令行命令,即终端命令
import subprocess
subprocess.call(["ls", "-l"])
subprocess.call("ls")
subprocess.check_call('ls -l',shell = True)
subprocess.check_call('cat test.txt',shell = True)