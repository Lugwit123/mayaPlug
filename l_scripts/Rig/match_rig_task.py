# -*- coding: utf-8 -*-
import json
import os
import re
import codecs
import maya.cmds as cmds

class RigMatcher:
    def __init__(self, config_file="rig_rename_config.json"):
        u"""初始化，加载配置文件"""
        self.config_file = os.path.join(os.path.dirname(__file__), config_file)
        self.config = self.load_config()
    
    def load_config(self):
        u"""加载JSON配置文件"""
        if os.path.exists(self.config_file):
            try:
                with codecs.open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(u"加载配置文件失败: {}".format(e))
                return None
        else:
            print(u"配置文件不存在: {}".format(self.config_file))
            return None
    
    def save_config(self, config=None):
        u"""保存配置到JSON文件"""
        if config is None:
            config = self.config
        try:
            with codecs.open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            print(u"配置已保存到: {}".format(self.config_file))
        except Exception as e:
            print(u"保存配置文件失败: {}".format(e))
    
    def get_all_nodes_in_group(self, group):
        u"""获取组中的所有节点"""
        if not cmds.objExists(group):
            print(u"组 '{}' 不存在".format(group))
            return []
        
        # 获取组下所有子节点
        children = cmds.listRelatives(group, allDescendents=True, type='joint') or []
        all_nodes = [group] + children  # 包含组本身和所有子节点
        
        return all_nodes
    
    def find_nodes_to_rename(self, group):
        u"""根据配置文件找到需要重命名的节点"""
        if not self.config or "rename_rules" not in self.config:
            print(u"配置文件加载失败或格式错误")
            return []
        
        all_nodes = self.get_all_nodes_in_group(group)
        rename_pairs = []
        
        print(u"开始查找需要重命名的节点...")
        print(u"总共 {} 个节点".format(len(all_nodes)))
        
        for node in all_nodes:
            # 获取节点的短名称（不包含父级路径）
            short_name = node.split("|")[-1]
            
            # 检查每个重命名规则
            for old_pattern, new_pattern in self.config["rename_rules"].items():
                if old_pattern in short_name:
                    # 替换名称中的模式
                    new_name = short_name.replace(old_pattern, new_pattern)
                    if new_name != short_name:  # 确保名称确实改变了
                        rename_pairs.append((node, new_name))
                        print(u"找到匹配: '{}' -> '{}'".format(short_name, new_name))
                        break  # 找到第一个匹配就跳出，避免重复替换
        
        return rename_pairs
    
    def preview_rename(self, group):
        u"""预览重命名操作"""
        print("=" * 60)
        print(u"重命名预览:")
        print(u"目标组: {}".format(group))
        print("=" * 60)
        
        rename_pairs = self.find_nodes_to_rename(group)
        
        if not rename_pairs:
            print(u"没有找到需要重命名的节点")
            return []
        
        print(u"\\n将要执行的重命名操作:")
        for old_name, new_name in rename_pairs:
            print(u"  '{}' -> '{}'".format(old_name.split("|")[-1], new_name))
        
        print("=" * 60)
        return rename_pairs
    
    def apply_rename(self, group, preview_only=False):
        u"""执行重命名操作"""
        rename_pairs = self.find_nodes_to_rename(group)
        
        if not rename_pairs:
            print(u"没有找到需要重命名的节点")
            return []
        
        # 显示预览
        print(u"\\n将要执行的重命名操作:")
        for old_name, new_name in rename_pairs:
            print(u"  '{}' -> '{}'".format(old_name.split("|")[-1], new_name))
        
        if preview_only:
            return rename_pairs
        
        # 直接执行重命名，不需要确认
        success_count = 0
        for old_name, new_name in rename_pairs:
            try:
                if cmds.objExists(old_name):
                    result_name = cmds.rename(old_name, new_name)
                    print(u"成功: '{}' -> '{}'".format(old_name.split("|")[-1], result_name))
                    success_count += 1
                else:
                    print(u"错误: 节点 '{}' 不存在".format(old_name))
            except Exception as e:
                print(u"重命名失败 '{}': {}".format(old_name.split("|")[-1], e))
        
        print(u"重命名完成，成功 {}/{} 个节点".format(success_count, len(rename_pairs)))
        return rename_pairs

# 便捷函数
def quick_preview(group="Grp"):
    u"""快速预览重命名"""
    matcher = RigMatcher()
    return matcher.preview_rename(group)

def quick_rename(group="Grp"):
    u"""快速执行重命名"""
    matcher = RigMatcher()
    return matcher.apply_rename(group)

def batch_rename(group="Grp", preview_only=False):
    u"""批量重命名（默认直接执行）"""
    matcher = RigMatcher()
    return matcher.apply_rename(group, preview_only)

# 主执行部分
if __name__ == "__main__":
    # 示例用法
    matcher = RigMatcher()
    if matcher.config:
        # 预览重命名
        matcher.preview_rename("Grp")
        
        # 如果要执行重命名，取消下面的注释
        # matcher.apply_rename("Grp")

'''
使用示例:

# 方式1: 直接使用便捷函数
import Rig.match_rig_task
reload(Rig.match_rig_task)

# 预览重命名
Rig.match_rig_task.quick_preview("Grp")

# 执行重命名
Rig.match_rig_task.quick_rename("Grp")

# 方式2: 使用类
matcher = Rig.match_rig_task.RigMatcher()
matcher.preview_rename("Grp")
matcher.apply_rename("Grp")
'''
