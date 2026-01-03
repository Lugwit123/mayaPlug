# coding:utf-8
import json
import os
import re
from Lugwit_Module import *
import codecs,inspect
__file__=inspect.getfile(inspect.currentframe())


try:
    import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm
except:
    pass

data = []


def get_document(group):
    return dict(
        name=group.name().split("|")[-1].split(":")[-1],
        label=u"",
        children=[get_document(child) for child in group.getChildren(type="transform")]
    )


def get_data_by_scene():
    #pm.select(all=1)
    return [get_document(group) for group in pm.ls(type="transform")]


def save_hierarchy(hierarchy):
    path = os.path.abspath(__file__+"/../hierarchy.json")
    with open(path, "w") as write:
        write.write(json.dumps(hierarchy, indent=2))


def load_hierarchy(file_path):
    # template_dir = os.path.abspath(__file__+"/../template")
    # file_list = os.listdir(template_dir)
    # file_list.sort()
    # first_file_path = os.path.join(template_dir,file_list[0])
    # path = os.path.abspath(__file__+"/../hierarchy.json")
    with codecs.open(file_path, "r",encoding='utf8') as read:
        return json.loads(read.read())


def get_group(name):
    if pm.objExists(name):
        return pm.PyNode(name)
    else:
        fields = name.split("|")
        parent = "|".join(fields[:-1])
        if parent:
            parent = get_group(parent)
            return pm.group(n=fields[-1], p=parent, em=1)
        else:
            return pm.group(n=fields[-1], em=1)

def createGroup(groupAbsName):
    parent=''
    for x in groupAbsName.split('|'):
        if x:
            if not cmds.objExists(parent+'|'+x):
                cmds.createNode('transform',n=x,p=parent)
        parent=parent+'|'+x
        parent=parent[:]


def move_polygons(polygons, name):
    old_polygons = []
    if pm.objExists(name):
        group = pm.PyNode(name)
        if group.getChildren(type="mesh"):
            old_polygons.append(group)
        old_polygons += [polygon for polygon in group.getChildren(type="transform") if polygon.getChildren(type="mesh")]
        polygons = old_polygons + [polygon for polygon in polygons if polygon not in old_polygons]
    #if len(polygons) > 1:
    for polygon in polygons:
        if polygon.getParent():
            polygon.setParent(w=1)
    
    
    print (name)
    isGroup=re.search('_Grp',name.split("|")[-1],flags=re.I)
    if isGroup:
        group = get_group(name)
        polygon_name = name.split("|")[-1] + "{i:0>%i}" % len(str(len(polygons)))
        polygon_name=re.sub('_Grp.*_*','',polygon_name,flags=re.I)
    else:
        polygon_name=name.split("|")[-1]
        group = "|".join(name.split("|")[:-1])
        print (group,group)
        if not cmds.objExists(group):
            createGroup(group)

    
    #lprint (u'模型{}放入组{}'.format(polygon_name,group))
        
    for i, polygon in enumerate(polygons):
        if polygon.getParent() != group:
            polygon.setParent(group)
        if isGroup:
            polygon.rename(polygon_name+'_'+str(i).zfill(3))
            polygon.getShape().rename(polygon_name+'_'+str(i).zfill(3) + "Shape")
        else: # 如果是多边形
            if cmds.objExists(name) or len(polygons)>1:
                polygon_name_addSuffix=polygon_name +'_'+str(i).zfill(3)
            else:
                polygon_name_addSuffix=polygon_name
            polygon.rename(polygon_name_addSuffix)
            polygon.getShape().rename(polygon_name_addSuffix + "Shape")
            lprint (polygon_name_addSuffix)
    # elif len(polygons) == 1:
    #     polygon=polygon[0]
    #     parent_name = name[:-len(name.split("|")[-1]) - 1]
    #     parent = get_group(parent_name)
    #     lprint (parent_name,parent,name)
    #     if pm.objExists(name):
    #         pm.parent(name, w=1)
    #     if polygons[0].getParent() != parent:
    #         polygons[0].setParent(parent)
    #     newName = name + '000'
    #     newName=re.sub('_Grp.*_*','',newName,flags=re.I)
    #     polygons[0].rename(newName)
        
        
        # parent_name = name[:-len(name.split("|")[-1]) - 1]
        # arent = get_group(parent_name)
        # polygon_name=re.sub('_Grp.*_*','',parent_name,flags=re.I)
        # if pm.objExists(name):
        #     pm.parent(name, w=1)
        # if polygons[0].getParent() != polygon_name:
        #     polygons[0].setParent(parent)
        # polygons[0].rename(name.split("|")[-1])


def move_text(text, name):
    polygons = [polygon for polygon in pm.ls(re.split("\n", text), type="transform") if
                polygon.getChildren(type="mesh")]
    move_polygons(polygons, name)


def move_selected(name):
    polygons = [polygon for polygon in pm.selected(type="transform") if
                polygon.getChildren(type="mesh")]
    move_polygons(polygons, name)
    
def add_suffix(inputStr='eyeBall_mesh_R_dow_LOW_grp', suffix='L',ignoreExitZiDuan=False):
    '''
    实现思路:首先查看后缀名中是否以sim|mesh,如果没得,suffix为sim|mesh的话直接添加在最前面,
    如果没得,则查看后缀名中是否以L|R,如果没得,suffix为L|R的话直接添加在最前面,一次类推
    '''
    inputStrUseToFindBaseName=inputStr.replace('_',' ')
    key_word_list=[('sim', 'mesh'), (r'\bL\b', r'\bR\b'), (r'top', r'dow'), ('HIGH', 'LOW'), ('Group', 'grp')]
    suffix_convert=suffix
    if suffix_convert=='L':
        suffix_convert='L[^OW]'
        
    # 获取基本名称:
    objBaseName=inputStrUseToFindBaseName
    for  key_words in key_word_list:
        lprint (objBaseName)
        #key_words=['_'+x for x in key_words]
        objBaseName=re.sub('|'.join(key_words),'',objBaseName,flags=re.I)
        lprint ('|'.join(key_words),'',objBaseName)
    objBaseName=objBaseName.replace(' ','_')
    lprint (objBaseName)
    objBaseName= re.sub('_+','_',objBaseName)
    objBaseName= re.sub('_+$','',objBaseName)
    lprint (u'从输入名称{}搜索基本名称的正则表达式是:{},结果为{}'.format(inputStr,'|'.join(key_words),objBaseName)) 

    # 获取后缀名
    objSuffix=re.sub(objBaseName,'',inputStr)
    objSuffix= re.sub('^_+','',objSuffix)
    lprint (u'物体的后缀名是:{}'.format(objSuffix))
    
    # 接下来从第一个字符串开始排查
    ResultName=objSuffix.replace('_',' ')
    indKeyWordInObjSuffixList=[]
    for key_word_index,key_words in enumerate(key_word_list):
        objSuffix=objSuffix.replace('_',' ')
        findKeyWordInsuffix=re.search('{}|{}'.format(*key_words),suffix,flags=re.I)
        findKeyWordInObjSuffix=re.search('{}|{}'.format(*key_words),objSuffix,flags=re.I)
        if findKeyWordInObjSuffix:
            indKeyWordInObjSuffixList.append(findKeyWordInObjSuffix.group())
        print ('>>>>>>>')   
        lprint (u'使用表达式{}在{}中re.search,结果为{}'.format('{}|{}'.format(*key_words),suffix,findKeyWordInsuffix))
        lprint (u'使用表达式{}在{}中re.search,结果为{}'.format('{}|{}'.format(*key_words),objSuffix,findKeyWordInObjSuffix))
        print ('<<<<<\n',ignoreExitZiDuan)  
        if findKeyWordInsuffix :
            if not findKeyWordInObjSuffix:
                if indKeyWordInObjSuffixList:
                    lprint (r'\b'+indKeyWordInObjSuffixList[-1]+r'\b')
                    lprint (suffix,ResultName)
                    ResultName=re.sub(r'\b'+indKeyWordInObjSuffixList[-1]+r'\b',indKeyWordInObjSuffixList[-1]+' '+suffix+' ',ResultName,flags=re.I)
                else:
                    ResultName=' '.join([suffix,objSuffix])
                ResultName=re.sub(' +','_',ResultName)
                ResultName=re.sub('_+','_',ResultName)
                ResultName=re.sub('_+$','',ResultName)
                lprint (objBaseName+'_'+ResultName,)
                return objBaseName+'_'+ResultName
            if findKeyWordInObjSuffix and not ignoreExitZiDuan:
                findKeyWordInObjSuffix=findKeyWordInObjSuffix.group()
                ResultName=re.sub(r'\b'+findKeyWordInObjSuffix+r'\b',suffix+'_',objSuffix,flags=re.I)
                ResultName=re.sub(' +','_',ResultName)
                ResultName=re.sub('_+','_',ResultName)
                ResultName=re.sub('_+$','',ResultName)
                lprint (objBaseName+'_'+ResultName,)
                return objBaseName+'_'+ResultName

if __name__=='__main__':
    add_suffix(suffix='L')
