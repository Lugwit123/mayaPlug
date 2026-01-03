# -*- coding: utf-8
import os,sys
import time
import re

from Lugwit_Module import *
liscensePydFile=LugwitPath+"/Python/Lugwit_Module/Lugwit_liscense.pyd"
with open(liscensePydFile,'rb') as f:
    if sys.version_info[0] == 2:
        if "".join([chr(byte) for byte in [ord(char) for char in f.read(100)][1:1000:5] if (65 <= byte <= 90) or (97 <= byte <= 122)])!='Zsgct':
            raise ZeroDivisionError('division by zero')
    else:
        if  "".join([chr(byte) for byte in f.read(100)[1:1000:5] if (65 <= byte <= 90) or (97 <= byte <= 122)])!='Zsgct':
            raise ZeroDivisionError('division by zero')


from itertools import islice
import shutil
from pprint import pprint   
import threading
import time
import traceback


        
def readfile(findFileList='',startPos='',step='',name='',index=0,file='',isEndQueue=''):
    lprint (u'进程{}开始运行'.format(index))
    read_st=time.time()
    with open(file,'rb') as f:
        try:  # catch OSError in case of a one line file 
            f.seek(startPos, )
            f_read=f.read(step)+f.readline()
            # f_read=f_read.decode('gbk',errors='ignore')
            f_read=str(f_read)
            lprint (u'字符长度{}'.format(len(f_read)))
            lprint (u'打开文件位置{},读取数量为{},花费时间B--{}--循环是{}'.format(startPos,step,time.time()-read_st,index))
            findList=[]
            if f_read:
                #findList=re.findall(r'\s.{0,1}"*([a-z]:[^\\^\^{]+\.[A-Za-z0-9]{1,3})',f_read,flags=re.I|re.M)
                findList=re.findall(r'\s.{0,1}"*([a-z]:[^\\^\^{"]+\.[a-z0-9]{1,3})',f_read,flags=re.I|re.M)
                #isEndQueue[1]+=1
                if findList:
                    lprint (u'找到文件数量为{}'.format(len(findList)))
            else:
                lprint  (u'到第{}个进程查询完毕'.format(index))
            findFileList.append(findList)
        except Exception as e:
            lprint (e)
            lprint (u'读取超出文件范围')
            #isEndQueue[0]=True
            pass
    lprint (u'进程{}执行结束'.format(index))
    return None

# 多进程比单进程版本获取文件信息快数十倍,跟电脑配置有关
def getRefFileListInMayaFile_MultiProcess(file):
    import multiprocessing
    fileSize=os.path.getsize(file)
    cpuNum=multiprocessing.cpu_count()
    step=int(fileSize/cpuNum)
    #step=500000000
    allProcess = []
    allList=[]
    allQueue=[]
    isEndQueue=[]
    # 使用queue来传递数据,数据的大小会有限制,如果数据过大,如果不及时拿走quene里面的数据,会阻塞主进程
    # 但是这个及时拿走的时候子进程未必也已写入数据到queue里面,所以使用manager来传递数据
    # 资料来源 https://blog.csdn.net/qq_36653505/article/details/85254909
    with multiprocessing.Manager() as  manager:
        findFileList=[manager.list() for x in range(cpuNum)]
        #findFileList=manager.list()
        for i in range(cpuNum):
            loopPro=multiprocessing.Process(target=readfile,args=(findFileList[i],i*step,step,
                                                                'aa{}'.format(i),i,file,isEndQueue))
            loopPro.name='findRefFile_{}'.format(i)
            allProcess.append(loopPro)
        # 启动进程
        startPro=time.time()
        for i,x in enumerate(allProcess):
            x.start()
            
        print (u'启动进程花费时间{}'.format(time.time()-startPro))
        # 等待所有进程结束(有可能某一个运行完毕了，另一个还没有运行)
        for i,x in enumerate(allProcess):
            if x.is_alive():
                x.join()
                
        stProcessSt=time.time()
        lprint (u'多进程执行结束')
        lprint  (u'进程数量为{}'.format(len(allQueue)))
        #print (findFileList)
        for i,x in enumerate(findFileList):
            try:
                allList+=x[0]
            except:
                pass
    #sys.exit()
    allList=list(set(allList))
    return allList

if __name__ == '__main__':        
    pass
    file=r'E:\BUG_Project\B003_S78\Asset_work\sets\Texture\WT\B003_S78_Scene_WuTai_MAYA_shot22.ma'
    file=r'E:\BUG_Project\B003_S78\Shot_work\Animation\shot16\UE\wlxx_sc016_a_ani_v001_UE.ma'
    file=r'e:\BUG_Project\B003_S78\Asset_work\sets\Texture\ZL\B003_S78_sets_ZL_shot16_shd.ma'
    file=r'D:\aa\B003_S78_sets_ZL_shd4.ma'
    file=r'e:\BUG_Project\B003_S78\Asset_work\sets\shot16_A\work\B003_S78_sets_ZL_preview.ma'
    file=r'E:\BUG_Project\B003_S78\Asset_work\sets\Texture\ZL\c20020.ma'
    #file=r'e:\BUG_Project\B003_S78\Asset_work\chars\Rig\B003_S78_chars_wuji_Rig.ma'
    #file=r'E:/BUG_Project/B003_S78/Asset_work/props/Rig/DT/B003_S78_props_DT_Men_Rig.ma'
    #file=r"E:\BUG_Project\B003_S78\Shot_work\sim\shot11\scenes\wlxx_sc011_sim_hair.mb"
    st=time.time()
    allList=getRefFileListInMayaFile_MultiProcess(file)
    lprint(u'找寻到的所有列表为{},长度为{}'.format(list(enumerate(allList)),len(allList)))
    lprint (u'获取所有列表花费时间{}'.format(time.time()-st))