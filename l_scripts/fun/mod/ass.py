import re
import os

# 完整路径
path = "H:/JZXCL/4.Assets/Char/C_A001_HanYang/Rig/C_A002_HanYang_Rig1.ma"

# 提取文件名
base_name = os.path.basename(path)

# 使用正则表达式匹配并排除 '_Rig' 和 '.ma' 扩展名
# 注意这里正则表达式的设计尽量确保处理各种可能的 '_Rig' 和数字组合
pattern = r'(.+?)(?:_Rig\d*)?(?:\.\w+)?$'
match = re.search(pattern, base_name)
if match:
    result = match.group(1)
    print(result)  # 输出: C_A002_HanYang1
else:
    print("No match found")
