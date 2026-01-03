# coding:utf-8
import maya.mel as mel
import maya.cmds as cmds
import sys,os,re
import maya.api.OpenMaya as om
import traceback
# sys.path.insert(0,r"D:\Temp\python27")

os.environ['QT_API'] = 'PySide2'

if r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp" in sys.path:
    sys.path.remove(r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp")
import maya.cmds as cmds
cmds.dirmap(en=1)
cmds.dirmap(m=(r'H:\\', r'G:\\'))
sys.path.append(os.getenv('LugwitLibDir'))
import Lugwit_Module as LM
if r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp" in sys.path:
    sys.path.remove(r"D:\TD_Depot\Software\Lugwit_syncPlug\lugwit_insapp\trayapp")
from datetime import datetime

# 获取当前时间
now = datetime.now()

# 格式化为日期字符串（示例：2024-03-15）
formatted_date = now.strftime("%Y-%m-%d")  
print(formatted_date)

# if not os.path.exists(LM.MayaPlugLogDir):
#     os.makedirs(LM.MayaPlugLogDir)
# logFile=u"{}/Maya_{}.log".format(LM.MayaPlugLogDir,formatted_date)
# maya_logger = logging.getLogger("MayaTools")
# maya_logger.setLevel(logging.DEBUG)

# for handler in maya_logger.handlers[:]:  # 遍历副本而不是原列表
#     if isinstance(handler, logging.FileHandler):
#         maya_logger.removeHandler(handler)
#         handler.close()  # 记得关闭handler释放资源
        
        
# file_handler = RotatingFileHandler(logFile, maxBytes=1*1024*1024, backupCount=3)
# file_handler.setFormatter(logging.Formatter('%(message)s'))
# file_handler.setLevel(logging.DEBUG)
# maya_logger.addHandler(file_handler)

from imp import reload
def initializePlugin(*args):
    from maya import mel
    if not mel.eval('$gMainWindow=$gMainWindow'):
        return
    if 'LugwitMayaPlugStart' in sys.modules:
        del sys.modules["LugwitMayaPlugStart"]
    try:
        import LugwitMayaPlugStart
        print("ins_start")
        LugwitMayaPlugStart.install()
        print("ins_finish")
    except :
        traceback.print_exc()
        print("ins_error")


def uninitializePlugin(*args):
    try:
        reload (LugwitMayaPlugStart)
    except:
        import LugwitMayaPlugStart
    LugwitMayaPlugStart.uninstall()

'''
这个文件夹只有一个python文件,否则在插件目录会有两个python文件
'''
