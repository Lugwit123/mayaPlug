# coding:utf-8
from __future__ import print_function
#添加模块所在路径
import os,re,sys,time,sys,os
import traceback
import inspect,os
__file__=inspect.getfile(inspect.currentframe())
fileDir=os.path.dirname(__file__)
print ('run module{}'.format(__file__))
import sys,os,time
from imp import  reload
import zipfile

import codecs 
from PySide2.QtWidgets import *
from PySide2 import QtCore
from PySide2.QtGui import QMovie
from PySide2.QtCore import *
from functools import partial

try:
    import maya.mel as mm
    import maya.cmds as cmds
except:
    pass
import re
import PySide2.QtCore as QtCore
from pprint import pprint
imageFormatList=['jpg','jpeg','png','tif','tiff','tga','bmp','exr','psd','hdr','pic','tga','tx','iff']


import threading

debug=1
def Print(*args):
    if debug:
        print (args)

def find_LUGWIT_PLUG_Path(curPath):
    import re
    curPath=curPath.replace('\\','/')
    curPath= re.findall('.+/Lugwit_plug',curPath)
    if curPath:
        return curPath[0]
    
def getAllChildPath(path,fileType=''):
    import os
    print ('path',path)
    specifyTypePathList=[];allTypePathList=[]
    if isinstance(path,str):
        pathList=[path]
    else:
        pathList=path
    for path in pathList:
        for root, dirs, files in os.walk(path):
            for file in files:
                genAbsPath=os.path.join(root, file).replace('/','\\')
                if os.path.splitext(file)[1] in  fileType:
                    specifyTypePathList.append(genAbsPath)
                allTypePathList.append(genAbsPath)
    return specifyTypePathList,allTypePathList

def readXgenFile(xgenFile=r'D:\aa\bb__collection3.xgen'):
    with codecs.open (xgenFile,'r',encoding='utf8') as f:
        f_read=f.read()
        xgDataPath=re.search('xgDataPath\s+(.+)\r*\n',f_read).group(1)
        xgProjectPath=re.search('xgProjectPath\s+(.+)\r*\n',f_read).group(1)
        if xgDataPath.startswith('${PROJECT}'):
            xgDataPath=xgProjectPath+xgDataPath.replace('${PROJECT}','')
        print ('xgDataPath-->',xgDataPath,end='=========')
        return xgDataPath
    
def getMayaFileContents(mayaFile=''):
    try:
        with open(mayaFile, 'r') as f:
            return f.read()
    except:
        print (u'整体打开Maya文件失败：{}'.format(mayaFile))
        
    try:
        mayaFileContents=''
        openMayaFile=codecs.open(mayaFile,'r',encoding='gbk')
        while 1:
            readPart=openMayaFile.read(50000)
            if not readPart:
                openMayaFile.close()
                break
            mayaFileContents += readPart
    except Exception as e:
        print ('e',e)
        try:
            openMayaFile.close()
        except:
            pass
    return mayaFileContents

#获取xgen文件的路径和xgen文件夹的路径
def getXgenInfoFromMayaFile(mayaFile='',mayaContent=''):
    mayaFileName=os.path.basename(mayaFile)
    mayaFileBaseName=os.path.splitext(mayaFileName)[0]
    mayaFileDir=os.path.dirname(mayaFile)
    xgenFileList=[]
    xgDataPathList=[]
    if mayaContent:
        print ('-----')
        xgenFileList=re.findall('setAttr ".xfn" -type "string" "(.+)";',mayaContent,flags=re.I)
    else:
        if os.path.exists(mayaFileDir):
            for file in os.listdir(mayaFileDir):
                if file.startswith(mayaFileBaseName+'__'):
                    if file.endswith('.xgen'):
                        xgenFileList.append(file)

    for i,xgenFile in enumerate(xgenFileList):
        fullPath=os.path.join(mayaFileDir,xgenFile).replace('\\','/')
        xgDataPathList.append(readXgenFile(fullPath))
        xgenFileList[i]=fullPath

    xgDataPathList=list(set(xgDataPathList))
    return xgenFileList,xgDataPathList


def chooseFile(par='',FieldPathWidget='',chooseFunc='getOpenFileName',DialogCommit=u"DialogCommit",stDir=r"d:/",fileType="(*.abc)"):
    
    if os.path.exists(FieldPathWidget.currentText() ):
        stDir=FieldPathWidget.currentText() 
    func=eval('QFileDialog.{}'.format(chooseFunc))
    if 'File' in chooseFunc:
        path= func(par,repr(DialogCommit,),repr(stDir),repr(fileType))[0]
    else:
        path=func(par,repr(DialogCommit),repr(stDir))
        
    path=path.replace('/','\\')    
    if path:
        FieldPathWidget.insertItems(0,[path])
        FieldPathWidget.setCurrentText(path)
    return path.replace('/','\\')

def Lbutton(label,  c):
    button = QPushButton(label)
    button.clicked.connect(c)
    return button

class LPathSel(QWidget):
    def __init__(self,par='',l_lab='label',buttonName='button',DialogCommit='choose',stDir='D:/',fileType='*.ext',chooseFunc='getOpenFileName',defaultPath=''):
        super(LPathSel, self).__init__()
        lav=QHBoxLayout()
        self.labelList=[]
        self.FieldPathWidget= QComboBox()
        self.FieldPathWidget.setEditable(True)
        self.FieldPathWidget.lineEdit().setReadOnly(True)
        Print ('self.FieldPathWidget',self.FieldPathWidget)
        if defaultPath:
            if isinstance(defaultPath,str):
                self.FieldPathWidget.insertItem(0,defaultPath)
            if isinstance(defaultPath,list):
                self.FieldPathWidget.insertItems(0,defaultPath)
        else:
            self.FieldPathWidget.addItems([stDir])
            
        if 'File' in chooseFunc:
            selFilebutton = Lbutton(
            buttonName,  c=partial(chooseFile,self,self.FieldPathWidget,chooseFunc,DialogCommit,stDir,fileType))
        else:
            selFilebutton = Lbutton(
            buttonName,  c=partial(chooseFile,self,self.FieldPathWidget,chooseFunc,DialogCommit,stDir)) 
            
        self.widgetLabel=l_lab
        lav.setContentsMargins(0, 0,0,0)
        if isinstance(l_lab,str):
            self.widgetLabel=QLabel(l_lab)
        elif self.widgetLabel[0]==QCheckBox:
            self.checkWidget=QCheckBox()  #创建QCheckBox
            lab=QLabel()                              #创建标签
            lab.setText(self.widgetLabel[1])
            self.labelList.append(lab)
            # lab.setContentsMargins(0, 0,0,0)
            self.checkWidget.setChecked(self.widgetLabel[2])
            self.checkWidget.stateChanged.connect(lambda:self.FieldPathWidget.setEnabled(self.checkWidget.isChecked()))
            self.checkWidget.stateChanged.connect(lambda:selFilebutton.setEnabled(self.checkWidget.isChecked()))
            self.checkWidget.stateChanged.connect(lambda:lab.setEnabled(self.checkWidget.isChecked()))
            lav.addWidget(self.checkWidget)
            lav.addWidget(lab)
        
        lav.addWidget(self.FieldPathWidget,3)  
        lav.addWidget(selFilebutton,1) 
        self.setLayout(lav)
        if par!='':
            par.addWidget(self)
            
    def setText(self,text):
        if isinstance(text,str):
            self.FieldPathWidget.setCurrentText(text)
        elif isinstance(text,list):
            self.FieldPathWidget.insertItems(0,text)
            self.FieldPathWidget.setCurrentText(text[0])
            
    def text(self):
        return self.FieldPathWidget.currentText() 
    
    def get_labList(self):
        return self.labelList
    
def getFileList(fileType,mayaFile):
    if mayaFile[0].islower():
        mayaFile=mayaFile[0].upper()+mayaFile[1:]

    fileList=[];unsolveFileList=[]

    unsolveFile=[]
    st=time.time()
    #刷新文件路径
    #mm.eval('filePathEditor -refresh;')

    refreshPathTime=time.time()
    #win.close()
    #列出所有目录
    list_dir = cmds.filePathEditor(
        query=True, listDirectories="", unresolved=True)
    list_files = [] #声明一个列表接受要打包的文件
    hasOneUdim=0   #默认设定贴图不是udim贴图
    
    xgenFileList=[]
    mayaFileDir=os.path.dirname(mayaFile)
    mayaFileBaseName=os.path.basename(mayaFile).rsplit('.',1)[0]
    
    AlembicNodes=cmds.ls(type='AlembicNode')
    AlembicNodes+=cmds.ls(type='xgmSplineCache')
    AlembicNode_abcFileList=[]
    for AlembicNode in AlembicNodes:
        #print cmds.listAttr(AlembicNode )
        try:
            abcFile=cmds.getAttr(AlembicNode+'.abc_File')
        except:
            abcFile=cmds.getAttr(AlembicNode+'.fileName')
        AlembicNode_abcFileList.append(abcFile)
        
    for i0,directory in enumerate(list_dir):
        #list_file_elem 列出所有文件的名称和属性名称
        #[u'sc001.ma', u'sc001RN']
        #[u'bb.jpg', u'file1.fileTextureName', u'aa.jpg', u'sc001:file1.fileTextureName']
        #list_file_elem  如果是贴图,返回贴图名称和隶属的属性
        #list_file_elem  如果是引用文件,返回引用文件名称和隶属的节点名称
        list_file_elem = cmds.filePathEditor(
            query=True, listFiles=directory, withAttribute=True)
        directory=directory.replace('\\','/')
        _list_file_elem=list_file_elem[::2]
        if i0==0:
            _list_file_elem+=AlembicNode_abcFileList
        for rel_path in _list_file_elem:#list_file_elem[::2]表示只取文件路径
            #决定是否打包Maya文件
            if re.search('.ma$|.mb$|.abc$|.fbx$|.obj$',rel_path,flags=re.I):
                if not fileType[0] :
                    continue
            #决定是否打包贴图文件
            elif re.search('jpg$|jpeg$|tiff$|png$|tif$|tga$|bmp$|exr$|psd$|hdr$|pic$|tga$|tx$|iff$',rel_path,flags=re.I):
                if not fileType[1] :
                    continue
            # 决定是否打包xgen文件
            elif re.search('/xgen/',directory,re.I) or re.search('.xgen$',rel_path,flags=re.I):
                if not fileType[2] :
                    continue
            #决定是否打包ptx文件
            
            elif re.search('/3dPaintTextures',directory,flags=re.I):
                if not fileType[3] :
                    continue
            
            list_files+=xgenFileList 

            
            #获取绝对路径 
            if ':' not in rel_path:
                absPath= directory+'/'+rel_path
            else:
                absPath=rel_path
            if absPath[0].islower():
                absPath=absPath[0].upper()+absPath[1:]
            absPath=absPath.replace('\\','/')
            print ('absPath-->>',absPath)
            if absPath in list_files:
                #print (u'已查找此文件{}'.format(absPath))
                continue
            
            #添加xgen文件夹下的所有文件
            if absPath.endswith('.ma'):
                xgenFileList,xgDataPathList=getXgenInfoFromMayaFile(absPath)
                list_files+=xgenFileList
                list_files+=getAllChildPath(xgDataPathList)[1]
                if os.path.exists(absPath):
                    list_files.append(absPath)
                else:
                    unsolveFile.append(absPath)
                continue

            
            #检测UDIM贴图
            rearchUdim=re.search('[._]+([1-2]\d\d\d)[._]+',absPath)
            #print ('absPath>>>>>>',repr(absPath))
            notXgenFile=not absPath.endswith('.xgen')
            isUdim='<UDIM>' in absPath or rearchUdim
            if isUdim and  notXgenFile:
                # if rearchUdim:
                #     getGroup1=rearchUdim.group(1)
                #     print (u'贴图不是1001并且{}存在'.format(absPath.replace(getGroup1,'1001')))
                #     print (getGroup1[-1]>1 and os.path.exists(absPath.replace(getGroup1,'1001')))
                #     if int(getGroup1[-1])>1 and os.path.exists(absPath.replace(getGroup1,'1001')):
                #         break
                for i in range(1,20):
                    # 设置udim名称
                    
                    if '<UDIM>' in absPath:
                        udim_expandPtath=absPath.replace('<UDIM>','10'+str(i).zfill(2))
                    elif rearchUdim: 
                        getGroup1=rearchUdim.group(1)
                        udim_expandPtath=absPath.replace(getGroup1,'10'+str(i).zfill(2))
                    
                    if os.path.exists(udim_expandPtath):
                        #print (u'添加Udmi贴图到列表{}'.format(udim_expandPtath))
                        list_files.append(udim_expandPtath)
                        hasOneUdim=1
                    #如果不存在加入unsolveFile列表
                    elif hasOneUdim==0:
                        unsolveFile.append(udim_expandPtath)

                for j in range(1,20):
                    if '<UDIM>' in absPath:
                        udim_expandPtath=absPath.replace('<UDIM>','20'+str(j).zfill(2))
                    elif rearchUdim:
                        udim_expandPtath=absPath.replace(rearchUdim.group(1),'20'+str(j).zfill(2))
                    if os.path.exists(udim_expandPtath):
                        #Print udim_expandPtath
                        list_files.append(udim_expandPtath)
                        hasOneUdim=1
                    elif hasOneUdim==0:
                        unsolveFile.append(udim_expandPtath)
            #检测非UDIM贴图
            else:
                if os.path.exists(absPath):
                    list_files.append(absPath)
                else:
                    unsolveFile.append(absPath)
    print (u'找到的文件--\n{}\n'.format(list_files))    
    print (u'未找到文件--\n{}\n'.format(unsolveFile))               
    # 获取maya工程文件中用到的的所有文件
    print (u'搜集文件完毕')
    list_files.append(mayaFile)
    list_files=list(set(list_files))
    list_files=sorted(list_files)
    # 1 根据盘符分拆所有文件
    # 1.1 获取磁盘盘符列表
    
    disListA=[x[0] for x in list_files if x and x[1]==':']
    disListB=[re.search('(//.+?/.+?)/',x).group(1).replace('/','_') for x in list_files if x.replace('\\','/').startswith('//')]
    disList= (list(set(disListA+disListB)))
    pprint (('diskListA:',disList))

    disList=sorted(disList)
    # 1.2 建立磁盘盘符列表列表变量
    name=locals()
    for diskName in disList:
        name['disk_'+diskName]=list()
    if u'' in list_files:
        list_files.remove(u'')
    # 1.2 在磁盘盘符列表列表变量中添加变量
    for file in list_files:
        print ('file',file)
        findLocalNetFile=re.search('(//.+?/.+?)/',file)
        if findLocalNetFile:
            findLocalNetFile=findLocalNetFile.group(1).replace('/','_')
            diskName=findLocalNetFile
        else:
            diskName=file[0]
            
        name['disk_'+diskName].append(file)
        #如果是普通图片格式,连着tx文件一起打包
        ext=os.path.splitext(file)[1]
        if  re.search(ext[1:],str(imageFormatList),flags=re.I):
            txFormat=re.sub(ext,'.tx',file,flags=re.I)
            if os.path.exists(txFormat):
                name['disk_'+diskName].append(txFormat)
            print ('txFormat',txFormat)
        elif file.endswith('tx'):
            for format in imageFormatList:
                conImage=file.replace('.tx','.'+format)
                if os.path.exists(conImage):
                    name['disk_'+diskName].append(conImage)
                    break
                

    #获取压缩列表耗时
    collectFileTime=time.time()
    
    #Print (U'list_files{}'.format(list_files))
    #return 列表
    findFileList=[name['disk_'+diskName] for diskName in disList]
    fileList=findFileList;unsolveFileList=unsolveFile
    pprint (U'findFileList--{}--{}--{}'.format(findFileList[0],type(findFileList[0]),len(findFileList)))
    print (u'X:/Project/2018/B003_S79_3/Asset_work/chars/XiaoJ/Texture/Texture/sourceimages/spec2_1001.jpg' in findFileList[0])
    Print (u'get file list take time--{}s'.format(collectFileTime-refreshPathTime))
    print ('unsolveFile-----',unsolveFile)
    # with open ('D:/aa/findList.txt','w') as f:
    #     f.write(str(findFileList))
    # with open('D:/aa/unsolveFile.txt','w') as f:
    #     f.write(str(unsolveFile))
    return findFileList,unsolveFile

def zipFiles(list_files,unsolveFile,outDir=''):
    mayaFile = cmds.file(q=True, expandName=True)
    mayaFileBaseName=os.path.basename(mayaFile)
    mayaFileDir =os.path.dirname(mayaFile)
    packDir=outDir
    fileReportFile=packDir+'/packLog.txt'
    if not os.path.exists(packDir):
        os.makedirs(packDir)
    diskName=list_files[0][0] if list_files[0][1]==':' else re.search('(//.+?/.+?)/',list_files[0]).group(1).replace('/','_')
    amount=len(list_files)
    Print (u'{}盘一共有{}个文件'.format(diskName.upper(),amount))
    
    def file2zip(zip_file_name, file_names):
        st=time.time();fileDaXiao=0
        with zipfile.ZipFile(zip_file_name, mode='w', compression=zipfile.ZIP_STORED,allowZip64 = True) as zf:
            listLen=len(file_names)
            progress=QProgressDialog(u"正在为您打包,请稍等", "Cancel", 0, listLen)
            progress.setFixedSize(700,170)
            progress.setCancelButtonText(u'停止打包')
            progress.setWindowFlags(Qt.WindowMinimizeButtonHint |   # 使能最小化按钮
                    Qt.WindowCloseButtonHint |      # 使能关闭按钮
                    Qt.WindowStaysOnTopHint) 
            for j,fn in enumerate(file_names):
                if progress.wasCanceled():
                    cmds.error(u'停止打包')
                progress.setValue(j)
                fileName=fn.split('/')[-1]
                fn=fn.replace('\\','/')
                try:
                    curFile=file_names[j+1]
                except:
                    try:
                        curFile=file_names[j]
                    except:
                        Print ('_______________________________')
                        continue
                if len(curFile)>85:
                    curFile=curFile[:85]+'\n'+curFile[85:]
                statinfo = os.stat(fn).st_size/1024/1024
                fileDaXiao+=statinfo
                speed=fileDaXiao/(time.time()-st)
                fileSize=str(os.path.getsize(fn)*1.0/1024/1024)[:6]
                if os.path.exists(fn):
                    progress.setLabelText(u'已完成{}/{},正在压缩{}盘文件:{}\n文件大小{}M,压缩速度{}M/s'.
                                          format(j,amount,diskName.upper(),curFile, fileSize,speed))
                    QtCore.QCoreApplication.processEvents()
                    zf.write(fn)     
                
                
               
        # win.close()
    zip_name = packDir+'/'+mayaFileBaseName+'_'+diskName+'.zip'
    #zip_name = r'X:\Project\2018\B014\Asset_work\chars\XY_CG\Texture\approve\Shader'+'/'+mayaFileBaseName+'_'+diskName+'.zip'
    file2zip(zip_name ,list(set(list_files)))
    unsolveFile='\n'.join(unsolveFile)
    unsolveFile=u'将对应盘符的压缩包解压到对应盘符的根目录,解压选项使用-"解压到当前文件夹"\n如果有arnold TX文件,原始贴图和TX贴图也会连着一起打包\nMaya文件路径:\n'+mayaFile+u'\n丢失文件列表:\n'+unsolveFile
    with codecs.open(fileReportFile,'w',encoding='utf-8') as openFileReportFile:
        openFileReportFile.write(unsolveFile)
    os.startfile(packDir)

class UI(QWidget):
    def __init__(self, parent = None):
        super(UI, self).__init__(parent)
        try:
            mayaFile = cmds.file(q=True, expandName=True)
            mayaFileBaseName=os.path.basename(mayaFile)
            mayaFileDir =os.path.dirname(mayaFile)
            packDir=mayaFileDir+'/ProjectPack'
            packDir='D:/ProjectPack'
        except:
            packDir='D:/ProjectPack'
        fileReportFile=packDir+'/packLog.txt'
        if not os.path.exists(packDir):
            os.makedirs(packDir)
        #self.resize(300, 200)
        self.setWindowTitle(u'打包文件')
        layout = QVBoxLayout()
        packSelGB=QGroupBox(u'请选择打包项目')
        packSelLay=QVBoxLayout()
        packSelGB.setLayout(packSelLay)
        self.ma=QCheckBox(u'模型资产类:Maya,Abc,Fbx,obj')
        self.ma.setChecked(True)
        self.image=QCheckBox(u'图片文件:jpg,jpeg,png,tif,tiff,tga,bmp,exr,psd,hdr,pic,tga,tx,iff')
        self.image.setChecked(True)
        self.xgen=QCheckBox(u'Xgen文件:xpd,xuv,xgc,xgen')
        self.xgen.setChecked(True)
        self.ptx=QCheckBox(u'3dPaint文件:(建议打包XGen时勾选此项)')
        self.ptx.setChecked(True)
        packSelLay.addWidget(self.ma)
        packSelLay.addWidget(self.image)
        packSelLay.addWidget(self.xgen)
        packSelLay.addWidget(self.ptx)
        
        self.packBn=QPushButton(u'打包(强烈建议选择打包到本地磁盘,打包速度会快10倍+)')



        
        layout.addWidget(packSelGB)
        
        #输出文件夹:
        self.oputDirWidget=LPathSel(par=layout,l_lab=u'请选择输出文件夹',buttonName=u'请选择输出文件夹',DialogCommit=u'请选择输出文件夹',stDir=packDir,fileType='*.ext',chooseFunc='getExistingDirectory',defaultPath='')
        
        layout.addWidget(self.packBn)
        self.tweakModeCkb=QCheckBox(u'调试模式')
        self.tweakModeCkb.stateChanged.connect(self.tweakMode)
        layout.addWidget(self.tweakModeCkb)
        self.tweakMode()
        self.packProjectFunc=partial(self.packProject,'AA')
        
        introductions_label=QLabel(u'该插件能抓取Maya文件引用到的所有贴图,.ma,.mb等文件')
        layout.addWidget(introductions_label)
        introductions_label.setObjectName('introductions_label')
        #self.setStyleSheet('QGroupBox{border:1px solid gray;border-radius:5px;margin-top:1ex;}')
        imageLay = QHBoxLayout()
        self.ColFiles=QLabel(u'正在搜集文件,请稍后...')
        self.ColFiles.setHidden(1)
        self.ColFiles.setObjectName('collectFiles')
        self.imageLabel=QLabel()
        self.gif=QMovie(fileDir+r'\loopProgressA.gif')
        self.gif.start()
        self.imageLabel.setMovie(self.gif)
        self.imageLabel.setHidden(1)
        
        
        imageLay.addWidget(self.ColFiles)
        imageLay.addWidget(self.imageLabel)
        layout.addLayout(imageLay)
        
        self.setLayout(layout)

        self.setStyleSheet('''
                           QGroupBox{font-size:15px;}
                           QCheckBox{font-size:17px;height:20px;}
                           QPushButton{font-size:17px;height:25px;}
                           QLabel#introductions_label{font-size:15px;}
                           QLabel#collectFiles{font-size:30px;color:red;height:40px;}
                           QComboBox{height:25px;}
                           '''
                           )
        
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |   # 使能最小化按钮
                            QtCore.Qt.WindowType.WindowCloseButtonHint |      # 使能关闭按钮
                            QtCore.Qt.WindowStaysOnTopHint) 

    def tweakMode(self):
        if self.tweakModeCkb.isChecked():
            self.packBn.clicked.connect(self.packProjectFunc)
            try:
                self.packBn.clicked.disconnect(self.runThread)
                print (u'断开多线程模式')
            except:
                print (u'断开多线程模式失败')
        else:
            self.packBn.clicked.connect(self.runThread)
            try:
                if hasattr(self,'packProjectFunc'):
                    self.packBn.clicked.disconnect(self.packProjectFunc)
                print (u'断开传统模式')
            except:
                print (traceback.format_exc())
                print (u'断开传统模式失败')
    
    def getMayaFile(self):
        mayaFile = cmds.file(q=True, expandName=True)
        return mayaFile
    
    def getFileType(self):
        fileType=(self.ma.isChecked(),self.image.isChecked(),self.xgen.isChecked(),self.ptx.isChecked())
        return fileType
    
    def runThread(self):
        self.thread = MyThread()
        self.thread.sec_changed_signal.connect(self.packProject)
        print (u'正在运行启动子线程...')
        self.thread.start()

    def packProject(self,sec,*args, **kwargs):
        pass
        if self.tweakModeCkb.isChecked():
            fileList,unsolveFile=getFileList(self.getFileType(),self.getMayaFile())
        else:
            fileList,unsolveFile=sec[0],sec[1]
        #pprint (sec)
        cmds.warning(u'更新更新列表完毕')
        for _fileList in fileList:
            zipFiles(_fileList,unsolveFile,outDir=self.oputDirWidget.text())
        print (u'打包结束')
        self.ColFiles.setHidden(1)
        self.imageLabel.setHidden(1)
        


class MyThread(QThread):
    print (u'--进入子线程aaaa--')
    sec_changed_signal = Signal(tuple)  # 信号类型：int
    def __init__(self,):
        
        self.mayaFile=mainUi.getMayaFile()
        self.fileType=mainUi.getFileType()
        Print ('self.fileType',self.fileType)
        super(MyThread,self).__init__()
        self.sec = (0,0)    
    def run(self):
        mainUi.gif.start()
        mainUi.ColFiles.setHidden(0)
        mainUi.imageLabel.setHidden(0)
        FileList=getFileList(self.fileType,self.mayaFile)
        self.sec_changed_signal.emit(FileList)  # 发射信号
        mainUi.ColFiles.setText(u'搜集文件完成,正在打包文件...')



def main(*args):
    if sys.executable.endswith('maya.exe'):
        pass
    else:
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    global mainUi 
    mainUi = UI()
    mainUi.show()
    if not sys.executable.endswith('maya.exe'):
        sys.exit(app.exec_())

# print (__name__)
# if __name__=='__main__':
#     main()
# import sys
# import inspect
# __file__=inspect.getfile(inspect.currentframe())
# sys.path.append(os.path.dirname(__file__))



