# 列出渲染层
lays=cmds.ls(type='renderLayer')
# 切换渲染层
for lay in lays:
    cmds.editRenderLayerGlobals(currentRenderLayer=lay,) 
    cmds.editRenderLayerMembers(lay,q=1,)                              
    
def get_overrides(layer):
    overrides = {}
    c = 0
    for plug in cmds.listConnections(layer+'.adjustments',
        destination=False, source=True, plugs=True):
        print 'Override found:', plug
        adjusted_values = []
        attr_values = cmds.getAttr(layer+'.adjustments[' + str(c) + ']')
        for attr_value in attr_values:
            unadjusted_value = attr_value[0]
            adjusted_value = attr_value[1]
            adjusted_values.append(adjusted_value)
            overrides[plug] = adjusted_values
            c += 1
    return overrides

overrides = get_overrides(layer='')
print cmds.listConnections('layer1.adjustments')