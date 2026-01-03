import maya.cmds as cmds
#删除未知节点
def delete_unknowNodes(*args):
    ls_unknownNodes = cmds.ls(type='unknown')+cmds.ls(type='unknownDag')+cmds.ls(type='unknownTransfrom')
    print  (u'清理未知节点:'.format(ls_unknownNodes))
    for unknownNode in ls_unknownNodes:
        if cmds.objExists(unknownNode):
            cmds.lockNode(unknownNode,lock=False)
            cmds.delete(unknownNode)
        else:
            print (u'\n\n\n\t你的场景已经清理未知节点')
    return ls_unknownNodes
#删除未知插件
def delete_unknowPlugins(*args):
    plugin_list = cmds.unknownPlugin(q=True,l=True)
    print  (u'清理未知插件:{}'.format(plugin_list))
    if plugin_list:
        for plugin in plugin_list:
            print (plugin)
            try:
                cmds.unknownPlugin(plugin,r=True)
            except:
                pass
    return plugin_list

def cleanFile(*args):  
    unknowNodes=delete_unknowNodes()
    unknowPlugin=delete_unknowPlugins()
    if unknowNodes:
        cmds.confirmDialog( title=u'清理文件', message=u'清理掉{}个未知节点'.format(len(unknowNodes)))
    if unknowPlugin:
        cmds.confirmDialog( title=u'清理文件', message=u'清理掉{}个未知插件'.format(len(unknowPlugin)))
    return unknowPlugin,unknowNodes
cleanFile(0)