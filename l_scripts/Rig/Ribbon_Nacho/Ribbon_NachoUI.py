try:
    import maya.cmds as cmds
except:
    pass
import json,sys,os

'''
Tool Created by Ignacio Zorrilla

Copy this python file to you maya scipts folder, usually located under user/documents/maya/version/scripts

Run this in Maya's python script editor to run the tool
from Ribbon_Nacho import Ribbon_NachoUI
import imp
Ribbon_NachoUI.UI()
imp.reload(Ribbon_NachoUI)
'''


allUIs = {}
curDir=os.path.dirname(__file__)
Path = curDir + '/RiggingTools/'
JsonPath = Path + "DefaultInfo.json"
 
def UI():
    #Get info from JsonFile
    with open(JsonPath, "r") as p:
        data = json.load(p)

    windowID = "Ribbon_Nacho_UI"
    if(cmds.window(windowID,q = True, exists = True)):
        cmds.deleteUI(windowID)

    window = cmds.window(windowID, title = "Ribbon Creation UI", rtf = True, s = True)
    ScrollLayout = cmds.scrollLayout(childResizable=True)

    cmds.setParent(windowID)

    #CREATE NAMING CONVENTION LAYOUT
    NamingLayout = cmds.frameLayout(l = "Naming Convention", cll = True, w = 460, cl = True)
    cmds.text(h = 5, l = "")
    cmds.text(l = "            Naming Convention for ribbon elements", al = "left")
    cmds.separator(h = 5)

    #print data
    cmds.setParent(NamingLayout)

    cmds.rowColumnLayout(nc = 2)
    cmds.text(h = 10, l = "  ")
    allUIs["prefixBtn"] = cmds.checkBox( l = " Use as prefix", v = data[4], cc = UpdateNameUI)
    cmds.setParent(NamingLayout)

    cmds.rowColumnLayout(nc = 5)
    cmds.text(l = "  Joint name:  ", al = "left")
    cmds.text(h = 10, l = "               ")
    allUIs["JointNameField"] = cmds.textField(vis = True, ed = True, w = 150, tx = data[0], cc = UpdateNameUI)
    cmds.text(h = 10, l = "           ")
    allUIs["ResultJointNameText"] = cmds.text('resultJointNameText', label="bn_tail01", font="obliqueLabelFont", align='left')

    cmds.text(l = "  Controller name:  ", al = "left")
    cmds.text(h = 10, l = "              ")
    allUIs["CCNameField"] = cmds.textField(vis = True, ed = True, w = 120, tx = data[1], cc = UpdateNameUI)
    cmds.text(h = 10, l = "           ")
    allUIs["ResultCCNameText"] = cmds.text('resultControllerNameText', label="cc_tail01", font="obliqueLabelFont", align='left')

    cmds.text(l = "  Locator name:  ", al = "left")
    cmds.text(h = 10, l = "              ")
    allUIs["LocatorNameField"] = cmds.textField(vis = True, ed = True, w = 120, tx = data[2], cc = UpdateNameUI)
    cmds.text(h = 10, l = "           ")
    allUIs["ResultLocNameText"] = cmds.text('resultLocatorNameText', label="locAlign_cc_tail01", font="obliqueLabelFont", align='left')

    cmds.text(l = "  Group name:  ", al = "left")
    cmds.text(h = 10, l = "           ")
    allUIs["GroupNameField"] = cmds.textField(vis = True, ed = True, w = 120, tx = data[3], cc = UpdateNameUI)
    cmds.text(h = 10, l = "           ")
    allUIs["ResultGroupNameText"] = cmds.text('resultGroupNameText', label="grp_cc_tail01", font="obliqueLabelFont", align='left')

    cmds.setParent(NamingLayout)

    cmds.rowColumnLayout(nc = 2)
    cmds.text(h = 10, l = "                                                 ")
    cmds.button(l = "Save as Deafult", w = 100, h = 20, c = lambda *x: saveDefaultUI())
    cmds.text(h = 10, l = "")
    cmds.text(h = 10, l = "")

    cmds.setParent(NamingLayout)

    cmds.setParent(NamingLayout)

    #CREATE RIBBON CREATION LAYOUT

    cmds.setParent(ScrollLayout)
    RibbonLayout = cmds.frameLayout(l = "Ribbon Creation", cll = True, w = 300)
    cmds.text(h = 5, l = "")
    cmds.text(l = "            Main Section of the UI: Ribbon Creation", al = "left")
    cmds.separator(h = 5)

    cmds.setParent(RibbonLayout)

    cmds.rowColumnLayout(nc = 3)
    cmds.text(l = "  Ribbon name:  ", al = "left")
    cmds.text(h = 5, l = "")
    allUIs["RibbonNameField"] = cmds.textField(vis = True, ed = True, w = 250, tx = "tail", cc = UpdateNameUI)

    cmds.setParent(RibbonLayout)
    #Bones and Controller Number Section
    cmds.rowColumnLayout(nc = 1)
    allUIs["BonesNumberSlider"] = cmds.intSliderGrp(l = "  Number of Bones:  ", min = 0, max = 50, field = True, ad3 = True, cw3 = [30, 50, 250], cl3 = ["left","left","left"], v = 5)
    allUIs["ControllerNumberSlider"] = cmds.intSliderGrp(l = "  Number of Controllers:    ", min = 0, max = 50, field = True, ad3 = True, cw3 = [30, 50, 250], cl3 = ["left","left","left"], v = 3)
    cmds.setParent(RibbonLayout)

    cmds.rowColumnLayout(nc = 5)
    cmds.text(l = "  Controller Scale:    ", al = "left")
    allUIs["CCScaleField"] = cmds.textField(vis = True, ed = True, w = 50, tx = "1")
    cmds.text(h = 5, l = "               ")
    cmds.text(l = "  Ribbon Width:    ", al = "left")
    allUIs["RibbonWidth"] = cmds.textField(vis = True, ed = True, w = 50, tx = "1")
    cmds.setParent(RibbonLayout)

    cmds.separator(h = 3)
    cmds.rowColumnLayout(nc = 4)
    cmds.text(l = "  Direction:    ", al = "left")
    RibbonDirection = cmds.radioCollection()
    allUIs["DirX"] = cmds.radioButton("X       ", al = "center", sl = True)
    allUIs["DirY"] = cmds.radioButton("Y       ", al = "center")
    allUIs["DirZ"] = cmds.radioButton("Z       ", al = "center")

    cmds.setParent(RibbonLayout)

    cmds.separator(h = 3)

    cmds.setParent(RibbonLayout)

    cmds.rowColumnLayout(nc = 3)
    cmds.text(h = 5, l = "       ")
    allUIs["DriverMiddle"] = cmds.checkBox( l = "   Attach Ribbon to Both Ends  ", v = False, ofc = lambda *x: ShowFK(), onc = lambda *x: HideFK())
    allUIs["DriverMiddleInfoButton"] = cmds.button(label="?", align='left', command=lambda *x:ShowInfoAttach(), w = 20, enable = True)
    cmds.setParent(RibbonLayout)
    cmds.rowColumnLayout(nc = 2)
    cmds.text(h = 5, l = "       ")
    allUIs["addFK"] = cmds.checkBox( l = "   Add FK", v = True)
    cmds.text(h = 5, l = "       ")
    allUIs["addDeformers"] = cmds.checkBox( l = "   Add Deformers", v = True , onc = lambda *x: ShowDeformers(), ofc = lambda *x: HideDeformers())

    cmds.setParent(RibbonLayout)

    cmds.rowColumnLayout(nc = 4)
    cmds.text(h = 5, l = "               ")
    allUIs["SineDeformer"] = cmds.checkBox( l = "   Sine", v = True)
    cmds.text(h = 5, l = "       ")
    allUIs["TwistDeformer"] = cmds.checkBox( l = "   Twist", v = True)
    cmds.text(h = 5, l = "               ")
    allUIs["VolumeDeformer"] = cmds.checkBox( l = "   Volume", v = True)
    cmds.text(h = 5, l = "               ")
    allUIs["RollDeformer"] = cmds.checkBox( l = "   Roll", v = True)

    cmds.setParent(RibbonLayout)

    cmds.rowColumnLayout(nc = 2)
    cmds.text(h = 5, l = "       ")
    allUIs["ParentToHierarchy"] = cmds.checkBox( l = "   Parent to hierarchy", v = False, onc = lambda *x: ShowParents(), ofc = lambda *x: HideParents())
    cmds.setParent(RibbonLayout)

    #Parent Joint UI
    cmds.rowColumnLayout(nc = 5)
    cmds.text(l = "                Parent Joint:    ", al = "left")
    cmds.text(h = 5, l = "   ")
    allUIs["ParentJointField"] = cmds.textField(vis = True, enable = False, w = 150, tx = "")
    cmds.text(h = 5, l = "   ")
    allUIs["ParentJointButton"] = cmds.button(label="<<<", align='left', backgroundColor=(0.25,0.25,0.25), command=lambda *x:assignField(field = allUIs["ParentJointField"]), w = 60, enable = False)

    #Parent Controller UI
    cmds.text(l = "                Parent Controller:    ", al = "left")
    cmds.text(h = 5, l = "   ")
    allUIs["ParentCCField"] = cmds.textField(vis = True, enable = False, w = 150, tx = "")
    cmds.text(h = 5, l = "   ")
    allUIs["ParentCCButton"] = cmds.button(label="<<<", align='left', backgroundColor=(0.25,0.25,0.25), command=lambda *x:assignField(field = allUIs["ParentCCField"]), w = 60, enable = False)

    #Parent extra nodes UI
    cmds.text(l = "                Parent Extra nodes:    ", al = "left")
    cmds.text(h = 5, l = "   ")
    allUIs["ParentExtrasField"] = cmds.textField(vis = True, enable = False, w = 150, tx = "")
    cmds.text(h = 5, l = "   ")
    allUIs["ParentExtrasButton"] = cmds.button(label="<<<", align='left', backgroundColor=(0.25,0.25,0.25), command=lambda *x:assignField(field = allUIs["ParentExtrasField"]), w = 60, enable = False)

    #Buttons Ribbon Creation UI
    cmds.setParent(RibbonLayout)

    cmds.separator(h = 3)
    cmds.rowColumnLayout(nc = 2)
    cmds.text(l = "    1st (Optional): Show Ribbon's NURBS Surface to check size and position     ", al = "left")
    allUIs["ShowGuidesInfoButton"] = cmds.button(label="?", align='left', command=lambda *x:ShowInfoGuides(), w = 20, h = 15,enable = True)
    cmds.setParent(RibbonLayout)
    cmds.rowColumnLayout(nc = 1)
    cmds.text(l = "            Select a NURBS Curve or nothing    ", al = "left")
    cmds.setParent(RibbonLayout)

    cmds.rowColumnLayout(nc = 4)
    cmds.text(h = 5, l = "       ")
    allUIs["RibbonGuidesButton"] = cmds.button(l = "CREATE RIBBON GUIDES", w = 300, h = 40, c = lambda *x: createGuides(allUIs))
    cmds.text(h = 5, l = "   ")
    allUIs["RibbonClearButton"] = cmds.button(l = "CLEAR", w = 110, h = 20, c = lambda *x: ClearGuides(allUIs), bgc = [0.9,1,1])

    cmds.setParent(RibbonLayout)
    cmds.rowColumnLayout(nc = 1)
    cmds.text(l = "    2nd. CREATE RIBBON.    ", al = "left")
    cmds.rowColumnLayout(nc = 1)
    cmds.text(l = "            Select a NURBS Curve or nothing    ", al = "left")
    cmds.setParent(RibbonLayout)

    cmds.rowColumnLayout(nc = 2)
    cmds.text(h = 5, l = "       ")
    allUIs["RibbonButton"] = cmds.button(l = "CREATE RIBBON", w = 420, h = 50, c = lambda *x: CreateRibbon())
    cmds.text(h = 5, l = "       ")
    cmds.text(h = 5, l = "       ")

    #CREATE CONTROLER CREATION LAYOUT
    cmds.setParent(ScrollLayout)
    ControllerLayout = cmds.frameLayout(l = "Controller Creation (Optional)", cll = True, w = 420, cl = True)
    cmds.text(h = 5, l = "")
    cmds.text(l = "            Change shape and color of controllers", al = "left")
    cmds.separator(h = 5)
    cmds.setParent(ControllerLayout)

    cmds.rowColumnLayout(nc = 4)
    cmds.text(l = "      Controller Shape:     ", al = "left")
    allUIs["IKCCSHape"] = cmds.optionMenu(w = 100)
    cmds.menuItem( label='Cube')
    cmds.menuItem( label='Circle')
    cmds.menuItem( label='Star')
    cmds.menuItem( label='Square')
    cmds.menuItem( label='Diamond')
    cmds.menuItem( label='Plus')

    cmds.text(l = "      Controller Color:", al = "left")
    allUIs["IKColor"] = cmds.optionMenu(w = 100)
    cmds.menuItem( label='Yellow')
    cmds.menuItem( label='Red')
    cmds.menuItem( label='Blue')
    cmds.menuItem( label='Green')
    cmds.menuItem( label='LightBlue')
    cmds.menuItem( label='Pink')

    cmds.text(l = "      FK Controller Shape:         ", al = "left")
    allUIs["FKCCSHape"] = cmds.optionMenu(w = 100)
    cmds.menuItem( label='Circle')
    cmds.menuItem( label='Cube')
    cmds.menuItem( label='Star')
    cmds.menuItem( label='Square')
    cmds.menuItem( label='Diamond')
    cmds.menuItem( label='Plus')

    cmds.text(l = "      FK Controller Color:   ", al = "left")
    allUIs["FKColor"] = cmds.optionMenu(w = 100)
    cmds.menuItem( label='Red')
    cmds.menuItem( label='Yellow')
    cmds.menuItem( label='Blue')
    cmds.menuItem( label='Green')
    cmds.menuItem( label='LightBlue')
    cmds.menuItem( label='Pink')

    cmds.setParent(ControllerLayout)

    cmds.rowColumnLayout(nc = 1)
    cmds.text(h = 5, l = "       ")
    cmds.text(h = 5, l = "       ")
    cmds.setParent(ControllerLayout)

    #CREATE CONTACT CREATION LAYOUT
    cmds.setParent(ScrollLayout)
    ContactLayout = cmds.frameLayout(l = "Contact", cll = True, w = 420, cl = True)

    cmds.rowColumnLayout(nc = 2)
    cmds.text(h = 5, l = "")
    cmds.text(l = "            Tool Created by Ignacio Zorrilla", al = "left")
    cmds.text(h = 5, l = "")
    cmds.text(l = "            Email: izbarbera94@gmail.com", al = "left")


    cmds.setParent(ContactLayout)

    #SHOW WINDOW
    cmds.showWindow(windowID)

def UpdateNameUI(*args):
    jointName = cmds.textField(allUIs["JointNameField"], query=True, text=True)
    ccName = cmds.textField(allUIs["CCNameField"], query=True, text=True)
    locName = cmds.textField(allUIs["LocatorNameField"], query=True, text=True)
    grpName = cmds.textField(allUIs["GroupNameField"], query=True, text=True)
    ribbonName = cmds.textField(allUIs["RibbonNameField"], query=True, text=True)

    #FinalJointName
    if cmds.checkBox(allUIs["prefixBtn"], query=True, value=True):
        FinalJointName = ribbonName + "01_" + jointName
    else:
        FinalJointName = jointName + "_" + ribbonName + "01"

    #Final Controller Name
    if cmds.checkBox(allUIs["prefixBtn"], query=True, value=True):
        FinalCCName = ribbonName + "01_" + ccName
    else:
        FinalCCName = ccName  + "_" + ribbonName + "01"

    #Final Locator Name
    if cmds.checkBox(allUIs["prefixBtn"], query=True, value=True):
        FinalLocName = ribbonName + "01_" + ccName + "_" + locName
    else:
        FinalLocName = locName + "_" + ccName + "_" + ribbonName + "01"

    #Final Grp Name
    if cmds.checkBox(allUIs["prefixBtn"], query=True, value=True):
        FinalGrpName = ribbonName + "01_" + ccName + "_" +grpName
    else:
        FinalGrpName = grpName + "_" + ccName + "_" + ribbonName + "01"

    #Set Joint name
    cmds.text(allUIs["ResultJointNameText"], edit=True, label=FinalJointName)
    cmds.text(allUIs["ResultCCNameText"], edit=True, label=FinalCCName)
    cmds.text(allUIs["ResultLocNameText"], edit=True, label=FinalLocName)
    cmds.text(allUIs["ResultGroupNameText"], edit=True, label=FinalGrpName)

def saveDefaultUI():
    #Create Emty list to store data
    JsonInfo = []

    #Get info from textfields
    jointName = cmds.textField(allUIs["JointNameField"], query=True, text=True)
    ccName = cmds.textField(allUIs["CCNameField"], query=True, text=True)
    locName = cmds.textField(allUIs["LocatorNameField"], query=True, text=True)
    grpName = cmds.textField(allUIs["GroupNameField"], query=True, text=True)
    prefixBtn = cmds.checkBox(allUIs["prefixBtn"], query=True, v=True)

    JsonInfo.append(jointName)
    JsonInfo.append(ccName)
    JsonInfo.append(locName)
    JsonInfo.append(grpName)
    JsonInfo.append(prefixBtn)

    with open(JsonPath, 'w') as p:
        json.dump(JsonInfo, p, indent = 4)

    print ("Saved Succesfully")

def ShowFK():
    cmds.checkBox(allUIs["addFK"], edit=True, enable=True, v= True)

def HideFK():
    cmds.checkBox(allUIs["addFK"], e = True, enable = False, v= False)

def ShowDeformers():
    cmds.checkBox(allUIs["SineDeformer"], edit=True, enable=True, v= True)
    cmds.checkBox(allUIs["TwistDeformer"], e = True, enable = True, v= True)
    cmds.checkBox(allUIs["VolumeDeformer"], e = True, enable = True, v= True)
    cmds.checkBox(allUIs["RollDeformer"], e = True, enable = True, v= True)

def HideDeformers():
    cmds.checkBox(allUIs["SineDeformer"], e = True, enable = False, v= False)
    cmds.checkBox(allUIs["TwistDeformer"], e = True, enable = False, v= False)
    cmds.checkBox(allUIs["VolumeDeformer"], e = True, enable = False, v= False)
    cmds.checkBox(allUIs["RollDeformer"], e = True, enable = False, v= False)

def ShowParents():
    cmds.textField(allUIs["ParentJointField"], edit=True, enable=True)
    cmds.textField(allUIs["ParentCCField"], edit=True, enable=True)
    cmds.textField(allUIs["ParentExtrasField"], edit=True, enable=True)

    cmds.button(allUIs["ParentJointButton"], e = True, enable = True)
    cmds.button(allUIs["ParentCCButton"], e = True, enable = True)
    cmds.button(allUIs["ParentExtrasButton"], e = True, enable = True)

def HideParents():
    cmds.textField(allUIs["ParentJointField"], edit=True, enable=False)
    cmds.textField(allUIs["ParentCCField"], edit=True, enable=False)
    cmds.textField(allUIs["ParentExtrasField"], edit=True, enable=False)

    cmds.button(allUIs["ParentJointButton"], e = True, enable = False)
    cmds.button(allUIs["ParentCCButton"], e = True, enable = False)
    cmds.button(allUIs["ParentExtrasButton"], e = True, enable = False)

def assignField(field):
    #Get selection
    selection = cmds.ls(sl = True)
    if len(selection) >=2:
        cmds.confirmDialog( icn = "warning", title='ERROR!', message='Please select just 1 object before clicking this button', button=['OK'], ma='center')
    elif len(selection)==0:
        cmds.confirmDialog( icn = "warning", title='ERROR!', message='Please select just 1 object before clicking this button', button=['OK'], ma='center')
    else:
        cmds.textField(field, edit=True, text=selection[0])

def createGuides(allUIs):
    from Ribbon_Nacho.RiggingTools import CreateGuides
    reload(CreateGuides)
    Guides = CreateGuides.CreateGuides(allUIs)

def ClearGuides(allUIs):
    from Ribbon_Nacho.RiggingTools import CreateGuides
    reload(CreateGuides)
    Guides = CreateGuides.ClearGuides(allUIs)

def ShowInfoAttach():
    cmds.confirmDialog( icn = "information", title='Information', ma='center', message=" This checkbox is useful when you want both ends of the ribbon to be the drivers of the rest of the controllers.                                                                                    "
                                                                                       "When you want both ends to be still while the middle moving.                                    "
                                                                                       "____________________________________________________________________________    "
                                                                                       "Example: Rope between two poles", button=['OK'])

def ShowInfoGuides():
    cmds.confirmDialog( icn = "information", title='Information', ma='center', message='This will show the nurbs surface before the creation of the Ribbon.                                  '
                                                                                       'It will allow you to adjust the shape of the surface or change the direction', button=['OK'])

def CreateRibbon():
    from Ribbon_Nacho.RiggingTools import CreateRibbon
    reload(CreateRibbon)
    CreateRibbon.CreateRibbon(allUIs)



UI()





