import sys,os,inspect
__file__=inspect.getfile(inspect.currentframe())
print ('__file__:',inspect.getfile(inspect.currentframe()))
fileDir=os.path.dirname(__file__)
sys.path.append(fileDir)
print ('fileDir:',fileDir)
import sppaint3d.spPaint3dGui as spPaint3dGui
spPaint3dwin=spPaint3dGui.spPaint3dWin()