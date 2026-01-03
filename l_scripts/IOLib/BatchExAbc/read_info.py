import json
import codecs
jsonFile=r'A:/temp/MayaToUE/ExHis/WXXJDGD/OC6/exAniClip_ep001_sc001_shot0010_anim_comment.json'


with codecs.open(jsonFile, 'r', encoding='utf-8') as f:
    data = json.load(f)
nameSplaceList=data['nameSpace']
print(nameSplaceList)