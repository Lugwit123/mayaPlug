# coding:utf-8
import maya.cmds as cmds
def get_selected_group_name():
    selected_objects = cmds.ls(selection=True, type='transform')  # 获取当前选中的transform类型物体列表

    if selected_objects:
        return selected_objects[0]  # 返回第一个选中的物体名称，即选中的组的名称

    # 如果没有选中物体，返回空字符串或者其他适当的信息
    return ''

# 示例用法：
selected_object = get_selected_group_name()

def export_selected_group_to_abc():
    startframe = cmds.playbackOptions(q=True, min=True)
    endframe = cmds.playbackOptions(q=True, max=True)

    file_path = cmds.file(q=True, sceneName=True)
    path_parts = file_path.split('/')
    directory_path = '/'.join(path_parts[:-1])
    print (directory_path)
    abcName = directory_path+"/"+selected_object+".abc"

    # 选择要导出的物体
    #selected_object = "pCone1"

    # 构建导出命令
    command = "-frameRange {} {} -stripNamespaces -uvWrite -writeFaceSets "
    command += "-worldSpace -writeUVSets -dataFormat ogawa -root |{} -file \"{}\""

    command = command.format(startframe, endframe, selected_object, abcName)


    cmds.AbcExport(j=command)

