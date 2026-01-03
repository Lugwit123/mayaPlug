import maya.cmds as cmds
def ex_xgmSplineDescription(GroupToEx=[],exPath='D:/aa.abc',sf=101,ef=110):
    if not GroupToEx:
        GroupToEx=cmds.ls(type='xgmSplineDescription')
    j = '-frameRange {} {} -step 1 -df "ogawa" -wfw -file "{}"'.format(sf, ef, exPath.replace('\\','/'))
    for ele in GroupToEx:
        print (ele)
        j='-obj {} {} '.format(ele,j)
    print j
    cmds.xgmSplineCache(ex=1, j=j)
        
if __name__ == '__main__':
    import sys
    sys.path.insert(0,r'D:\plug_in\Lugwit_plug\mayaPlug\l_scripts\IOLib\test.py')
    import test;reload(test)
    test.ex_xgmSplineDescription()
