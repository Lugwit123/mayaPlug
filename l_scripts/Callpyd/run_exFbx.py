# -*- coding: utf8


from __future__ import print_function
from __future__ import unicode_literals

import os,sys,json,codecs

sys.path.insert(0,os.environ['LugwitToolDir']+'/Lib')

from Lugwit_Module import *

import sys,os

try:
    import maya.standalone
    maya.standalone.initialize(name='python')
    reload(sys)
    sys.setdefaultencoding('gbk')
    lprint (u'你正在后台调用代码')
    # print (u'你正在后台调用代码')
    os.environ['houtai']='1'
except Exception as e:
    lprint (u'导入maya.standalone失败,原因是{},你正在前台调用代码'.format(e))
    os.environ['houtai']='0'


exFbx_pyFile=Lugwit_mayaPluginPath+r'\l_scripts\IOLib\exFbx.py'
exFbx_pyFileDir=os.path.dirname(exFbx_pyFile)
moduleNameExt=os.path.basename(exFbx_pyFile)
moduleNameExt=moduleNameExt.split('.')[0]
sys.path.append(exFbx_pyFileDir)
lprint (exFbx_pyFileDir)

from Lugwit_Module.l_src.l_parse_args import parse_args

from exFbx import *

print ("__name__ == '__main__'",__name__ == '__main__')



if __name__ == '__main__':
    try:
        exec_func = sys.argv[1]
        
        parsed_args = parse_args(sys.argv[2:])
        print(u"解析后的参数字典:{}".format(parsed_args))
        eval(exec_func + '(**parsed_args)')
    except Exception as e:
        print("错误:", e)
