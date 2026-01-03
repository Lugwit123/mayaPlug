# coding:utf-8
st=0
import os,re,sys
LugwitPath = os.path.dirname(__file__)
LugwitPath = LugwitPath.replace('\\', '/')
LugwitPath = re.search('.+/Lugwit_plug', LugwitPath).group(0)
sys.path.append(LugwitPath+r'\mayaPlug\l_scripts\GloablVariable')

'''
#添加模块所在路径
import os,re,sys,time,sys,os
fileDir = os.path.dirname(__file__)
sys.path.insert(0,fileDir)



'''