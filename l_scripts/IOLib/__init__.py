# coding:utf-8
#添加模块所在路径
import os,re,sys
fileDir = os.path.dirname(__file__)
sys.path.insert(0,fileDir)

# 注释掉,不然
# from exFbx import *
from mat import *
print("import iolib-----------------------------------")
from . import call_batch_ex_abc
