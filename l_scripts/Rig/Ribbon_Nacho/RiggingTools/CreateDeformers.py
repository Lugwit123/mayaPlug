import maya.cmds as cmds


def CreateDeformers(allUIs, ribbonNurbs, TopCCGroup, bindJntList, folicleList, TopExtrasGroup, MasterCC):
    #Create Main Deformers CC
    AsPrefix = cmds.checkBox(allUIs["prefixBtn"], q = True, v = True)
    CCName = cmds.textField(allUIs["CCNameField"], q = True, text = True)
    GrpName = cmds.textField(allUIs["GroupNameField"], q = True, text = True)
    Name = cmds.textField(allUIs["RibbonNameField"], q = True, text = True)
    BonesNumber = cmds.intSliderGrp(allUIs["BonesNumberSlider"], q = True, v = True)
    CCScale = float(cmds.textField(allUIs["CCScaleField"], q = True, text = True))
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
    Sine = cmds.checkBox(allUIs["SineDeformer"], q = True, v = True)
    Twist = cmds.checkBox(allUIs["TwistDeformer"], q = True, v = True)
    Volume = cmds.checkBox(allUIs["VolumeDeformer"], q = True, v = True)
    Roll = cmds.checkBox(allUIs["RollDeformer"], q = True, v = True)

    DeformerControllerName = ribbonNurbs[0].replace("surface", CCName + "_Deformers")
    if cmds.objExists(MasterCC) == True:
        control = MasterCC
    else:
        control = cmds.curve(n = DeformerControllerName, d=1, p=[(-1,0,-3),(1,0,-3),(1,0,-1),(3,0,-1),(3,0,1),(1,0,1),(1,0,3),(-1,0,3),(-1,0,1),(-3,0,1),(-3,0,-1),(-1,0,-1),(-1,0,-3)], k=[0,1,2,3,4,5,6,7,8,9,10,11,12])
        cmds.setAttr(control + ".sx", CCScale/3)
        cmds.setAttr(control + ".sy", CCScale/3)
        cmds.setAttr(control + ".sz", CCScale/3)
        cmds.makeIdentity(control, apply=True, t=True, r=True, s=True)
        defLocator = cmds.spaceLocator(n = "locAlign_" + control)
        cmds.parent(control, defLocator)
        cmds.parent(defLocator, TopCCGroup)

        #Change CC Shape
        cmds.select(control + ".cv[0:12]")
        cmds.move(0,5, 0, r = True, os = True, wd = True)
        cmds.rotate(90,0,0, r = True, os = True, fo = True, p = (0, 0, 0))

        #Lock and Hide Attr
        cmds.setAttr(control + ".tx", lock = True, keyable = False, ch = False)
        cmds.setAttr(control + ".ty", lock = True, keyable = False, ch = False)
        cmds.setAttr(control + ".tz", lock = True, keyable = False, ch = False)
        cmds.setAttr(control + ".rx", lock = True, keyable = False, ch = False)
        cmds.setAttr(control + ".ry", lock = True, keyable = False, ch = False)
        cmds.setAttr(control + ".rz", lock = True, keyable = False, ch = False)
        cmds.setAttr(control + ".sx", lock = True, keyable = False, ch = False)
        cmds.setAttr(control + ".sy", lock = True, keyable = False, ch = False)
        cmds.setAttr(control + ".sz", lock = True, keyable = False, ch = False)
        cmds.setAttr(control + ".v", lock = True, keyable = False, ch = False)

    #Create hierarchy groups
    grpSurfaces = cmds.group(empty=True, name=ribbonNurbs[0].replace("surface", GrpName + "_surfaces"))
    grpDeformers = cmds.group(empty=True, name=ribbonNurbs[0].replace("surface", GrpName + "_Deformers"))
    grpDeformersTop = cmds.group(empty=True, name=ribbonNurbs[0].replace("surface", GrpName + "_Deformers_Extras"))

    #Get Middle position to match deformers
    cmds.spaceLocator(n = "Temp_MiddleLoc")
    Const = cmds.parentConstraint(bindJntList[0],  bindJntList[-1], "Temp_MiddleLoc")
    cmds.delete(Const)
    aim = cmds.aimConstraint(bindJntList[-1], "Temp_MiddleLoc", aimVector = [0,1,0], upVector = [-1,0,0])
    cmds.delete(aim)

    deformerSurfaces = []

    if Twist == True:
        #Add extra Attributes
        cmds.addAttr(control,longName='twistSep',niceName='---------------',at="enum",en='Twist',k=True)
        cmds.addAttr(control,longName='TopTwist',at="float",k=True)
        cmds.addAttr(control,longName='EndTwist',at="float",k=True)
        cmds.addAttr(control,longName='twistOffset',at="float",k=True)
        cmds.addAttr(control,longName='twistPosition',at="float",k=True)
        cmds.addAttr(control,longName='affectToMid',at="float",min=0, max=20,dv=10,k=True)
        cmds.addAttr(control,longName='roll',at="float",k=True)
        cmds.addAttr(control,longName='rollOffset',at="float",k=True)
        cmds.addAttr(control,longName='twistAmplitude',at="float",k=True)
        cmds.addAttr(control,longName='TwistAxys',at="float",k=True)

        #Create the NURBS-planes to use in the setup
        geoPlaneTwist  = cmds.duplicate(ribbonNurbs[0], name=ribbonNurbs[0].replace("surface", "surface_Twist"))

        cmds.setAttr(geoPlaneTwist[0] + ".v", 1)

        #Create deformer
        twistDef  = nonlinearDeformer(objects=[geoPlaneTwist[0]],  defType='twist',  name= geoPlaneTwist[0].replace("surface", "Deformer"),  lowBound=-1, highBound=1)

        #List Shapes
        twistShape = cmds.listRelatives(twistDef, s = True)

        #Create Grp offset for deformer
        if AsPrefix == True:
            DeformerGrp = cmds.group(n = twistDef[0] + "_offset_grp", em = True)
        else:
            DeformerGrp = cmds.group(n = "grp_offset_" + twistDef[0], em = True)

        cmds.matchTransform(DeformerGrp, "Temp_MiddleLoc")
        cmds.matchTransform(twistDef, "Temp_MiddleLoc", pos = True, rot = True, scl = False)
        cmds.parent(twistDef[1], DeformerGrp)

        deformerSurfaces.append(geoPlaneTwist[0])

        #CONNECT DEFORMERS TO CC
        #Twist deformer: Sum the twist and the roll
        sumTopPma = cmds.shadingNode('plusMinusAverage', asUtility=1, name = ('twist_top_sum_pma' + Name))
        cmds.connectAttr((control + '.TopTwist'), (sumTopPma + '.input1D[0]'))
        cmds.connectAttr((control + '.twistOffset'), (sumTopPma + '.input1D[1]'))
        cmds.connectAttr((control + '.roll'), (sumTopPma + '.input1D[2]'))
        cmds.connectAttr((control + '.rollOffset'), (sumTopPma + '.input1D[3]'))

        sumEndPma = cmds.shadingNode('plusMinusAverage', asUtility=1, name = ('twist_low_sum_pma' + Name))
        cmds.connectAttr((control + '.EndTwist'), (sumEndPma + '.input1D[0]'))
        try:
            cmds.connectAttr((sumTopPma + '.output1D'), (twistDef[0] + '.startAngle'))
            cmds.connectAttr((sumEndPma + '.output1D'), (twistDef[0] + '.endAngle'))
        except:
            cmds.connectAttr((sumTopPma + '.output1D'), (twistShape[0] + '.startAngle'))
            cmds.connectAttr((sumEndPma + '.output1D'), (twistShape[0] + '.endAngle'))

        #Twist deformer: Set up the affect of the deformer
        topAffMdl = cmds.shadingNode('multDoubleLinear', asUtility=1, name = ('twist_top_affect_mdl' + Name))
        cmds.setAttr((topAffMdl + '.input1'), -0.1)
        cmds.connectAttr((control + '.affectToMid'), (topAffMdl + '.input2'))
        try:
            cmds.connectAttr((topAffMdl + '.output'), (twistDef[0] + '.lowBound'))
        except:
            cmds.connectAttr((topAffMdl + '.output'), (twistShape[0] + '.lowBound'))

        endAffMdl = cmds.shadingNode('multDoubleLinear', asUtility=1, name = ('twist_end_affect_mdl' + Name))
        cmds.setAttr((endAffMdl + '.input1'), 0.1)
        cmds.connectAttr((control + '.affectToMid'), (endAffMdl + '.input2'))
        try:
            cmds.connectAttr((endAffMdl + '.output'), (twistDef[0] + '.highBound'))
        except:
            cmds.connectAttr((endAffMdl + '.output'), (twistShape[0] + '.highBound'))
        #Twist deformer: Connect Amplitud to scale Y
        sumAmplitudePma = cmds.shadingNode('plusMinusAverage', asUtility=1, name = ('twist_amplitude_pma' + Name))
        cmds.connectAttr(control + ".twistAmplitude", sumAmplitudePma + '.input1D[0]')
        TwistScale = cmds.getAttr(twistDef[1] + ".sy")
        cmds.setAttr(sumAmplitudePma + '.input1D[1]', TwistScale)
        cmds.connectAttr(sumAmplitudePma + '.output1D', twistDef[1] + ".sy")

        cmds.connectAttr(control + ".TwistAxys", twistDef[1] + '.ry')
        cmds.connectAttr(control + ".twistPosition", twistDef[1] + '.translateY')

        #Clean hierarchy
        cmds.parent(geoPlaneTwist[0], grpSurfaces)
        cmds.parent(DeformerGrp,  grpDeformers)

    if Sine == True:
        #Add attributes: Sine attributes
        cmds.addAttr(control, longName='sineSep', niceName='---------------', attributeType='enum', en="Sine:", keyable=True)
        cmds.addAttr(control, longName='amplitude', attributeType="float", keyable=True)
        cmds.addAttr(control, longName='SineOffset', attributeType="float", keyable=True)
        cmds.addAttr(control, longName='SinePosition', attributeType="float", keyable=True)
        cmds.addAttr(control, longName='SineDropoff', attributeType="float", keyable=True, min=-1, max = 1, dv=1)
        cmds.addAttr(control, longName='SineTwist', attributeType="float", keyable=True)
        cmds.addAttr(control, longName='sineLength', min=0, dv=2, attributeType="float", keyable=True)
        cmds.addAttr(control, longName='sineScale', attributeType="float", keyable=True)

        #Create surfaces to use as deformers
        geoPlaneSine   = cmds.duplicate(ribbonNurbs[0], name=ribbonNurbs[0].replace("surface", "surface_Sine"))
        cmds.setAttr(geoPlaneSine[0] + ".v", 1)

        sineDef = nonlinearDeformer(objects=[geoPlaneSine[0]],   defType='sine',   name= geoPlaneSine[0].replace("surface", "Deformer"),   lowBound=-1, highBound=1)

        #List Shapes
        sineShape = cmds.listRelatives(sineDef, s = True)

        #Create Grp offset for deformer
        if AsPrefix == True:
            DeformerGrp = cmds.group(n = sineDef[0] + "_offset_grp", em = True)
        else:
            DeformerGrp = cmds.group(n = "grp_offset_" + sineDef[0], em = True)

        cmds.matchTransform(DeformerGrp, "Temp_MiddleLoc")
        cmds.matchTransform(sineDef, "Temp_MiddleLoc", pos = True, rot = True, scl = False)
        cmds.parent(sineDef[1], DeformerGrp)

        deformerSurfaces.append(geoPlaneSine[0])

        #Sine deformer: Connect Amplitud to scale Y
        sumSineScalePma = cmds.shadingNode('plusMinusAverage', asUtility=1, name = ('sine_scale_pma' + Name))
        cmds.connectAttr(control + ".sineScale", sumSineScalePma + '.input1D[0]')
        TwistScale = cmds.getAttr(sineDef[1] + ".sy")
        cmds.setAttr(sumSineScalePma + '.input1D[1]', TwistScale)
        cmds.connectAttr(sumSineScalePma + '.output1D', sineDef[1] + ".sy")

        #Sine deformer: Set up the connections for the sine
        try:
            cmds.connectAttr((control + '.amplitude'), (sineDef[0] + '.amplitude'))
            cmds.connectAttr((control + '.SineOffset'), (sineDef[0] + '.offset'))
            cmds.connectAttr((control + '.sineLength'), (sineDef[0] + '.wavelength'))
            cmds.connectAttr((control + '.SineDropoff'), (sineDef[0] + '.dropoff'))
        except:
            cmds.connectAttr((control + '.amplitude'), (sineShape[0] + '.amplitude'))
            cmds.connectAttr((control + '.SineOffset'), (sineShape[0] + '.offset'))
            cmds.connectAttr((control + '.sineLength'), (sineShape[0] + '.wavelength'))
            cmds.connectAttr((control + '.SineDropoff'), (sineShape[0] + '.dropoff'))

        cmds.connectAttr((control + '.SineTwist'), (sineDef[1] + '.rotateY'))
        cmds.connectAttr((control + '.SinePosition'), (sineDef[1] + '.translateY'))


        #Clean hierarchy
        cmds.parent(geoPlaneSine[0], grpSurfaces)
        cmds.parent(DeformerGrp,  grpDeformers)

    if Roll == True:
        #Add attributes: Sine attributes
        cmds.addAttr(control, longName='RollSep', niceName='---------------', attributeType='enum', en="Roll:", keyable=True)
        cmds.addAttr(control, longName='RollAmplitude', attributeType="float", keyable=True)
        cmds.addAttr(control, longName='RollPosition', attributeType="float", keyable=True)
        cmds.addAttr(control, longName='RollAngle', attributeType="float", keyable=True, min = -10, max = 10, dv = 0)
        cmds.addAttr(control, longName='RollScale', attributeType="float", keyable=True)
        cmds.addAttr(control, longName='RollHeight', attributeType="float", keyable=True)
        cmds.addAttr(control, longName='RollTwist', attributeType="float", keyable=True)
        cmds.addAttr(control, longName='RollStartDropoff', attributeType="float", keyable=True, min = -10, max = 0, dv = 0)
        cmds.addAttr(control, longName='RollEndDropoff', attributeType="float", keyable=True, min = 0, max = 10, dv = 10)

        #Create surfaces to use as deformers
        geoPlaneRoll = cmds.duplicate(ribbonNurbs[0], name=ribbonNurbs[0].replace("surface", "surface_Roll"))
        cmds.setAttr(geoPlaneRoll[0] + ".v", 1)

        RollDef = nonlinearDeformer(objects=[geoPlaneRoll[0]],   defType='bend',   name= geoPlaneRoll[0].replace("surface", "Deformer"),   lowBound=-1, highBound=10)

        #List Shapes
        rollShape = cmds.listRelatives(RollDef, s = True)

        #Create Grp offset for deformer
        if AsPrefix == True:
            DeformerGrp = cmds.group(n = RollDef[0] + "_offset_grp", em = True)
        else:
            DeformerGrp = cmds.group(n = "grp_offset_" + RollDef[0], em = True)

        cmds.matchTransform(DeformerGrp, "Temp_MiddleLoc")
        cmds.matchTransform(RollDef, "Temp_MiddleLoc", pos = True, rot = True, scl = False)
        cmds.parent(RollDef[1], DeformerGrp)

        deformerSurfaces.append(geoPlaneRoll[0])

        #Get Roll Scale Default Value
        VolumeScaleDV = cmds.getAttr(RollDef[1] + ".scaleX")

        #Set Height Value
        cmds.setAttr(control + '.RollHeight', VolumeScaleDV)

        #Connect Attr to Roll Deformer
        try:
            cmds.connectAttr((control + '.RollAmplitude'), (RollDef[0] + '.curvature'))
            cmds.connectAttr((control + '.RollStartDropoff'), (RollDef[0] + '.lowBound'))
            cmds.connectAttr((control + '.RollEndDropoff'), (RollDef[0] + '.highBound'))

        except:
            cmds.connectAttr((control + '.RollAmplitude'), (rollShape[0] + '.curvature'))
            cmds.connectAttr((control + '.RollStartDropoff'), (rollShape[0] + '.lowBound'))
            cmds.connectAttr((control + '.RollEndDropoff'), (rollShape[0] + '.highBound'))

        cmds.connectAttr((control + '.RollAngle'), (RollDef[1] + '.rotateZ'))
        cmds.connectAttr((control + '.RollTwist'), (RollDef[1] + '.rotateY'))
        cmds.connectAttr((control + '.RollScale'), (RollDef[1] + '.translateX'))
        cmds.connectAttr((control + '.RollHeight'), (RollDef[1] + '.scaleX'))
        cmds.connectAttr((control + '.RollPosition'), (RollDef[1] + '.translateY'))

        #Clean hierarchy
        cmds.parent(geoPlaneRoll[0], grpSurfaces)
        cmds.parent(DeformerGrp,  grpDeformers)

    if Volume == True:

        #Create Ribbon from Scratch: Nothing is selected
        if AsPrefix == True:
            geoPlaneVolume = cmds.nurbsPlane(u = BonesNumber,ax = (RibbonDirection[0], RibbonDirection[1], RibbonDirection[2]), n = Name + '_surface_Volume', lr = 1.0/BonesNumber, w = BonesNumber)
        else:
            geoPlaneVolume = cmds.nurbsPlane(u = BonesNumber,ax = (RibbonDirection[0], RibbonDirection[1], RibbonDirection[2]), n = 'surface_Volume_' + Name , lr = 1.0/BonesNumber, w = BonesNumber)
        
        squashDef = nonlinearDeformer(objects=[geoPlaneVolume[0]], defType='squash', name= geoPlaneVolume[0].replace("surface", "Deformer"), lowBound=-1, highBound=1)

        #List Shapes
        squashShape = cmds.listRelatives(squashDef, s = True)

        #Create Grp offset for deformer
        if AsPrefix == True:
            DeformerGrp = cmds.group(n = squashDef[0] + "_offset_grp", em = True)
        else:
            DeformerGrp = cmds.group(n = "grp_offset_" + squashDef[0], em = True)

        #Get Volume Scale Default Value
        VolumeScaleDV = cmds.getAttr(squashDef[1] + ".scaleX")

        #Add attributes: Volume attributes
        cmds.addAttr(control,longName='volumeSep',niceName='---------------',at="enum",en='Volume',k=True)
        cmds.addAttr(control,longName='volume',at="float",min=-2,max=2,k=True)
        cmds.addAttr(control,longName='volumeMultiplier',at="float",min=-1,dv=1,k=True)
        cmds.addAttr(control,longName='startDropoff',at="float",min=0, max=1, dv=1,k=True)
        cmds.addAttr(control,longName='endDropoff',at="float",min=0, max=1, dv=1, k=True)
        cmds.addAttr(control,longName='volumeScale',at="float", dv = VolumeScaleDV,k=True)
        cmds.addAttr(control,longName='volumePosition',at="float",k=True)

        #Volume
        VolumeFollicleGrp = cmds.group(em = True, w = True, n = "grp_Follicles_Volume_" + ribbonNurbs[0])
        VolumeFollicleList = []

        #Create follicles for the Volume surface
        for iter in range(1, BonesNumber + 1):
            folicleU = 1.0/(BonesNumber - 1.0) * (iter - 1)
            SurfaceToCreateOn = geoPlaneVolume[0]
            folicle = createFolicle(SurfaceToCreateOn, folicleU, 0, iter)
            newName = folicle[1].replace("surface_", "follicle_")
            cmds.rename(folicle[1], newName)
            cmds.parent(newName, VolumeFollicleGrp)
            VolumeFollicleList.append(folicle[1])

        #Get Middle position to match deformers
        cmds.spaceLocator(n = "Temp_MiddleVolumeLoc")
        Const = cmds.parentConstraint(VolumeFollicleList[0],  VolumeFollicleList[-1], "Temp_MiddleVolumeLoc")
        cmds.delete(Const)
        aim = cmds.aimConstraint(VolumeFollicleList[-1], "Temp_MiddleVolumeLoc", aimVector = [0,1,0], upVector = [-1,0,0])
        cmds.delete(aim)

        cmds.matchTransform(DeformerGrp, "Temp_MiddleVolumeLoc", pos = False, rot = True, scl = False)
        cmds.matchTransform(squashDef, "Temp_MiddleVolumeLoc", pos = False, rot = True, scl = False)
        cmds.parent(squashDef[1], DeformerGrp)

        #List follicles
        follicleList = []
        cmds.select(VolumeFollicleGrp)
        ChildrenList = cmds.listRelatives(VolumeFollicleGrp, c = True, typ = "transform")
        for item in ChildrenList:
            if item.startswith("follicle_"):
                follicleList.append(item)

        #Reposition Surface and squash deofrmer for the follicles to be 0

        MiddleFollicle =  len(VolumeFollicleList)/2
        cmds.group(n = "temp", em = True)
        cmds.group(n = "temp02", em = True)
        cmds.matchTransform("temp", VolumeFollicleList[MiddleFollicle])
        cmds.matchTransform("temp02", VolumeFollicleList[MiddleFollicle])
        cmds.parent("temp", "temp02")

        tempConst = cmds.parentConstraint("temp", geoPlaneVolume[0], mo = True)
        tempConst02 = cmds.parentConstraint("temp", squashDef[1], mo = True)

        cmds.setAttr("temp" + ".ty", 0.5)

        #Delete Temporary nodes
        cmds.delete(tempConst, tempConst02,"temp", "temp02")

        #Connect From the controller to deformer

        #Squash deformer: Set up the connections for the volume control
        volumeRevfMdl = cmds.shadingNode('multDoubleLinear', asUtility=1, name = ('volume_reverse_mdl' + Name))
        cmds.setAttr((volumeRevfMdl + '.input1'), -1)
        cmds.connectAttr((control + '.volume'), (volumeRevfMdl + '.input2'))
        try:
            cmds.connectAttr((volumeRevfMdl + '.output'), (squashDef[0] + '.factor'))
            cmds.connectAttr((control + '.startDropoff'), (squashDef[0] + '.startSmoothness'))
            cmds.connectAttr((control + '.endDropoff'), (squashDef[0] + '.endSmoothness'))

        except:
            cmds.connectAttr((volumeRevfMdl + '.output'), (squashShape[0] + '.factor'))
            cmds.connectAttr((control + '.startDropoff'), (squashShape[0] + '.startSmoothness'))
            cmds.connectAttr((control + '.endDropoff'), (squashShape[0] + '.endSmoothness'))

        cmds.connectAttr((control + '.volumePosition'), (squashDef[1] + '.translateY'))
        cmds.connectAttr((control + '.volumeScale'), (squashDef[1] + '.scaleY'))

        for follicle in follicleList:
            #Create Utility node for each node
            mult = cmds.shadingNode('multDoubleLinear', asUtility = 1, n = "mult_" + follicle + "_squashMult01")
            pma = cmds.shadingNode('plusMinusAverage', asUtility = 1, n = "pma_" + follicle + "_squashSum01")
            #Make the connections for the multiplier
            cmds.connectAttr(control + ".volumeMultiplier", (mult + '.input1'))
            if DirY == True:
                cmds.connectAttr(follicle + ".translateZ", (mult + '.input2'))
                #add 1 to the output of the multiplier
                cmds.setAttr((pma + ".input1D[0]"), 1)
                cmds.connectAttr((mult + ".output"), (pma + ".input1D[1]"))
                index = follicleList.index(follicle) + 1
            else:
                cmds.connectAttr(follicle + ".translateY", (mult + '.input2'))
                #Invert
                multRev = cmds.shadingNode('multiplyDivide', asUtility = 1, n = "multRev_" + follicle + "_squashMult01")
                cmds.setAttr(multRev + ".input2X", -1)
                cmds.connectAttr(mult + ".output", multRev + ".input1X")

                #add 1 to the output of the multiplier
                cmds.setAttr((pma + ".input1D[0]"), 1)
                cmds.connectAttr((multRev + ".outputX"), (pma + ".input1D[1]"))
                index = follicleList.index(follicle) + 1

            prefix = follicle.replace("follicle_Volume", GrpName + "_" + CCName + "Extra")

            cmds.connectAttr((pma + ".output1D"), (prefix + ".scaleY"))
            cmds.connectAttr((pma + ".output1D"), (prefix + ".scaleZ"))

        #Clean hierarchy
        cmds.parent(geoPlaneVolume[0], grpSurfaces)
        cmds.parent(DeformerGrp,  grpDeformers)
        cmds.parent(VolumeFollicleGrp, grpDeformersTop)
        cmds.setAttr(VolumeFollicleGrp + ".v", 0)

    #BlendShaples function
    cmds.select(cl = True)
    for item in deformerSurfaces:
        cmds.select(item, add = True)

    selection = cmds.ls(sl = True)

    blndDef = cmds.blendShape(selection, ribbonNurbs[0], name=("bs_deformers_" + Name),weight=[(0,1),(1,1),(2,1),(3,1)])

    #Clean Hierarchy
    cmds.parent(grpSurfaces, grpDeformers, grpDeformersTop)
    cmds.parent(grpDeformersTop, TopExtrasGroup)
    cmds.setAttr(grpSurfaces + ".v", 0)
    cmds.setAttr(grpDeformers + ".v", 0)
    cmds.setAttr(grpDeformersTop + ".v", 0)
    cmds.delete("Temp_MiddleLoc")
    if Volume == True:
        cmds.delete("Temp_MiddleVolumeLoc")

def nonlinearDeformer(objects=[], defType=None, lowBound=-1, highBound=1, translate=None, rotate=None, name='nonLinear'):
    #If something went wrong or the type is not valid, raise exception
    if not objects or defType not in ['bend','flare','sine','squash','twist','wave']:
        raise Exception, "function: 'nonlinearDeformer' - Make sure you specified a mesh and a valid deformer"
    #Create and rename the deformer
    nonLinDef = cmds.nonLinear(objects[0], type=defType, lowBound=lowBound, highBound=highBound)
    nonLinDef[0] = cmds.rename(nonLinDef[0], (name + '_' + defType + '_def'))
    nonLinDef[1] = cmds.rename(nonLinDef[1], (name + '_' + defType + 'Handle'))
    #If translate was specified, set the translate
    if translate:
        cmds.setAttr((nonLinDef[1] + '.translate'), translate[0], translate[1], translate[2])
    #If rotate was specified, set the rotate
    if rotate:
        cmds.setAttr((nonLinDef[1] + '.rotate'), rotate[0], rotate[1], rotate[2])
    #Return the deformer
    return nonLinDef

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


