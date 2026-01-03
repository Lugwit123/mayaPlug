import hou,os
geo=hou.node('/obj').createNode('geo')
alembicNode=geo.createNode('alembic')
alembicNode.setParms({'fileName':'D:/aa.abc'})
geo=alembicNode.geometry()
center=geo.boundingBox().center()
Lugwit_publicPath=os.environ.get('Lugwit_publicPath')
with open(Lugwit_publicPath+'\\Temp\\temp.txt','w') as f:
    f.write(str(center))