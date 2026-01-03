# -*- coding:utf-8 -*-
import maya.cmds as cm
import time
import maya.mel as mel

version = 'v1.2'

def set_the_most_useful_uvset(mesh):
    #把用得最多的uvset设置为当前uvset
    uv_set_list = cm.getAttr('%s.uvSet'%mesh,mi = True)
    uv_set_attr_list = []
    for i in range(len(uv_set_list)):
        if cm.polyEvaluate(mesh,uva = True,
        uvs = cm.getAttr('%s.uvSet[%d].uvSetName'%(mesh,uv_set_list[i]))) != 0:
            uv_set_attr_list.append(uv_set_list[i])
    use_count_dict = dict()
    for i in range(len(uv_set_attr_list)):
        use_count_dict.setdefault(len(cm.uvLink(q = True,
        uvSet = '%s.uvSet[%d].uvSetName'%(mesh,uv_set_attr_list[i]))),[]).append(uv_set_attr_list[i])
    most_use_index = use_count_dict[max(use_count_dict.keys())][0]
    cm.polyUVSet(mesh,uvs = cm.getAttr('%s.uvSet[%d].uvSetName'%(mesh,most_use_index)),cuv = True)

def clean_uv_set(mesh):
    u"""
        保留使用最多的uvset，命名为map1，删除其余uvset。
    """
    #如果有重名uvset，就把第二个uvset开始的uvset改名字
    all_uv_set_list = cm.polyUVSet(mesh,auv = True,q = True)
    if len(all_uv_set_list) <= 1:
        if len(all_uv_set_list) == 1 and all_uv_set_list[0] != 'map1':
            cm.polyUVSet(mesh,rename = True,uvSet = all_uv_set_list[0],newUVSet = 'map1')
        return
    uv_set_attr_list = cm.getAttr('%s.uvSet'%mesh,mi = True)
    if len(uv_set_attr_list) == len(all_uv_set_list) and \
    len(all_uv_set_list) != len(set(all_uv_set_list)):
        for i in range(1,len(uv_set_attr_list)):
            cm.setAttr('%s.uvSet[%d].uvSetName'%(mesh,uv_set_attr_list[i]),
                'delete_map%d%d'%(int(time.time()),uv_set_attr_list[i]),type = 'string')
    #把用得最多的uvset设置为当前uvset
    set_the_most_useful_uvset(mesh)
    #如果当前uvset不是第一个，就把当前uvset拷贝至第一个
    all_uv_set_list = cm.polyUVSet(mesh,auv = True,q = True)
    current_uv_set_list = cm.polyUVSet(mesh,cuv = True,q = True)
    if current_uv_set_list[0] != all_uv_set_list[0]:
        cm.polyCopyUV( mesh, uvi=current_uv_set_list[0], uvs=all_uv_set_list[0] )
    #把除第一个外的uvset删除
    for i in range(len(all_uv_set_list) -1,0,-1):
        try:
            cm.polyUVSet(mesh,d = True,uvs = all_uv_set_list[i])
        except:
            print(u'%s 的 uvset无法删除： %s'%(mesh,all_uv_set_list[i]))
    #把默认的uvset名字改好
    if all_uv_set_list[0] != 'map1':
        cm.polyUVSet(mesh,rename = True,uvSet = all_uv_set_list[0],newUVSet = 'map1')

def clean_uv_set_from_all_mesh(history = 1):
    u"""
        清理所有模型的uvset
    """        
    mesh_set = {cm.listRelatives(mesh,p = True,pa = True)[0] for mesh in cm.ls(type = 'mesh')}
    if not len(mesh_set):
        mel.eval(u"print(\"执行完毕！\");")
        return
    if history == 1:
        cm.delete(list(mesh_set),ch = True)
    else:
        cm.select(list(mesh_set),r = True)
        mel.eval('''doBakeNonDefHistory( 1, {"prePost" });''')
    mesh_list = cm.ls(type = 'mesh')
    for mesh in mesh_list:
        clean_uv_set(mesh)
    mel.eval(u"print(\"执行完毕！\");")


radioCollection1 = ''
def clean(*argvs):
    selected = cm.radioCollection(radioCollection1,q = True,sl = True)
    selected_label = cm.radioButton(selected,q = True,l = True)
    if selected_label == u'删除历史':
        clean_uv_set_from_all_mesh(history = 1)
    else:
        clean_uv_set_from_all_mesh(history = 2)


def show_uv_clean_window():
    winName = 'uvCleanWin'
    if cm.window(winName,exists = True):
        cm.deleteUI(winName)
    cm.window(winName,title = u'UVSet清理 %s'%version)
    cm.window(winName,e = True,w = 260,h = 100)
    cm.columnLayout(adj = True)
    cm.text(l = u'保留使用最多的uvset，\n命名为map1，\n删除其余uvset。',
        h = 50,font = 'plainLabelFont')
    collection1 = cm.radioCollection()
    global radioCollection1
    radioCollection1 = collection1
    rb1 = cm.radioButton( label=u'删除历史' )
    rb2 = cm.radioButton( label=u'删除非变形历史(较慢)' )
    # cm.setParent( '..' )
    cm.radioCollection( collection1, edit=True, select=rb1 )
    cm.button(l = u'执行',h = 30,c = clean)
    cm.showWindow(winName)

    
if __name__ == '__main__':
    show_uv_clean_window()