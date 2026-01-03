import sys
import sys,os,inspect
__file__=inspect.getfile(inspect.currentframe())
print ('__file__:',inspect.getfile(inspect.currentframe()))
fileDir=os.path.dirname(__file__)
sys.path.append(fileDir)
print ('fileDir:',fileDir)

import animPolish.ui
reload (animPolish.ui)
animPolish.ui.ui ()