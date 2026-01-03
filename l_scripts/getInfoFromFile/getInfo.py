# -*- coding: utf-8
import sys,os
from token import LPAR
sys.path.append(os.environ.get('LugwitToolDir')+'/Lib')
import Lugwit_Module as LM
lprint=LM.lprint


from itertools import islice
import re,time,codecs

def getExFrameRangeFromFrameRange(cameraList):
    if not cameraList:
        return None
    for cameraTrNode in cameraList:
        if len(cameraTrNode)>7:
            break
    cameraTrNode_split=cameraTrNode.split('_')
    if len(cameraTrNode_split)>2:
        sf = cameraTrNode.split('_')[-2]
        ef = cameraTrNode.split('_')[-1]
        try:
            return int(float(sf)),int(float(ef))
        except:
            return None

def get_maya_arnold_redshiftVersion(mayaFile):
    MayaVersion,arnoldVersion,redshiftVersion='2018','402','3.5.09'
    if os.path.exists(mayaFile):
        with codecs.open(mayaFile,'rb') as f:
            f_read=f.read(5000)
            f_read =str(f_read)
            arnoldVersion_match=re.search('"mtoa" "(\d+.\d+.\d+)',f_read,re.M|re.S)
            arnoldVersion = arnoldVersion_match.group(1) if arnoldVersion_match else arnoldVersion
            
            redshiftVersion_match=re.search('"redshift4maya" "(\d+.\d+.\d+)',f_read,re.M|re.S)#"redshift4maya" "3.5.09";
            redshiftVersion = redshiftVersion_match.group(1) if redshiftVersion_match else redshiftVersion
            
            MayaVersion_match=re.search('requires maya "(\d+)',f_read,re.M|re.S)
            MayaVersion = MayaVersion_match.group(1) if MayaVersion_match else MayaVersion

    return MayaVersion,arnoldVersion,redshiftVersion

def getExEleFromReadMa(mayaFile,cam_RefFileNameSpace='',cameraNameRule=['',''],
                    frameRangeRule=['','']):
    # cameraNameRule='content:ex:ep\d.+'
    # frameRangeRule=['ex:cameraTrNode:(\d+)_\d+$','ex:cameraTrNode:\d+_(\d+)$']
    print (u'从{}中获取导出元素'.format(mayaFile))
    lprint(locals(),force_print=True)
    cameraTrNode=''
    camereShapeNode=''
    if 'C_N_HanJiaPuCongA' in mayaFile:
        mayaFile=mayaFile.replace('.ma','_New.ma')
        
    nsList,cameraList,camRefFile  = [],[],''
    i=0
    st=time.time()
    findRef=False
    load_nameSpace_refFileList=[];nameSpaceList=[];defaultResolutionList=[];playRange=[]
    curRender=''
    renderLayerList=[]
    exFrameRange=[]
    arnoldRenderFmt=''
    index=0
    frame_rate=''
    frame_rate_mapping = {
        'game': 15,
        'film': 24,
        'pal': 25,
        'ntsc': 30,
        'show': 48,
        'palf': 50,
        'ntscf': 60
    }
    RefFileList=[]
    with open(mayaFile, 'r',errors='ignore') as f:
        while 1:
            # 使用readlines()读取前面几行获取名称空间,文件是否加载,引用文件等信息
            index+=1
            try:
                lines_gen = list(islice(f, 50000))
                lprint (f"查询了{len(lines_gen)}行")
            except:
                lprint (u'查询到第{}行出现错误'.format(index*50000))
                continue
            if not lines_gen:
                lprint (u'查询到最后一行,行好为{}*{}'.format(index,50000))
                break
            if not findRef:
                #lines_genList='\n'.join(lines_gen).split('\n')
                lines_genList=lines_gen
                while '' in lines_genList:
                    lines_genList.remove('')
                lprint ('lines_genList->',lines_genList[:10])
                nameSpaceIndex=0
                
                for lineIndex,line in enumerate(lines_genList):
                    findRef=True
                    if not frame_rate:
                        if 'currentUnit' in line and '-t' in line:
                            # 从字符串中提取帧速率值
                            tokens = line.split()
                            for i, token in enumerate(tokens):
                                if token in ['-t','-time']:
                                    frame_rate_str = tokens[i + 1].strip(';')
                                    # 检查帧速率是否是关键字
                                    if frame_rate_str in frame_rate_mapping:
                                        frame_rate = frame_rate_mapping[frame_rate_str]
                                    else:
                                        # 尝试将帧速率转换为整数
                                        try:
                                            frame_rate = int(frame_rate_str)
                                        except ValueError:
                                            pass

                    if line.startswith('file -rdi'):
                        # fileRefTwoLines=re.search('file -rdi.+/r/nfile')
                        fileRefTwoLines=''.join(lines_genList[lineIndex:lineIndex+3])
                        # fileRefTwoLines=fileRefTwoLines.replace('\n',' ')
                        lprint ('fileRefTwoLines->',fileRefTwoLines)
                        refFile_group=re.search('-rdi.+?-typ\s+"[a-z?]+"\s+"(.+?)";\r*\nfile\s-r', 
                                          fileRefTwoLines,flags=re.I|re.M|re.DOTALL)
                        if refFile_group:
                            refFile=refFile_group.group(1)  
                            lprint (refFile_group.group()  )
                        else:
                            continue

                        #比如cam_RefFileNameSpace为camrigcam_Re[0-9]*$,这个时候要去除$,不然匹配不上
                        if cam_RefFileNameSpace:
                            if re.search(' "{}" '.format(cam_RefFileNameSpace.replace('$','')),refFile_group.group()):
                                camRefFile=refFile
                        try:
                            nameSpace=re.findall('file -rdi . (?:-ns|-rpr) "(.+?)"', fileRefTwoLines)[0]
                        except:
                            print(line)
                            # sys.exit()
                        try:
                            refNode = re.findall('-rfn "(.+?)"', fileRefTwoLines)[0]
                        except:
                            print(line)
                            # sys.exit()
                        
                        
                        if refFile in RefFileList:
                            num=re.search('\d+$',nameSpace)
                            if num:
                                refFile=refFile+'{'+num.group()+'}'

                        if not os.path.exists(refFile):
                            g_disk_refFile=refFile.replace('H:','G:')
                            if os.path.exists(g_disk_refFile):
                                refFile=refFile.replace('H:','G:')
                        RefFileList.append(refFile)
                        if nameSpace in nameSpaceList:
                            continue
                        
                        load_nameSpace_refFileList.append([])
                        
                        load_nameSpace_refFileList[nameSpaceIndex]=\
                                                    {"dr":'-dr' in line,
                                                    "nameSpace":nameSpace,
                                                    "refNode":refNode,
                                                    "refFile":refFile }   

                        nameSpaceIndex+=1
                        nameSpaceList.append(nameSpace)
                        
                    if line.startswith('select -ne :defaultResolution;'):
                        matchStr='select -ne :defaultResolution;\n\tsetAttr ".w" ([0-9]+);\n\tsetAttr ".h" ([0-9]+)'
                        FindRes=''.join(lines_genList[lineIndex:lineIndex+3])
                        lprint (repr(FindRes))
                        setResolution=re.search(matchStr,FindRes,flags=re.I|re.M)
                        lprint (setResolution)
                        if setResolution:
                            find=re.search(matchStr,FindRes,flags=re.I|re.M)
                            if find:
                                defaultResolutionList=[find.group(1),find.group(2)]

            if not lines_gen:
                lprint ('查询到最后一行')
                break
            
            read_f=' '.join(lines_gen)
            
            # 查找渲染层列表
            renderLayerList+=re.findall('createNode renderLayer -n "(\w+)";',read_f)

            #createNode camera -n "B024_SM01_A_shot03_1001_Shape1050" -p "B024_SM01_B_shot01_1001_1050";
            # RESOLVED: 换行符导致匹配失败,摄像机明层可能会跨行,因此使用"\s"替换" "空格,\s能匹配任意空白字符,包括换行符
            cameraList+=re.findall(r'createNode camera -n(?:ame)* "(.+?)"\s*-p(?:arent)* "(.+?)";', read_f)
            lprint(cameraList)
            # cameraList+=re.findall(r'-camera \\"(.+?)\\"',read_f)
            if not curRender:
                curRender=re.search('setAttr -av -cb on ".ren" -type "string" "(.+)";',read_f)
                if curRender:
                    curRender=curRender.group(1)
            #nsList += re.findall('file -r -ns "(.+?)" ', read_f
            #setAttr ".b" -type "string" "playbackOptions -min 1001 -max 1094 -ast 1001 -aet 1258.23 ";
            
            if not arnoldRenderFmt:
                Fmt=re.search('createNode aiAOVDriver -s -n "defaultArnoldDriver";.+?setAttr ".ai_translator" -type "string" "([a-z]+)";',
                            read_f,flags=re.I|re.S|re.M)
                if Fmt:
                    lprint ('Fmt->',Fmt.group(),repr(Fmt.group()))
                    arnoldRenderFmt=Fmt.group(1)
                
            i+=1
            if not playRange:
                playRange=re.findall('playbackOptions -min (-?\d+[\.\d+]*) -max (-?\d+[\.\d+]*) -ast (-?\d+[\.\d+]*) -aet (-?\d+[\.\d+]*)',read_f)
                if playRange:
                    playRange=playRange[0]
                    lprint ('playRange->',playRange)
                
                
            if not defaultResolutionList:
                defaultResolution=re.search('setAttr -av -k on ".w"\s*(\d*);',read_f,flags=re.S|re.M)
                
                if defaultResolution:
                    lprint ('defaultResolution->',defaultResolution.group())
                    try:
                        if defaultResolution.group(1):
                            defaultResolutionList.append(defaultResolution.group(1))
                            lprint (u'没有设置分辨率,使用分辨率默认值960_{}_'.format(defaultResolution.group(1)))
                        else:
                            defaultResolutionList.append('960')
                    except:
                        defaultResolutionList.append('960')
                    try:
                        resY=re.search('setAttr -av -k on ".h" (\d+);',read_f,flags=re.S|re.M).group(1)
                    except:
                        resY='540'
                    defaultResolutionList.append(resY)
                    lprint ('从Maya文件中获取导出文件信息直到{}行结束'.format(i*500))
                    break
                    
                
    
    if not defaultResolutionList:
        defaultResolutionList=['960','540']

    lprint (cameraList)
    nonExList=['front','frontShape' 'persp', 'side', 'top','back','bottom','right',
                'top','left','perspShape', 'sideShape', 'topShape','backShape',
                'bottomShape','rightShape','topShape','leftShape','bottom1Shape','perspShape1','perspShape2']

    cameraList = list(filter (lambda x : x[0] not in nonExList ,cameraList  ))
    # cameraList=new_cameraList

    playRange=[x.split('.')[0] for x in playRange]
    lprint (playRange,cameraList)
    
    if cameraList:
        for i,(camereShapeNode,cameraTrNode) in enumerate(cameraList):
            cameraList[i]=[camereShapeNode.split('|')[-1],cameraTrNode.split('|')[-1]]


    maya_arnold_redshiftVersion=get_maya_arnold_redshiftVersion(mayaFile)
    # lprint (cameraNameRule,'content:ex:' in cameraNameRule[0])
    lprint (cameraList,cameraNameRule)
    if 'content:ex:' in cameraNameRule[1]:
        for i,(camereShapeNode,cameraTrNode) in enumerate(cameraList):
            if cameraTrNode in nonExList:
                continue
            regExp=cameraNameRule[1].replace('content:ex:','')
            findCamera=re.search(regExp,cameraTrNode)
            lprint (regExp,cameraTrNode)
            if findCamera:
                cameraTrNode=cameraTrNode
                camereShapeNode=camereShapeNode
                lprint (cameraTrNode,camereShapeNode)
                break
    
    lprint (frameRangeRule)
    if all(frameRangeRule):
        exFrameRange=[]
        for item in frameRangeRule:
            regExp=item.replace('content:ex:cameraTrNode:','')
            lprint (regExp)
            findFrameRange=re.search(regExp,cameraTrNode)
            if findFrameRange:
                exFrameRange.append(int(findFrameRange.group(1)))
            else:
                exFrameRange=[int(playRange[2]),int(playRange[3])]

        
    
    return {'cameraList':cameraList,
            'nameSpaceList':load_nameSpace_refFileList,
            'exCamera':(cameraTrNode,camereShapeNode),
            'playRange':playRange,
            'exFrameRange':exFrameRange,
            'defaultResolution':defaultResolutionList,
            'arnoldRenderFmt':arnoldRenderFmt,
            'renderLayerList':renderLayerList,
            'mayaVersion':maya_arnold_redshiftVersion[0],
            'arnoldVersion':maya_arnold_redshiftVersion[1],
            'redshiftVersion':maya_arnold_redshiftVersion[2],
            'curRender':curRender,
            'frame_rate':frame_rate,
            'camRefFile':camRefFile}
    
    
def getXgenInfoFromMayaFile(mayaFile=''):
    pass


if __name__=='__main__':
    mayaFile=r'Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP106\Animation\scenes&movies\CW_EP106_SC076_Fin.ma'
    mayaFile=r'Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP124\Animation\scenes&movies\CW_EP124_SC157_an.ma'
    mayaFile=r'Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP126\Animation\scenes&movies\CW_EP126_SC175_an.ma'
    mayaFile=r'Z:\Cosmos_Wartale2\03_Main-Production\05_animation\EP107\Animation\scenes&movies\CW_EP107_SC003_an.ma'
    mayaFile=r"Z:\Cosmos_Wartale\03_Main-Production\05_animation\EP107\Animation\scenes&movies\CW_EP107_SC003_an_A.ma"
    mayaFile=r"H:/JZXCL/5.Anima final/anim/ep022/ma/ep022_sc001_shot0170_anim.ma"
    mayaFile=r"G:\BLDTD\Shot\PV02\sc01\shot025\Animation\Version\PV02_sc01_shot025_ani_V019.ma"
    # mayaFile='X:/OP_WX/pro-production/Shot/Animation/sc01_cut0010/publish/OP_WX_CG_sc01_cut0010_ani.ma'
    # mayaFile=r'D:\bb\XD_CG_CG_C13_ly_v014.ma'
    lprint (getExEleFromReadMa(mayaFile,None))
    # sys.exit(0)
    
