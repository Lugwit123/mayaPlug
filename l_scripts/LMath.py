import os,re,sys
LugwitPath = os.path.dirname(__file__)
LugwitPath = LugwitPath.replace('\\', '/')
LugwitPath = re.search('.+/Lugwit_plug', LugwitPath).group(0)
if sys.version_info[0]==2:
    sys.path.insert(0,LugwitPath+r'\mayaPlug\materialPlug\python_library')
try:
    import numpy as np
except:
    pass
def dis(x,y):
    x=np.array([x[0],x[1],x[2]]);y=np.array([y[0],y[1],y[2]])
    d1=np.sqrt(np.sum(np.square(x-y)))
    return d1