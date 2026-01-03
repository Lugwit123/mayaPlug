# -*- coding: utf8
import maya.cmds as cmds
print("import ======================================================")
def  main(*args):
    #cmds.scriptEditorInfo(clearHistory=True)
    from IOLib.BatchExAbc import load_ui
    print(u"加载abc33333333333")
    reload(load_ui)
    load_ui.showWin()