# coding:utf-8
print(('run module{}'.format(__file__)))
import sys,os
#添加模块所在路径
import os,re,sys
fileDir = os.path.dirname(__file__)
sys.path.insert(0,fileDir)

import ExPhiz
import MatchJoint
import usualRig
import DP
import autoBs


