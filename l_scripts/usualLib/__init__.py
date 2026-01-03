# coding:utf-8
from __future__ import absolute_import
import sys,os
sys.path.append(os.path.dirname(__file__))

print (u'添加路径{}'.format(os.path.dirname(__file__)))
print (u'usual')
from .usual import *
print (u'usual')
from .cleanRef import *

from . import replaceHigModel
