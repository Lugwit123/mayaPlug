import sys
sys.path.insert(0,r'Z:\plug_in\Lugwit_plug\mayaPlug\l_scripts\IOLib')
import exFbx
exFbx.exAniClip(exABC=0,mayaFile=cmds.file(q=1,sn=1),openNewFile=1,replaceExit=0,renderExportFbx=1,cusCfg=0,ExDir='D:/aa')