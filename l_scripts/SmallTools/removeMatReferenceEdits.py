import os,sys
sys.path.append(r'D:\TD_Depot\plug_in\Lugwit_plug\mayaPlug')
import load_pymel
pm=load_pymel.pm
allRef=pm.listReferences()
for ref in allRef:
    ref.unload()
    referenceEdits=pm.referenceQuery(ref, editStrings=True )
    for referenceEdit in referenceEdits:
        if 'dagSetMembers' in str(referenceEdit) or 'aiStandardSurface' in str(referenceEdit):
            referenceEdit.remove()
    ref.load()