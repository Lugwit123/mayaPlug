# -*- coding: utf8
import os,sys, traceback
LugwitToolDir=os.environ.get('LugwitToolDir')
sys.path.append(LugwitToolDir+'/Lib')
import Lugwit_Module as LM
from Lugwit_Module.l_src.l_parse_args import parse_args
print("morenbianma:", sys.getdefaultencoding())
print("biaozuinshuchubianma :", sys.stdout.encoding)
try:
    import maya.standalone
    maya.standalone.initialize(name='python')
    reload(sys)
    #sys.setdefaultencoding('gbk')
    import codecs
    sys.stdout = codecs.getwriter('gbk')(sys.stdout)
    LM.lprint (u'你正在后台调用代码')
    os.environ['houtai']='1'
except Exception as e:
    LM.lprint (u'导入maya.standalone失败,原因是{},你正在前台调用代码'.format(e))
    os.environ['houtai']='0'
print("morenbianma:", sys.getdefaultencoding())
print("biaozuinshuchubianma :", sys.stdout.encoding)


import exFbx
import mat
export_mat_json = mat.export_mat_json
export_mat_json = mat.export_mat_json
exAniClip_Simple=exFbx.exAniClip_Simple
exmatJsonAndSgNode = mat.exmatJsonAndSgNode
exAbc_Batch=exFbx.exAbc_Batch
exFBX=exFbx.exFBX
exTpose=exFbx.exTpose


    

def your_function(**kwargs):
    args = ['--name John', '--age 25', '--message Hello World', '--occupation Engineer']
    result = parse_args(args)
    print(result)

if __name__ == '__main__':
    try:
        exec_func = sys.argv[1]
        parsed_args = parse_args(sys.argv[2:])
        print(u"解析后的参数字典:", parsed_args)
        eval(exec_func + '(**parsed_args)')
    except Exception as e:
        print(traceback.format_exc())
