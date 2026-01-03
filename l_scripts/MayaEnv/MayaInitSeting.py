from Lugwit_Module import *

if 'maya' in sys.executable:
    import cmds
    
def setCustomFileDialogSidebarUrls(*args):
    cmds.optionVar(sva=["CustomFileDialogSidebarUrls","D:/aa"])
    cmds.optionVar(sva=["CustomFileDialogSidebarUrls","D:/bb"])