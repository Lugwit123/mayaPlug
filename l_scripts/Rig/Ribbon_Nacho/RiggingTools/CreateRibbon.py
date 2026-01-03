import maya.cmds as cmds
import sys

def CreateRibbon(allUIs):
    AsPrefix = cmds.checkBox(allUIs["prefixBtn"], q = True, v = True)
    BoneName = cmds.textField(allUIs["JointNameField"], q = True, text = True)
    CCName = cmds.textField(allUIs["CCNameField"], q = True, text = True)
    LocatorName = cmds.textField(allUIs["LocatorNameField"], q = True, text = True)
    GrpName = cmds.textField(allUIs["GroupNameField"], q = True, text = True)
    Name = cmds.textField(allUIs["RibbonNameField"], q = True, text = True)
    BonesNumber = cmds.intSliderGrp(allUIs["BonesNumberSlider"], q = True, v = True)
    CCNumber = cmds.intSliderGrp(allUIs["ControllerNumberSlider"], q = True, v = True)
    CCScale = cmds.textField(allUIs["CCScaleField"], q = True, text = True)
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

    Attach = cmds.checkBox(allUIs["DriverMiddle"], q = True, v = True)
    AddFK = cmds.checkBox(allUIs["addFK"], q = True, v = True)
    Deformers = cmds.checkBox(allUIs["addDeformers"], q = True, v = True)
    ParentToHierarchy = cmds.checkBox(allUIs["ParentToHierarchy"], q = True, v = True)
    ParentJoint = cmds.textField(allUIs["ParentJointField"], q = True, text = True)
    ParentCC = cmds.textField(allUIs["ParentCCField"], q = True, text = True)
    ParentExtras = cmds.textField(allUIs["ParentExtrasField"], q = True, text = True)
    CCColor = cmds.optionMenu(allUIs["IKColor"], q = True, v = True)

    if AsPrefix == True:
        NurbsSurfaceName = Name + '_surface'
        FinalBoneName = Name + "_" + BoneName
        surfaceGuideName = Name + '_surfaceGuide'
        BaseCurveName =  Name + "_crv"
        CrvGuideName = Name + '_crvGuide'
    else:
        NurbsSurfaceName = 'surface_' + Name
        surfaceGuideName = 'surfaceGuide_' + Name
        FinalBoneName = BoneName + "_" + Name
        BaseCurveName = "crv_" + Name
        CrvGuideName = 'crvGuide_' + Name

    #Create Ribbon  bind nurbs
    selection = cmds.ls(sl = True) or []
    selectionType = cmds.listRelatives(selection, shapes=True)
    nodeType = cmds.nodeType(selectionType)

    if cmds.objExists(NurbsSurfaceName) == True:
        cmds.confirmDialog( icn = "warning", title='ERROR!', message='A nurbs surface with the given name already exists. Plase the change the name of the Ribbon', button=['OK'], ma='center')

    else:
        #Check if there is guide surface
        if cmds.objExists(surfaceGuideName) == True:
            Guide = surfaceGuideName
            #Rename guide
            cmds.rename(Guide, NurbsSurfaceName)
            ribbonNurbs = cmds.ls(NurbsSurfaceName)

            cmds.rename(CrvGuideName, BaseCurveName)

            BaseCurve = BaseCurveName

            if Attach == True:
                DriverSurface = cmds.duplicate(ribbonNurbs[0], name=ribbonNurbs[0].replace("surface", "surface_Driver"))
                ribbonDriverNurbs = cmds.rebuildSurface(DriverSurface[0],ch = False, su = CCNumber -1, sv = 1, du = 3, dv = 3)
        else:
            if len(selection) and not nodeType == 'nurbsCurve':
                #Pop Up Warning: Something that is not a Nurbs Curve is selected
                cmds.confirmDialog( icn = "warning", title='ERROR!', message='You must select a nurbs Curve or nothing', button=['OK'], ma='center')
                sys.exit()

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

                    #Create Nurbs Surface
                    ribbonNurbs = cmds.loft(curveTwo, curveOne, n = NurbsSurfaceName , ch = False, rsn = True)

                    cmds.rebuildSurface(ribbonNurbs[0],ch = False, su = BonesNumber - 1, sv = 1, du = 3, dv = 3)

                    #clean up:
                    cmds.delete(curveOne)
                    cmds.delete(curveTwo)
                    #Clean Crv
                    cmds.makeIdentity(BaseCurve, apply = True)
                    cmds.delete(BaseCurve, ch = True)

                    BaseCurve = cmds.rename(BaseCurve, BaseCurveName)

                    #Clean Nurbs Surface
                    cmds.makeIdentity(ribbonNurbs[0], apply = True)
                    cmds.delete(ribbonNurbs[0], ch = True)

                    if Attach == True:
                        DriverSurface = cmds.duplicate(ribbonNurbs[0], name=ribbonNurbs[0].replace("surface", "surface_Driver"))
                        ribbonDriverNurbs = cmds.rebuildSurface(DriverSurface[0],ch = False, su = CCNumber -1, sv = 1, du = 3, dv = 3)

                else:
                    #Create Ribbon from Scratch: Nothing is selected

                    ribbonNurbs = cmds.nurbsPlane(u = BonesNumber - 1, ax = (RibbonDirection[0], RibbonDirection[1], RibbonDirection[2]), n = NurbsSurfaceName, lr = 1.0/BonesNumber, w = BonesNumber)

                    # crete a curve here as the base curve
                    cmds.select(ribbonNurbs[0] + ".v[0.5]", r = True)

                    BaseCurve = cmds.duplicateCurve(ribbonNurbs[0] + ".v[0.5]", n = BaseCurveName, ch = False)

                    if Attach == True:
                        ribbonDriverNurbs = cmds.nurbsPlane(u = CCNumber-1,ax = (RibbonDirection[0], RibbonDirection[1], RibbonDirection[2]), n = ribbonNurbs[0].replace("surface", "surface_Driver"), lr = 1.0/BonesNumber, w = BonesNumber)

        #CREATE TOP GROUPS
        if AsPrefix == True:
            TopGrp = cmds.group(n = Name + "_Ribbon_" + GrpName, em = True)
            TopBindGroup = cmds.group(n = Name + "_" + BoneName + "_" + GrpName, em = True)
            TopCCGroup = cmds.group(n = Name + "_" + CCName + "_" + GrpName, em = True)
            TopCCBindGroup = cmds.group(n = Name + "_" + CCName + "_" + BoneName + "_" + GrpName, em = True)
            TopExtrasGroup = cmds.group(n = Name + "_" + "Extras" + "_" + GrpName, em = True)
            TopFolliclesGroup = cmds.group(n = Name + "_" + "Follicles" + "_" + GrpName, em = True)
            TopDriverGrp = cmds.group(n = Name + "_Driver_" + BoneName + "_" + GrpName, em = True)

        else:
            TopGrp = cmds.group(n = GrpName + "_Ribbon_" + Name, em = True)
            TopBindGroup = cmds.group(n = GrpName + "_" + BoneName + "_" + Name, em = True)
            TopCCGroup = cmds.group(n = GrpName + "_" + CCName + "_" + Name, em = True)
            TopCCBindGroup = cmds.group(n = GrpName + "_" + CCName + "_" + BoneName + "_" + Name, em = True)
            TopExtrasGroup = cmds.group(n = GrpName + "_" + "Extras" + "_" + Name, em = True)
            TopFolliclesGroup = cmds.group(n = GrpName + "_" + "Follicles" + "_" + Name, em = True)
            TopDriverGrp = cmds.group(n = GrpName + "_Driver_" + BoneName + "_" + Name, em = True)

        #Adjust Hierarchy
        cmds.parent(TopCCBindGroup, TopCCGroup)
        cmds.parent(TopFolliclesGroup, TopExtrasGroup)
        cmds.parent(TopDriverGrp, TopExtrasGroup)

        cmds.setAttr(TopDriverGrp + ".v", 0)
        cmds.setAttr(ribbonNurbs[0] + ".v", 0)
        cmds.setAttr(TopFolliclesGroup + ".v", 0)
        cmds.setAttr(TopCCBindGroup + ".v", 0)

        #start creating folicles and jnts:

        folicleList = []
        bindJntList = []

        for iter in range(1, BonesNumber + 1):
            folicleU = 1.0/(BonesNumber -1) * (iter - 1)
            folicle = createFolicle(ribbonNurbs[0], folicleU, 0.5, iter)
            folicleList.append(folicle[1])

            bindJntHierachy = createJntUnderObj(folicle[1], BoneName, CCName, LocatorName, GrpName, TopBindGroup, TopFolliclesGroup, TopCCBindGroup, CCScale)

            bindJnt = bindJntHierachy[0]

            bindJntList.append(bindJnt)


        #Create Driver Joints to bind to surface
        #start create control jnts:
        ctrlJntGrpList = []
        ctrlJntLocList = []
        ctrlJntList = []
        DrvJointName = FinalBoneName.replace(BoneName, "Driver_" + BoneName)

        for iter in range(1, CCNumber + 1):
            #gather info
            ctrlJntName =  DrvJointName + str(iter).zfill(2)
            uValue = 1.0/(CCNumber - 1.0) * (iter - 1)
            cmds.select(cl = True)
            cmds.joint(n = ctrlJntName, rad = RibbonWidth)
            ctrlJntList.append(ctrlJntName)
            jntGrpList = groupJntHierachy(BoneName, LocatorName, GrpName, ctrlJntName)
            jntGrp = jntGrpList[0]
            jntLocName = jntGrpList[1]
            ctrlJntGrpList.append(jntGrp)
            ctrlJntLocList.append(jntLocName)
            folicleU = 1.0/(CCNumber - 1.0) * (iter - 1)
            folicle = createFolicle(ribbonNurbs[0], folicleU, 0.5, iter, "bn_temp_")

            cmds.matchTransform(jntGrp, folicle[1])
            cmds.delete(folicle)

        #bind ctrl jnts with ribbon:
        cmds.select(ctrlJntList, r = True)
        cmds.select(ribbonNurbs[0], add = True)
        cmds.skinCluster(n = "skinCluster_" + Name)

        #Clean hierarchy
        #Parent Driver Groups under top group
        for grp in ctrlJntGrpList:
            cmds.parent(grp, TopDriverGrp)

        #CREATE MASTER CONTROLLER
        if AsPrefix == True:
            MasterCCName = Name + "_Master_" + CCName
            MasterLocName = Name + "_Master_" + CCName + "_" + LocatorName

        else:
            MasterCCName = CCName + "_Master_" + Name
            MasterLocName = LocatorName + "_" + CCName + "_Master_" + Name

        MasterLoc = cmds.spaceLocator(n = MasterLocName)

        MasterCC = cmds.curve(d=1, p=[(1, 0, 1),(3, 0, 1),(3, 0, 2),(5, 0, 0),(3, 0, -2),(3, 0, -1),(1, 0, -1),(1, 0, -3),(2, 0, -3),(0, 0, -5),(-2, 0, -3),(-1, 0, -3),(-1, 0, -1),(-3, 0, -1),(-3, 0, -2),(-5, 0, 0),(-3, 0, 2),(-3, 0, 1),(-1, 0, 1),(-1, 0, 3),(-2, 0, 3),(0, 0, 5),( 2, 0, 3),(1, 0, 3),(1, 0, 1),], k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24], n= MasterCCName)

        CreateMasterController(CCColor,CCScale, bindJntList, AddFK, MasterCC, MasterLoc, Attach)

        #Connect Master CC Attr to components
        #IK Controllers connected in createController Function
        cmds.connectAttr(MasterCC + ".Extra_Controllers", TopCCBindGroup + ".v")
        cmds.connectAttr(MasterCC + ".NurbsSurface", ribbonNurbs[0] + ".v")

        CCGrpList = []
        CCList = []
        #CREATE CONTROLLERS FOR RIBBON
        for item in ctrlJntList:
            createController(allUIs, FKCC = False)
            #Create locator and group under CC
            if AsPrefix == True:
                FinalLocatorName = CCName + "_" + LocatorName
                FinalGrpName = CCName + "_" + GrpName
            else:
                FinalLocatorName = LocatorName + "_" + CCName
                FinalGrpName = GrpName + "_" + CCName

            CC = cmds.rename("temp_cc_name", item.replace("Driver_" + BoneName, CCName))
            CCGrp = cmds.group(n = item.replace("Driver_" + BoneName, FinalGrpName), em = True)
            CCLoc = cmds.spaceLocator(n = item.replace("Driver_" + BoneName, FinalLocatorName))[0]

            CCGrpList.append(CCGrp)
            CCList.append(CC)

            cmds.parent(CC, CCLoc)
            cmds.parent(CCLoc, CCGrp)

            cmds.matchTransform(item.replace("Driver_" + BoneName, FinalGrpName), item)
            cmds.parentConstraint(item.replace("Driver_" + BoneName, CCName), item)
            cmds.scaleConstraint(item.replace("Driver_" + BoneName, CCName), item, mo = True)

            cmds.parent(CCGrp, MasterCC)
            cmds.connectAttr(MasterCC + ".IK_Controllers", CCGrp + ".v")

        #Clean Attributes of the IK COntrollers
        for cc in CCList:
            cmds.setAttr(cc + ".v", lock = True, keyable = False, channelBox = False)


        #CREATE FK SET UP
        FKCCList = []
        FKCCGrpList = []

        if AddFK == True:
            for item in ctrlJntList:
                createController(allUIs, FKCC = True)
                #Create locator and group under CC
                if AsPrefix == True:
                    FinalLocatorName = "FK_" + CCName + LocatorName
                    FinalGrpName = "FK_" + CCName + GrpName
                else:
                    FinalLocatorName = LocatorName + "_" + CCName + "_FK"
                    FinalGrpName = GrpName + "_" + CCName + "_FK"

                CC = cmds.rename("temp_cc_name", item.replace("Driver_" + BoneName, CCName + "_FK"))
                CCGrp = cmds.group(n = item.replace("Driver_" + BoneName, FinalGrpName), em = True)
                CCLoc = cmds.spaceLocator(n = item.replace("Driver_" + BoneName, FinalLocatorName))[0]

                FKCCList.append(CC)
                FKCCGrpList.append(CCGrp)

                cmds.parent(CC, CCLoc)
                cmds.parent(CCLoc, CCGrp)

                cmds.matchTransform(item.replace("Driver_" + BoneName, FinalGrpName), item)
                cmds.parentConstraint(item.replace("Driver_" + BoneName, CCName), item)

                cmds.parent(CCGrp, MasterCC)
                cmds.connectAttr(MasterCC + ".FK_Controllers", CCGrp + ".v")

            #Parent under previous Controller
            for iter in range(1, len(FKCCList)):
                cmds.parent(FKCCGrpList[iter], FKCCList[iter -1])
            #Parent COnstraint FK COntroller to IK Grp
            for iter in range(0, len(FKCCList)):
                cmds.parentConstraint(FKCCList[iter], CCGrpList[iter])

            for cc in FKCCList:
                cmds.setAttr(cc + ".v", lock = True, keyable = False, channelBox = False)

        #CREATE DRIVER SURFACE
        if Attach == True:
            #Create Follicles for the driver Surface = number of Controllers
            driverFolicleList = []
            for iter in range(1, CCNumber - 1):
                DriverFolicleU = 1.0/(CCNumber - 1.0) * (iter)
                DriverFolicle = createFolicle(ribbonDriverNurbs[0], DriverFolicleU, 0.5, iter)
                cmds.pickWalk(d = "up")
                foliccleFinal = cmds.ls(sl = True)
                driverFolicleList.append(foliccleFinal[0])

            #Create Group for Driver Follicles
            driverFolliclesGrp = cmds.group(driverFolicleList,n = ribbonDriverNurbs[0].replace("surface_Driver", "grp_Driver_follicles"))

                    #CONTROLLER STRETCH
            #Crete joints for driver surface at the start and at the end of the surface
            startDriverJoint = cmds.joint(n = CCList[0].replace(CCName, "Driver_" +CCName + "_" + BoneName))
            cmds.parentConstraint(CCList[0], startDriverJoint)
            cmds.parent(startDriverJoint, w = True)
            endDriverJoint = cmds.joint(n = CCList[-1].replace(CCName, "Driver_" + CCName+ "_" + BoneName))
            cmds.parentConstraint(CCList[-1], endDriverJoint)
            cmds.parent(endDriverJoint, w = True)

            #bind ctrl jnts with ribbon:
            cmds.select(startDriverJoint, endDriverJoint, r = True)
            cmds.select(ribbonDriverNurbs[0], add = True)
            cmds.skinCluster()

            driverSurfaceGrp = cmds.group(n = ribbonDriverNurbs[0].replace("surface_Driver", GrpName + "_Driver"), em = True)
            cmds.parent(startDriverJoint, endDriverJoint, ribbonDriverNurbs[0], driverFolliclesGrp, driverSurfaceGrp)
            cmds.setAttr(driverSurfaceGrp + ".v", 0)

            #Create Connections to Driver the Follow option to drive Controllers
            RevNode01 = cmds.shadingNode('reverse', asUtility=True, n="reverse_" + MasterCC)
            cmds.connectAttr(MasterCC + ".Follow", RevNode01 + ".inputX")

            #Connect Follicles to controller
            for iter in range(1, CCNumber - 1):
                Const = cmds.parentConstraint(MasterCC, driverFolicleList[iter - 1], CCGrpList[iter],mo = True)
                cmds.connectAttr(MasterCC + ".Follow", Const[0] + "." + driverFolicleList[iter - 1] + "W1")
                cmds.connectAttr(RevNode01 + ".output.outputX", Const[0] + "." + MasterCC + "W0")

            #Clean Hierachy
            cmds.parent(driverSurfaceGrp, TopExtrasGroup)

        #CREATE DEFORMERS
        if Deformers == True:
            createDeformers(allUIs, ribbonNurbs, TopCCGroup, bindJntList, folicleList, TopExtrasGroup, MasterCC)
            cmds.select(ribbonNurbs[0])
            cmds.reorderDeformers("skinCluster_" + Name, "bs_deformers_" + Name)

        #Clean Hierarchy
        cmds.parent(ribbonNurbs[0], BaseCurve, TopExtrasGroup)
        cmds.parent(TopBindGroup, TopCCGroup, TopExtrasGroup, TopGrp)
        cmds.parent(MasterLoc, TopCCGroup)
        try:
            cmds.setAttr(BaseCurve + ".v", 0)
        except:
            pass

        #Hide Locators Visibility
        #List all locators under Top Group
        allDescendants = cmds.listRelatives(TopGrp, ad = True, typ = "locator")
        visibleLocators = []

        for obj in allDescendants:
                    #Get locators visibility
            try:
                locVisbility = cmds.getAttr(obj + "Shape" + ".lodVisibility")
                if locVisbility == True:
                    visibleLocators.append(obj)
            except:
                locVisbility = cmds.getAttr(obj + ".lodVisibility")
                if locVisbility == True:
                    visibleLocators.append(obj)
            try:
                cmds.select(obj + "Shape")
                cmds.setAttr(obj + "Shape" + ".lodVisibility", 0)
            except:
                cmds.setAttr(obj + ".lodVisibility", 0)


        visibleLocators[:] = []

        #Create Ribbon Set
        if cmds.objExists("set_BindJoitns_" + Name) == True:
            for joint in bindJntList:
                if cmds.objectType(joint) == "joint":
                    cmds.sets(joint, add="set_BindJoitns_" + Name)
        else:
            cmds.sets(n = "set_BindJoitns_" + Name)
            for joint in bindJntList:
                if cmds.objectType(joint) == "joint":
                    cmds.sets(joint, add="set_BindJoitns_" + Name)

        #Hide Visibility for all locators

        #ADJUST HIERARCHY IF PARENT TO HEIRARCHY CHECKBOX IS CHECKED

        #Parent Joints
        if ParentToHierarchy == True:
            #Parent Joints
            if not ParentJoint == "":
                for item in bindJntList:
                    cmds.parent(item, ParentJoint)
                cmds.delete(TopBindGroup)
            #Parent Controllers
            if not ParentCC == "":
                cmds.parent(TopCCGroup, ParentCC)

            #Parent Extras
            if not ParentExtras == "":
                cmds.parent(TopExtrasGroup, ParentExtras)

            #Delete The rest of the Nodes
            if not ParentJoint == "" and not ParentCC == "" and not ParentExtras == "":
                cmds.delete(TopGrp)

        print "Ribbon Created Succesfully!"

def hideLocatorVisibility():
    #List all locators in scene
    locatorlist =cmds.ls(type = "locator")
    visibleLocators = []

    for obj in locatorlist:
        #Get locators visibility
        try:
            locVisbility = cmds.getAttr(obj + "Shape" + ".lodVisibility")
            if locVisbility == True:
                visibleLocators.append(obj)
        except:
            locVisbility = cmds.getAttr(obj + ".lodVisibility")
            if locVisbility == True:
                visibleLocators.append(obj)
        try:
            cmds.select(obj + "Shape")
            cmds.setAttr(obj + "Shape" + ".lodVisibility", 0)
        except:
            cmds.setAttr(obj + ".lodVisibility", 0)

    print(str(len(visibleLocators)) +' Locators hidden')
    visibleLocators[:] = []

def createFolicle(SurfaceToCreateOn, uValue, vValue, index, follicleNameBase = ""):
    #figure the name of the folicle

    follicleName = SurfaceToCreateOn.replace("surface", "follicle") + follicleNameBase + "Shape" +  str(index).zfill(2)

    #create the folicle
    newFolicleShape = cmds.createNode('follicle', n = follicleName)
    newFolicle = cmds.listRelatives(newFolicleShape, p = True)[0]
    cmds.rename(newFolicle, SurfaceToCreateOn.replace("surface", "follicle") + follicleNameBase + str(index).zfill(2))

    #connect the nessary attributes:
    cmds.connectAttr(SurfaceToCreateOn + "Shape.local", newFolicleShape + ".inputSurface")

    cmds.connectAttr(SurfaceToCreateOn + "Shape.worldMatrix[0]", newFolicleShape + ".inputWorldMatrix")
    cmds.connectAttr(newFolicle + ".outRotate", newFolicle + ".rotate" )
    cmds.connectAttr(newFolicle + ".outTranslate", newFolicle + ".translate")

    #set UV value:
    cmds.setAttr(newFolicle + ".parameterU", uValue)
    cmds.setAttr(newFolicle + ".parameterV", vValue)

    return newFolicleShape, newFolicle

def groupJntHierachy(BoneName, LocatorName, GrpName, ctrlJntName):

    locatorName = ctrlJntName.replace(BoneName, LocatorName)
    groupName = ctrlJntName.replace(BoneName, GrpName)

    cmds.spaceLocator(n = locatorName)
    cmds.setAttr(locatorName + ".localScaleX", 1)
    cmds.setAttr(locatorName + ".localScaleY", 1)
    cmds.setAttr(locatorName + ".localScaleZ", 1)
    cmds.setAttr(locatorName + "Shape.visibility", 0)

    cmds.select(locatorName, r = True)
    cmds.group(n = groupName)
    cmds.parent(ctrlJntName, locatorName)
    return groupName, locatorName

def createJntUnderObj(obj, BoneName, CCName, LocatorName, GrpName, TopBindGroup, TopFolliclesGroup, TopCCBindGroup, CCScale):
    #determine Name

    BindJointName = obj.replace("follicle", BoneName)
    ccName = obj.replace("follicle", CCName + "Extra")
    locName = obj.replace("follicle", LocatorName + "_" + CCName + "Extra")
    grpName = obj.replace("follicle", GrpName + "_" + CCName + "Extra")

    #Create
    cmds.joint(n = BindJointName)
    Controller = cmds.circle(n = ccName, r = CCScale)

    #Change Cntroller Shape
    cmds.select(Controller[0] + ".cv[0:7]")
    cmds.rotate(0, 90, 0)

    cmds.spaceLocator( n = locName)
    cmds.group(n = grpName)
    locatorShape = cmds.listRelatives(locName, s = True)[0]
    cmds.setAttr(locatorShape + ".visibility", 0)

    cmds.matchTransform(grpName, BindJointName, ccName, locName, obj)

    cmds.parent(ccName, locName)

    cmds.parent(grpName, TopCCBindGroup)
    cmds.parent(obj, TopFolliclesGroup)
    cmds.parent(BindJointName, TopBindGroup)

    #Create Constraints
    cmds.parentConstraint(ccName, BindJointName, mo = True)
    cmds.scaleConstraint(ccName, BindJointName, mo = True)
    cmds.parentConstraint(obj, grpName, mo = True)

    return BindJointName, locName, grpName

def CreateMasterController(CCColor,CCScale, bindJntList, AddFK, MasterCC, MasterLoc, Attach):
        #Define Color variables
        if CCColor == "Red":
            colorCode = 13
        if CCColor == "Pink":
            colorCode = 9
        if CCColor == "Green":
            colorCode = 14
        elif CCColor == "Blue":
            colorCode = 6
        elif CCColor == "Yellow":
            colorCode = 17
        elif CCColor == "LightBlue":
            colorCode = 18

        cmds.select(MasterCC + ".cv[:]")
        cmds.rotate(0, 0, 90)
        cmds.move(-1.5, 0, 0, r = True, os = True, wd = True)

        ControllerList = cmds.ls(MasterCC)
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

        cmds.parent(MasterCC, MasterLoc)
        tempConst = cmds.parentConstraint(bindJntList[0], MasterLoc)
        cmds.delete(tempConst)

        #Adjust Custom Attributes from Controller
        cmds.setAttr(MasterCC + ".sx", lock = True, keyable = False, ch = False)
        cmds.setAttr(MasterCC + ".sy", lock = True, keyable = False, ch = False)
        cmds.setAttr(MasterCC + ".sz", lock = True, keyable = False, ch = False)
        cmds.setAttr(MasterCC + ".v", lock = True, keyable = False, ch = False)

        #Add extra Attributes
        cmds.addAttr(MasterCC,longName='Visibility',niceName='---------------',at="enum",en='Visibility',k=True)
        cmds.addAttr(MasterCC,longName='IK_Controllers',at="bool",k=True, dv = 1)
        if AddFK == True:
            cmds.addAttr(MasterCC,longName='FK_Controllers',at="bool",k=True, dv = 1)

        cmds.addAttr(MasterCC,longName='Extra_Controllers',at="bool",k=True)
        cmds.addAttr(MasterCC,longName='NurbsSurface',at="bool",k=True )
        if Attach == True:
            cmds.addAttr(MasterCC,longName='Behaviour',niceName='---------------',at="enum",en='Follow',k=True)
            cmds.addAttr(MasterCC,longName='Follow',at="float",k=True, max = 1, min = 0, dv = 1)

def createController(allUIs, FKCC):
    import CreateControllers
    reload(CreateControllers)
    CreateControllers.createController(allUIs, FKCC)

def createDeformers(allUIs, ribbonNurbs, TopCCGroup, bindJntList, folicleList, TopExtrasGroup, MasterCC):
    import CreateDeformers
    reload(CreateDeformers)
    CreateDeformers.CreateDeformers(allUIs, ribbonNurbs, TopCCGroup, bindJntList, folicleList, TopExtrasGroup, MasterCC)

















