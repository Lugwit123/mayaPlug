import maya.cmds as cmds

Path = cmds.internalVar(usd = True) + 'Ribbon_Nacho/RiggingTools/'


def createController(allUIs, FKCC):
    CCScale = cmds.textField(allUIs["CCScaleField"], q = True, text = True)
    CCShape = cmds.optionMenu(allUIs["IKCCSHape"], q = True, v = True)
    Color = cmds.optionMenu(allUIs["IKColor"], q = True, v = True)
    FKCCShape = cmds.optionMenu(allUIs["FKCCSHape"], q = True, v = True)
    FKCCColor = cmds.optionMenu(allUIs["FKColor"], q = True, v = True)

    if FKCC == True:
        CCShape = FKCCShape
        Color = FKCCColor
        CCScale = float(CCScale) * 2
    else:
        pass

    #Define Color variables
    if Color == "Red":
        colorCode = 13
    if Color == "Pink":
        colorCode = 9
    if Color == "Green":
        colorCode = 14
    elif Color == "Blue":
        colorCode = 6
    elif Color == "Yellow":
        colorCode = 17
    elif Color == "LightBlue":
        colorCode = 18

    #Create Controllers
    if CCShape == "Cube":
        Controller = cmds.curve(p=[(-1.0, 1.0, 1.0), (-1.0, 1.0, -1.0), (1.0, 1.0, -1.0),
                         (1.0, 1.0, 1.0), (-1.0, 1.0, 1.0), (-1.0, -1.0, 1.0),
                         (1.0, -1.0, 1.0), (1.0, -1.0, -1.0), (-1.0, -1.0, -1.0),
                         (-1.0, -1.0, 1.0), (-1.0, -1.0, -1.0), (-1.0, 1.0, -1.0),
                         (1.0, 1.0, -1.0), (1.0, -1.0, -1.0), (1.0, -1.0, 1.0), (1.0, 1.0, 1.0)],
                         k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], d=1, n= "temp_cc_name")

    if CCShape == "Circle":
        Controller = cmds.circle(d = 3, n= "temp_cc_name")
        cmds.select(Controller[0] + ".cv[0:7]")
        cmds.rotate(0, 90, 0)

    if CCShape == "Star":
        Controller = cmds.circle(d = 3, n= "temp_cc_name")
        cmds.select(Controller[0] + ".cv[2]", Controller[0] + ".cv[0]", Controller[0] + ".cv[4]", Controller[0] + ".cv[6]")
        cmds.scale(0, 0, 0, r = True)
        cmds.select(Controller[0] + ".cv[0:7]")
        cmds.rotate(0, 90, 0)
        cmds.scale(2, 2, 2, r = True)
        cmds.select(cl = True)

    if CCShape == "Square":
        Controller = cmds.curve(d=1, p=[(-1,0,-1),(1,0,-1),(1,0,1),(-1,0,1), (-1,0,-1)], k=[0,1,2,3,4], n= "temp_cc_name")
        cmds.select(Controller + ".cv[0:4]")
        cmds.rotate(0, 0, 90)
        cmds.move(-1, 0, 0, r = True, os = True, wd = True)

    if CCShape == "Diamond":
        Controller = cmds.curve(d=1, p=[(0, 1, 0),(-1, 0.00278996, 6.18172e-08),(0, 0, 1),(0, 1, 0),(1, 0.00278996, 0),
            (0, 0, 1),(1, 0.00278996, 0),(0, 0, -1),(0, 1, 0),(0, 0, -1),
            (-1, 0.00278996, 6.18172e-08),(0, -1, 0),(0, 0 ,-1),(1, 0.00278996, 0),
            (0, -1, 0),(0, 0, 1)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], n = "temp_cc_name")

    if CCShape == "Plus":
        Controller = cmds.curve(d=1, p=[(-1,0,-3),(1,0,-3),(1,0,-1),(3,0,-1),(3,0,1),(1,0,1),(1,0,3),(-1,0,3),(-1,0,1),(-3,0,1),(-3,0,-1),(-1,0,-1),(-1,0,-3)], k=[0,1,2,3,4,5,6,7,8,9,10,11,12], n = "temp_cc_name")

    ControllerList = cmds.ls(Controller)
    shapes = cmds.listRelatives(ControllerList, s = True)

    #Change Controller Scale
    cmds.setAttr(ControllerList[0] + ".scaleX", float(CCScale))
    cmds.setAttr(ControllerList[0] + ".scaleY", float(CCScale))
    cmds.setAttr(ControllerList[0] + ".scaleZ", float(CCScale))

    cmds.makeIdentity(ControllerList[0], a = True)

    #Change Controller Color
    for shape in shapes:
        cmds.setAttr(shape + ".overrideEnabled", 1)
        cmds.setAttr(shape + ".overrideColor", colorCode)











