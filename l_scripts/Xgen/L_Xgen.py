mayaFile=r'D:/aa/aa.ma'
mayaFileContents=''
openMayaFile=codecs.open(mayaFile,'r',encoding='gbk')
while 1:
    mayaFileContents += openMayaFile.read(5000)
    print ('mayaFileContents',mayaFileContents[:-100])
    if not mayaFileContents:
        openMayaFile.close()
        break
xgenFileName=re.search('setAttr ".xfn" -type "string" "(.+)";',mayaFileContents,flags=re.I)
if xgenFileName:
    xgenFileName=xgenFileName.group(1)
    xgenPath=os.path.dirname(child_path)+'/'+xgenFileName
    xgenDir=os.path.dirname(xgenPath)
    fileInXgenDir=os.listdir(xgenDir)
    for _fileInXgenDir in fileInXgenDir:
        if _fileInXgenDir.startswith(os.path.basename(child_path)+'__'):
            P4Lib.getFile(_fileInXgenDir)
    # P4Lib.getFile(xgenDir)
    # print ('xgenDir----------------------',xgenDir)
    print ('xgenPath----------------------',xgenPath)
    P4Lib.getFile(xgenPath)
    print ('xgenPath----------------------',xgenPath)
    if os.path.exists(xgenPath):
        with codecs.open (xgenPath,'r',encoding='utf8') as f:
            f_read=f.read()
        xgDataPath=re.search('xgDataPath\s+(.+)\r*\n',f_read).group(1)
        if xgDataPath.endswith('\\') or xgDataPath.endswith('/'):
            xgDataPath=xgDataPath[:-1]
        print ('xgDataPath-->',xgDataPath,end='=========')

        secList.append(xgenPath)
        secList.append(xgDataPath)
