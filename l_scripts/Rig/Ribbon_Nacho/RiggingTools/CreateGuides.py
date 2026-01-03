import maya.cmds as cmds

allUIs = {}
Path = cmds.internalVar(usd = True) + 'Ribbon_Nacho/RiggingTools/'
JsonPath = Path + "DefaultInfo.json"

def CreateGuides(allUIs):
    AsPrefix = cmds.checkBox(allUIs["prefixBtn"], q = True, v = True)
    Name = cmds.textField(allUIs["RibbonNameField"], q = True, text = True)
    BonesNumber = cmds.intSliderGrp(allUIs["BonesNumberSlider"], q = True, v = True)
    RibbonWidth = float(cmds.textField(allUIs["RibbonWidth"], q = True, text = True))
    RibbonDirection = [0, 0, 0]
    DirX = cmds.radioButton(allUIs["DirX"], q = True, sl = True)
    DirY = cmds.radioButton(allUIs["DirY"], q = True, sl = True)
    DirZ = cmds.radioButton(allUIs["DirZ"], q = True, sl = True)
    if DirX == True:
        RibbonDirection[0] = 1.0
    elif DirY == True:
        RibbonDirection[1] = 1.0
    else:
        RibbonDirection[2] = 1.0

    if AsPrefix == True:
        CrvGuideName = Name + '_crvGuide'
    else:
        CrvGuideName = 'crvGuide_' + Name

    #Create Ribbon  bind nurbs
    selection = cmds.ls(sl = True) or []
    selectionType = cmds.listRelatives(selection, shapes=True)
    nodeType = cmds.nodeType(selectionType)

    if AsPrefix == True:
        surfaceGuideName = Name + '_surfaceGuide'
    else:
        surfaceGuideName = 'surfaceGuide_' + Name

    if cmds.objExists(surfaceGuideName) == True:
        cmds.confirmDialog( icn = "warning", title='ERROR!', message='Clear Guides before clicking me again', button=['OK'], ma='center')

    else:
        if len(selection) and not nodeType == 'nurbsCurve':
            #Pop Up Warning: Something that is not a Nurbs Curve is selected
            cmds.confirmDialog( icn = "warning", title='ERROR!', message='A nurbs surface Guide with the given name already exists. Plase the change the name of the Ribbon', button=['OK'], ma='center')
        else:
            if len(selection) and nodeType == 'nurbsCurve':
                BaseCurve = selection[0]
                #Clean Curve Selected
                cmds.makeIdentity(BaseCurve, apply = True)
                cmds.delete(BaseCurve, ch = True)

                # "create a ribbon using crv selected"
                cmds.select(BaseCurve, r = True)
                cmds.rebuildCurve(BaseCurve, ch = False, s = BonesNumber, d = 3)
                cmds.makeIdentity(BaseCurve, apply = True)
                curveOne = cmds.duplicate(BaseCurve)
                curveTwo = cmds.duplicate(BaseCurve)
                cmds.select(curveOne, r = True)
                cmds.move( RibbonDirection[0]/2 * RibbonWidth, RibbonDirection[1]/2 * RibbonWidth, RibbonDirection[2]/2 * RibbonWidth)
                cmds.select(curveTwo, r = True)
                cmds.move(-1 * RibbonDirection[0]/2 * RibbonWidth, -1 * RibbonDirection[1]/2 * RibbonWidth, -1 * RibbonDirection[2]/2 * RibbonWidth, ws = True)
                if AsPrefix == True:
                    ribbonNurbs = cmds.loft(curveTwo, curveOne, n = Name + '_surfaceGuide', ch = False, rsn = True)
                else:
                    ribbonNurbs = cmds.loft(curveTwo, curveOne, n = 'surfaceGuide_' + Name , ch = False, rsn = True)

                cmds.rebuildSurface(ribbonNurbs[0],ch = False, su = BonesNumber - 1, sv = 1, du = 3, dv = 3)

                #clean up:
                cmds.delete(curveOne)
                cmds.delete(curveTwo)
                #Clean Crv
                cmds.makeIdentity(BaseCurve, apply = True)
                cmds.delete(BaseCurve, ch = True)
                if AsPrefix == True:
                    BaseCurve = cmds.rename(BaseCurve, Name + "_crvGuide")
                else:
                    BaseCurve = cmds.rename(BaseCurve, "crvGuide_" + Name)
                #Clean Nurbs Surface
                cmds.makeIdentity(ribbonNurbs[0], apply = True)
                cmds.delete(ribbonNurbs[0], ch = True)

            else:
                if cmds.objExists(CrvGuideName) == True:
                    cmds.select(CrvGuideName)
                    selection = cmds.ls(sl = True)
                    BaseCurve = selection[0]
                    #Clean Curve Selected
                    cmds.makeIdentity(BaseCurve, apply = True)
                    cmds.delete(BaseCurve, ch = True)

                    # "create a ribbon using crv selected"
                    cmds.select(BaseCurve, r = True)
                    cmds.rebuildCurve(BaseCurve, ch = False, s = BonesNumber, d = 3)
                    cmds.makeIdentity(BaseCurve, apply = True)
                    curveOne = cmds.duplicate(BaseCurve)
                    curveTwo = cmds.duplicate(BaseCurve)
                    cmds.select(curveOne, r = True)
                    cmds.move( RibbonDirection[0]/2 * RibbonWidth, RibbonDirection[1]/2 * RibbonWidth, RibbonDirection[2]/2 * RibbonWidth)
                    cmds.select(curveTwo, r = True)
                    cmds.move(-1 * RibbonDirection[0]/2 * RibbonWidth, -1 * RibbonDirection[1]/2 * RibbonWidth, -1 * RibbonDirection[2]/2 * RibbonWidth, ws = True)
                    if AsPrefix == True:
                        ribbonNurbs = cmds.loft(curveTwo, curveOne, n = Name + '_surfaceGuide', ch = False, rsn = True)
                    else:
                        ribbonNurbs = cmds.loft(curveTwo, curveOne, n = 'surfaceGuide_' + Name , ch = False, rsn = True)

                    cmds.rebuildSurface(ribbonNurbs[0],ch = False, su = BonesNumber - 1, sv = 1, du = 3, dv = 3)

                    #clean up:
                    cmds.delete(curveOne)
                    cmds.delete(curveTwo)
                    #Clean Crv
                    cmds.makeIdentity(BaseCurve, apply = True)
                    cmds.delete(BaseCurve, ch = True)
                    if AsPrefix == True:
                        BaseCurve = cmds.rename(BaseCurve, Name + "_crvGuide")
                    else:
                        BaseCurve = cmds.rename(BaseCurve, "crvGuide_" + Name)
                    #Clean Nurbs Surface
                    cmds.makeIdentity(ribbonNurbs[0], apply = True)
                    cmds.delete(ribbonNurbs[0], ch = True)


                else:
                    #Create Ribbon from Scratch: Nothing is selected
                    if AsPrefix == True:
                        ribbonNurbs = cmds.nurbsPlane(u = BonesNumber,ax = (RibbonDirection[0], RibbonDirection[1], RibbonDirection[2]), n = Name + '_surfaceGuide', lr = 1.0/BonesNumber, w = BonesNumber)
                    else:
                        ribbonNurbs = cmds.nurbsPlane(u = BonesNumber,ax = (RibbonDirection[0], RibbonDirection[1], RibbonDirection[2]), n = 'surfaceGuide_' + Name , lr = 1.0/BonesNumber, w = BonesNumber)
                    # crete a curve here as the base curve
                    cmds.select(ribbonNurbs[0] + ".v[0.5]", r = True)
                    if AsPrefix == True:
                        BaseCurve = cmds.duplicateCurve(ribbonNurbs[0] + ".v[0.5]", n = Name + "_crvGuide",ch = False)
                    else:
                        BaseCurve = cmds.duplicateCurve(ribbonNurbs[0] + ".v[0.5]", n = "crvGuide_" + Name ,ch = False)


def ClearGuides(allUIs):
    AsPrefix = cmds.checkBox(allUIs["prefixBtn"], q = True, v = True)
    Name = cmds.textField(allUIs["RibbonNameField"], q = True, text = True)

    if AsPrefix == True:
        surfaceGuideName = Name + '_surfaceGuide'
    else:
        surfaceGuideName = 'surfaceGuide_' + Name
    print "clearing Guides"
    if cmds.objExists(surfaceGuideName) == True:
        cmds.delete(surfaceGuideName)
    else:
        cmds.confirmDialog( icn = "warning", title='ERROR!', message="A guide with the name: '" + surfaceGuideName + "' doesn't exist, so nothing hapenned", button=['OK'], ma='center')








