# coding:utf-8
from ast import excepthandler
import sys,os
sys.path.append(os.path.dirname(__file__))
print (u'添加路径{}'.format(os.path.dirname(__file__)))

try:
    import textureManager
except:
    pass


import SetColorSpace

import mapSizeSwitch