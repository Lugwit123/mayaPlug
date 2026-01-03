# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
"""
UI助手模块 - 用于驱动UI组件更新
专门针对Maya 2020 + PySide2 + Python 2.7环境设计
参考ui_components.py的设计，简化版实现

线程安全UI更新说明：
===================
在Maya等GUI应用程序中，UI操作必须在主线程中执行。本模块提供了以下解决方案：

1. @thread_safe_ui_update 装饰器
   - 自动检测线程并在主线程中执行UI操作
   - 使用Maya的utils.executeDeferred()确保线程安全

使用示例：

# 使用装饰器（已应用到所有UI更新方法）
@thread_safe_ui_update
def update_ui_element(self):
    self.combo_box.clear()
    self.combo_box.addItems(items)
"""

import os
import sys
import re
import traceback



# 导入日志模块
import Lugwit_Module as LM
lprint = LM.lprint

# Maya相关导入
import maya.cmds as cmds
import maya.utils as utils

# 线程安全的UI更新装饰器
def thread_safe_ui_update(func):
    u"""确保UI更新在主线程中执行的装饰器 - Maya 2020专用"""
    def wrapper(*args, **kwargs):
        # 使用Maya的executeDeferred确保在主线程执行
        def deferred_func():
            try:
                return func(*args, **kwargs)
            except Exception as e:
                lprint(u"[线程安全] UI更新失败: {0}".format(unicode(e)))
                traceback.print_exc()
        
        # 检查是否已在主线程
        try:
            import threading
            current_thread = threading.current_thread()
            if current_thread.name == 'MainThread' or isinstance(current_thread, threading._MainThread):
                return func(*args, **kwargs)
            else:
                #utils.executeDeferred(deferred_func)
                utils.executeInMainThreadWithResult(deferred_func)
        except:
            # 如果无法判断线程，直接使用executeDeferred
            utils.executeDeferred(deferred_func)
    return wrapper

# 简单的单例装饰器
def singleton(cls):
    """简单的单例装饰器"""
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance





@singleton
class ProjectHelper(object):
    u"""项目选择辅助类 - 数据中心驱动模式 (单例)"""
    
    def __init__(self, main_window=None, project_combo=None):
        self.main_window = main_window
        self.project_combo = project_combo
        self.data_center = None
        
        # 连接UI事件
        if self.project_combo:
            self.project_combo.currentTextChanged.connect(self._on_project_changed)

    def set_data_center(self, data_center):
        u"""设置数据中心"""
        self.data_center = data_center
    
    def _on_project_changed(self, project_text):
        u"""项目下拉框变化事件"""
        lprint(u"[项目辅助] 用户选择项目: {0}".format(project_text))
        
        # 通知数据中心项目变化
        if self.data_center:
            # 查找对应的项目数据
            for project in self.data_center.project_list:
                if project == project_text:
                    self.data_center.current_project = project
                    break
    
    @thread_safe_ui_update
    def _on_data_center_project_change(self, project_data):
        """数据中心项目变化回调"""
        if project_data:
            lprint(u"[项目辅助] 数据中心项目切换到: {}".format(project_data.display_name))
            
            # 更新UI（但不触发回调）
            self.project_combo.blockSignals(True)
            try:
                # 找到对应的选项并设置
                for i in range(self.project_combo.count()):
                    if self.project_combo.itemText(i) == project_data.project_name:
                        self.project_combo.setCurrentIndex(i)
                        break
            finally:
                self.project_combo.blockSignals(False)
    
    @thread_safe_ui_update
    def update_project_list(self, project_list):
        """更新项目列表"""
        if not self.project_combo or not project_list:
            return

        
        self.project_combo.blockSignals(True)
        try:
            self.project_combo.clear()
            for project_name in project_list:
                self.project_combo.addItem(project_name)  # 直接使用字符串
            lprint(u"[项目辅助] 项目列表已更新: {} 个项目".format(len(project_list)))
        finally:
            self.project_combo.blockSignals(False)
    
    @thread_safe_ui_update
    def set_current_project(self, project_name):
        """设置当前项目"""
        if not self.data_center:
            lprint(u"[项目辅助] 警告: 数据中心未设置，无法设置当前项目")
            return False
            
        # 查找对应的项目数据
        for project in self.data_center.project_list:
            if project == project_name:
                self.data_center.current_project = project
                lprint(u"[项目辅助] 当前项目已设置为: {}".format(project_name))
                
                # 同步更新UI（但不触发回调）
                if self.project_combo:
                    self.project_combo.blockSignals(True)
                    try:
                        # 找到对应的选项并设置
                        for i in range(self.project_combo.count()):
                            if self.project_combo.itemText(i) == project_name:
                                self.project_combo.setCurrentIndex(i)
                                break
                    finally:
                        self.project_combo.blockSignals(False)
                
                return True
        
        lprint(u"[项目辅助] 错误: 项目 '{}' 不存在于项目列表中".format(project_name))
        return False


@singleton
class ShotHelper(object):
    """镜头信息辅助类 (单例)"""
    
    def __init__(self, main_window=None, ep_combo=None, sc_combo=None, shot_combo=None):
        self.main_window = main_window
        self.ep_combo = ep_combo
        self.sc_combo = sc_combo
        self.shot_combo = shot_combo
        self.data_center = None
        
        # 连接UI事件
        if self.ep_combo:
            self.ep_combo.currentTextChanged.connect(self._on_episode_changed)
        if self.sc_combo:
            self.sc_combo.currentTextChanged.connect(self._on_sequence_changed)
        if self.shot_combo:
            self.shot_combo.currentTextChanged.connect(self._on_shot_changed)
        
        # 连接JSON预设文件变化事件
        if self.main_window and hasattr(self.main_window, 'ui') and hasattr(self.main_window.ui, 'jsonPreset_Combo'):
            self.main_window.ui.jsonPreset_Combo.currentTextChanged.connect(self._on_json_preset_changed)
    
    def set_data_center(self, data_center):
        """设置数据中心"""
        self.data_center = data_center

    
    def _on_episode_changed(self, episode_text):
        """集变化事件"""
        lprint(u"[镜头辅助] 用户选择集: {}".format(episode_text))
        if self.data_center:
            self.data_center.current_episode_name = episode_text

    
    def _on_sequence_changed(self, sequence_text):
        """场变化事件"""
        lprint(u"[镜头辅助] 用户选择场: {}".format(sequence_text))
        if self.data_center:
            self.data_center.current_sequence_name = sequence_text

    
    def _on_shot_changed(self, shot_text):
        """镜头变化事件"""
        lprint(u"[镜头辅助] 用户选择镜头: {}".format(shot_text))
        if self.data_center and shot_text:
            # 直接设置当前镜头名称
            self.data_center.current_shot_name = shot_text
    
    def _on_json_preset_changed(self, json_file_path):
        """JSON预设文件变化事件"""
        lprint(u"[镜头辅助] JSON预设文件变化: {}".format(json_file_path))
        if self.data_center and json_file_path:
            # 通过数据中心的属性设置当前预设文件
            self.data_center.current_preset_file = json_file_path
    
    @thread_safe_ui_update
    def update_actual_dir(self,):
        """更新 actualDirWgt 组件的值"""
        project_name = self.data_center.current_project
        episode_name = self.data_center.current_episode_name
        sequence_name = self.data_center.current_sequence_name
        shot_name = self.data_center.current_shot_name
        actual_dir = "D:\\Work\\{}\\{}_{}_{}\\abc_sim".format(project_name, episode_name, sequence_name, shot_name)
        self.main_window.ui.actualDirWgt.clear()
        self.main_window.ui.actualDirWgt.addItem(actual_dir)
        lprint(u"[镜头辅助] actualDirWgt已更新: {}".format(actual_dir))
    

    
    @thread_safe_ui_update
    def update_episode_list(self, episode_list=[]):
        """更新集列表"""
        if not self.data_center or not self.ep_combo:
            return
        
        self.ep_combo.blockSignals(True)
        try:
            self.ep_combo.clear()
            for episode in episode_list:
                self.ep_combo.addItem(episode)
            
            # 自动选择第一个
            if episode_list:
                self.ep_combo.setCurrentText(self.data_center.current_episode_name)
            lprint(u"[镜头辅助] 集列表已更新: {} 个集".format(len(episode_list)))
        finally:
            self.ep_combo.blockSignals(False)
    
    @thread_safe_ui_update
    def update_sequence_list(self, sequence_list=[]):
        """更新场列表"""
        if not self.data_center or not self.sc_combo:
            return
        
        self.sc_combo.blockSignals(True)
        try:
            self.sc_combo.clear()
            self.sc_combo.addItems(sorted(sequence_list))
            lprint(u"[镜头辅助] 场列表已更新: {} 个场".format(len(sequence_list)))
        finally:
            self.sc_combo.blockSignals(False)
    
    @thread_safe_ui_update
    def update_shot_list(self, current_shot_list=[]):
        """更新镜头列表"""
        lprint(self.data_center,self.shot_combo,len(current_shot_list))
        if not self.data_center or not self.shot_combo or not len(current_shot_list):
            return
        self.shot_combo.blockSignals(True)
        try:
            self.shot_combo.clear()
            self.shot_combo.addItems(current_shot_list)
            lprint(u"[镜头辅助] 镜头列表已更新: {} 个镜头".format(len(current_shot_list)))
        finally:
            self.shot_combo.blockSignals(False)
    
    @thread_safe_ui_update
    def update_preset_list(self, preset_list):
        """更新预设文件列表"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return
        
        ui = self.main_window.ui
        if hasattr(ui, 'jsonPreset_Combo'):
            ui.jsonPreset_Combo.blockSignals(True)
            try:
                ui.jsonPreset_Combo.clear()
                ui.jsonPreset_Combo.addItems(preset_list)
                
                # 如果有文件，自动选择第一个并加载JSON
                if preset_list:
                    ui.jsonPreset_Combo.setCurrentText(preset_list[-1])
                    # 自动加载第一个JSON文件并更新导出名称

                self.main_window.ui_helper.export_name_helper.load_preset_json(ui.jsonPreset_Combo.currentText())
                self.main_window.ui_helper.export_name_helper.update_export_names_in_grid()
                    
                lprint(u"[镜头辅助] 预设文件列表已更新: {} 个文件".format(len(preset_list)))
            finally:
                ui.jsonPreset_Combo.blockSignals(False)
        
        
    
    @thread_safe_ui_update
    def set_current_episode(self, episode_name):
        """设置当前集"""
        if self.ep_combo:
            self.ep_combo.blockSignals(True)
            try:
                self.ep_combo.setCurrentText(episode_name)
            finally:
                self.ep_combo.blockSignals(False)
    
    @thread_safe_ui_update
    def set_current_sequence(self, sequence_name):
        """设置当前场"""
        if self.sc_combo:
            self.sc_combo.blockSignals(True)
            try:
                self.sc_combo.setCurrentText(sequence_name)
            finally:
                self.sc_combo.blockSignals(False)
    
    @thread_safe_ui_update
    def set_current_shot(self, shot_name):
        """设置当前镜头"""
        if self.shot_combo:
            self.shot_combo.blockSignals(True)
            try:
                self.shot_combo.setCurrentText(shot_name)
            finally:
                self.shot_combo.blockSignals(False)
    
    @thread_safe_ui_update
    def _update_ui_selection(self, shot_data):
        """更新UI选择状态"""
        # 阻止信号避免循环调用
        for combo in [self.ep_combo, self.sc_combo, self.shot_combo]:
            if combo:
                combo.blockSignals(True)
        
        try:
            if self.ep_combo:
                self.ep_combo.setCurrentText(shot_data.episode)
            if self.sc_combo:
                self.sc_combo.setCurrentText(shot_data.sequence)
            if self.shot_combo:
                self.shot_combo.setCurrentText(shot_data.shot_name)
        finally:
            # 恢复信号
            for combo in [self.ep_combo, self.sc_combo, self.shot_combo]:
                if combo:
                    combo.blockSignals(False)


@singleton
class ExportNameHelper(object):
    """导出名称辅助类 - 根据JSON预设文件和名称空间设置导出名称"""
    
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.current_json_data = None
    
    def load_preset_json(self, json_file_path):
        """加载JSON预设文件"""
        if not json_file_path or not os.path.exists(json_file_path):
            self.current_json_data = None
            return
        
        try:
            import json
            import codecs
            with codecs.open(json_file_path, 'r', encoding='utf-8') as f:
                self.current_json_data = json.load(f)
            lprint(u"[导出名称辅助] JSON预设文件已加载: {}".format(os.path.basename(json_file_path)))
        except Exception as e:
            lprint(u"[导出名称辅助] JSON文件加载失败: {}".format(str(e)))
            self.current_json_data = None
    
    def get_export_name_for_namespace(self, namespace):
        """根据名称空间从JSON中查询导出名称 - 两阶段逻辑"""

        
        # 第一阶段：JSON未加载时使用简化逻辑
        if not self.current_json_data:
            return self._get_simple_export_name(namespace)
        
        # 第二阶段：JSON已加载，使用JSON配置
        nameSpace_data = self.current_json_data.get("nameSpace", {})
        namespace_config = nameSpace_data.get(namespace, {})
        lprint(nameSpace_data,namespace_config)
        # 优先查找 CfxToLighAbcExPath 路径
        cfx_path = namespace_config.get("filePathList", {})\
                        .get("AniToLightSkeAniFbxExPath", {})\
                        .get("filePath", "")
        lprint(cfx_path)
        cfx_path = re.sub(r"(_anitolgt)*\.fbx$","_cfx",cfx_path,flags=re.I)
        cfx_path = cfx_path.replace(".abc","")
        lprint(cfx_path)
        if cfx_path:
            # 只返回文件名，不要完整路径
            export_name = os.path.basename(cfx_path)
            return self._clean_export_name(export_name)
        
        # 如果JSON中没找到，回退到简化逻辑
        return self._get_simple_export_name(namespace)
    
    def _get_simple_export_name(self, namespace):
        """简化逻辑：根据当前镜头名称生成导出名称"""
        # 尝试从数据中心获取集场镜信息
        if self.main_window and hasattr(self.main_window, 'data_center') and self.main_window.data_center:
            data_center = self.main_window.data_center
            try:
                project_name = getattr(data_center, 'current_project', '')
                episode_name = getattr(data_center, 'current_episode_name', '')
                sequence_name = getattr(data_center, 'current_sequence_name', '')
                shot_name = getattr(data_center, 'current_shot_name', '')
                
                # 如果有完整的镜头信息，构建完整名称
                if episode_name and sequence_name and shot_name:
                    shot_entire_name = "{}_{}_{}_{}".format(episode_name, sequence_name, shot_name, namespace)
                    return re.sub("_rig","","{}_cfx".format(shot_entire_name),flags=re.I)
            except Exception as e:
                lprint(u"[导出名称辅助] 从数据中心获取镜头信息失败: {}".format(str(e)))
        
        # 默认命名：仅使用名称空间
        return re.sub("_rig","","{}_cfx".format(namespace),flags=re.I)
    
    def _clean_export_name(self, export_name):
        """清理导出名称格式"""
        if not export_name:
            return "default_cfx.abc"
        
        # 处理路径分隔符和特殊字符
        export_name = export_name.replace('__', '_').replace('|', '_')
        
        # 移除开头的下划线
        while export_name.startswith('_'):
            export_name = export_name[1:]
        
        return export_name
    
    @thread_safe_ui_update
    def set_export_name_for_combo(self, combo_box, namespace):
        """为组合框设置导出名称 - 兼容原 setExNameFromAbc 方法"""
        export_name = self.get_export_name_for_namespace(namespace)
        combo_box.blockSignals(True)
        combo_box.clear()
        combo_box.addItem(export_name)
        combo_box.setCurrentText(export_name)
        combo_box.blockSignals(False)
        lprint(locals())
        lprint(u"[导出名称辅助] 设置导出名称: {} -> {}".format(namespace, export_name))
    
    @thread_safe_ui_update
    def populate_grid_layout(self):
        """填充Grid布局 - 从Maya获取选择节点并创建UI（初始化填充，不依赖JSON）"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return
        
        from PySide2.QtWidgets import QLabel, QComboBox, QLineEdit, QPushButton
        from functools import partial
        
        # 清空现有的行（保留标题行）
        grid_layout = self.main_window.ui.exListGridLay
        if hasattr(self.main_window, 'qttool'):
            self.main_window.qttool.collect_and_clear_non_zero_row_widgets(grid_layout)
        
        # 获取Maya选择的节点
        selNodeList = cmds.ls(sl=1)
        
        if not selNodeList:
            lprint(u"[导出名称辅助] 没有选择任何节点")
            return
        
        # 提取名称空间并去重 - 这个将用于创建名称空间下拉选项
        namespaceListFromSelected = list(set(x.split(":")[0] for x in selNodeList))
        
        # 获取缓存匹配模式
        cacheMatchPattern = "*cache*,Geometry"
        if hasattr(self.main_window.ui, 'cacheMatchPatternWgt'):
            cacheMatchPattern = self.main_window.ui.cacheMatchPatternWgt.text()
        lprint(selNodeList,namespaceListFromSelected)
        # 为每个选择的节点创建UI行
        for i, ele in enumerate(selNodeList):
            nameSpace = ele.split(':')[0] if ':' in ele else ''
            
            for j in range(5):
                existing_widget = grid_layout.itemAtPosition(i+1, j)
                if existing_widget and existing_widget.widget():
                    grid_layout.removeWidget(existing_widget.widget())
                    try:
                        existing_widget.widget().deleteLater()  # 可选：彻底删除
                    except:
                        pass
 
                if j == 0:  # 选择物体列
                    widget = QLabel(ele)
                    grid_layout.addWidget(widget, i+1, j)
                
                elif j == 1:  # 名称空间列
                    ns_combo = QComboBox()
                    # 当前节点的名称空间作为默认选项
                    if nameSpace:
                        ns_combo.addItem(nameSpace)
                    lprint(nameSpace)
                    # 添加所有从选择节点中提取的名称空间作为选项
                    for ns in namespaceListFromSelected:
                        if ns != nameSpace and ns:  # 避免重复
                            ns_combo.addItem(ns)
                    grid_layout.addWidget(ns_combo, i+1, j)
                    
                elif j == 2:  # 导出组列
                    # 根据缓存匹配模式查找导出组
                    matchGrpList = self._find_matching_groups(nameSpace, cacheMatchPattern)
                    widget = QLineEdit(str(matchGrpList))
                    grid_layout.addWidget(widget, i+1, j)
                    
                elif j == 3:  # 导出名称列
                    export_combo = QComboBox()
                    export_combo.setFixedHeight(25)
                    export_combo.setEditable(True)
                    
                    # 初始化时使用简化逻辑生成导出名称
                    initial_name = self._get_simple_export_name(nameSpace)
                    export_combo.addItem(initial_name)
                    export_combo.setCurrentText(initial_name)
                    
                    grid_layout.addWidget(export_combo, i+1, j)
                    
                    # 连接名称空间变化事件
                    ns_combo.currentTextChanged.connect(
                        partial(self._on_namespace_changed, export_combo))
                    
                elif j == 4:  # 选择按钮列
                    button = QPushButton(u"选择")
                    grid_layout.addWidget(button, i+1, j)
                    button.clicked.connect(partial(self._on_select_group, i+1))
        
        lprint(u"[导出名称辅助] Grid布局已填充: {} 个节点，{} 个名称空间".format(
            len(selNodeList), len(namespaceListFromSelected)))
    
    def _find_matching_groups(self, namespace, cache_pattern):
        """查找匹配的导出组 - 根据cacheMatchPatternWgt中的模式在指定名称空间下查找所有匹配的组"""
        
        try:
            
            # 解析缓存匹配模式，支持逗号分隔的多个模式
            patterns = [p.strip() for p in cache_pattern.split(',')]
            matchGrpList = []
            
            lprint(u"[导出名称辅助] 在名称空间 '{}' 中查找匹配模式: {}".format(namespace, patterns))
            
            for pattern in patterns:
                if not pattern:  # 跳过空模式
                    continue
                
                found_groups = []
                
                if namespace:
                    # 在指定名称空间中查找匹配的transform节点
                    # 支持通配符模式，如 "*cache*"
                    search_pattern = "{}:{}".format(namespace, pattern)
                    found_nodes = cmds.ls(search_pattern, type='transform')
                    
                    # 也尝试在名称空间下的所有子节点中查找
                    if '*' in pattern:
                        # 对于通配符模式，直接使用ls命令
                        found_nodes.extend(cmds.ls(search_pattern, type='transform'))
                    else:
                        # 对于精确匹配，检查节点是否存在
                        exact_node = "{}:{}".format(namespace, pattern)
                        if cmds.objExists(exact_node):
                            found_nodes.append(exact_node)
                    
                    # 处理找到的节点
                    for node in found_nodes:
                        # 去掉名称空间前缀，只保留节点名
                        node_name = node.split(':')[-1] if ':' in node else node
                        if node_name not in found_groups:
                            found_groups.append(node_name)
                            
                else:
                    # 如果没有名称空间，直接在根级查找
                    found_nodes = cmds.ls(pattern, type='transform')
                    for node in found_nodes:
                        if node not in found_groups:
                            found_groups.append(node)
                
                # 将这个模式找到的组添加到总列表中
                for group in found_groups:
                    if group not in matchGrpList:
                        matchGrpList.append(group)
                
                lprint(u"[导出名称辅助] 模式 '{}' 找到组: {}".format(pattern, found_groups))
            
            # 如果没找到任何匹配的组，使用默认值
            if not matchGrpList:
                matchGrpList = [u'Geometry']
                lprint(u"[导出名称辅助] 未找到匹配组，使用默认值: {}".format(matchGrpList))
            else:
                lprint(u"[导出名称辅助] 最终匹配组列表: {}".format(matchGrpList))
            
            return matchGrpList
            
        except Exception as e:
            lprint(u"[导出名称辅助] 查找匹配组失败: {}".format(str(e)))
            return [u'Geometry']
    
    @thread_safe_ui_update
    def setup_timeline_range(self):
        """设置时间轴范围"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return
        
        try:
            min_frame = cmds.playbackOptions(query=True, min=True)
            max_frame = cmds.playbackOptions(query=True, max=True)
            
            self.main_window.ui.sf_wgt.setValue(min_frame - 3)
            self.main_window.ui.ef_wgt.setValue(max_frame + 3)
            
            lprint(u"[导出名称辅助] 时间轴范围已设置: {} - {}".format(min_frame-3, max_frame+3))
        except Exception as e:
            lprint(u"[导出名称辅助] 设置时间轴范围失败: {}".format(str(e)))
    
    def _on_namespace_changed(self, export_combo, namespace):
        """名称空间变化时更新导出名称"""
        self.set_export_name_for_combo(export_combo, namespace)
    
    def _on_select_group(self, row_index):
        """选择按钮点击事件"""
        if not self.main_window or not hasattr(self.main_window, 'selectExGroup'):
            return
        self.main_window.selectExGroup(row_index)
    
    @thread_safe_ui_update
    def update_export_names_in_grid(self):
        """更新Grid布局中所有行的导出名称"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            lprint(u"[导出名称辅助] 主窗口或UI不存在，无法更新Grid")
            return
        
        grid_layout = self.main_window.ui.exListGridLay
        if not grid_layout:
            lprint(u"[导出名称辅助] Grid布局不存在")
            return
        
        # 计算Grid中的行数：通过检查实际的widget数量
        max_row = 0
        for i in range(grid_layout.count()):
            item = grid_layout.itemAt(i)
            if item and item.widget():
                row, col, rowspan, colspan = grid_layout.getItemPosition(i)
                max_row = max(max_row, row)
        
        lprint(u"[导出名称辅助] 检测到Grid最大行数: {}".format(max_row))
        
        # 遍历Grid中的每一行（从第1行开始，第0行是标题）
        updated_count = 0
        for row in range(1, max_row + 1):
            try:
                lprint(locals())
                # 获取第1列（名称空间）的组合框
                namespace_widget = grid_layout.itemAtPosition(row, 1)
                export_name_widget = grid_layout.itemAtPosition(row, 3)
                
                namespace_combo = namespace_widget.widget()
                export_name_combo = export_name_widget.widget()
                namespace = namespace_combo.currentText()
                lprint(namespace,namespace_widget,namespace_combo,export_name_widget,export_name_combo,grid_layout.itemAtPosition(row, 0).widget().text())
                lprint(namespace_combo.count())
                for i in range(namespace_combo.count()):
                    lprint(namespace_combo.itemText(i))
                if namespace:  # 确保名称空间不为空
                    self.set_export_name_for_combo(export_name_combo, namespace)
                    updated_count += 1
                        
            except Exception as e:
                lprint(u"[导出名称辅助] 更新第{}行失败: {}".format(row, str(e)))
                continue
        
        lprint(u"[导出名称辅助] Grid导出名称更新完成，成功更新 {} 行".format(updated_count))


@singleton
class AutoFillHelper(object):
    """自动填充辅助类 - 根据Maya文件名自动填充项目信息 (单例)"""
    
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.data_center = None
    
    def set_data_center(self, data_center):
        """设置数据中心"""
        self.data_center = data_center
    
    def auto_fill_from_maya_filename(self):
        """从Maya文件名自动填充项目信息"""
        try:
            from l_scripts import L_GV
            maya_filename = L_GV.getMayaFileName()
            lprint(u"[自动填充] Maya文件名: {}".format(maya_filename))
            
            # 解析项目名称
            project_match = re.search(r'(^\w+?)_ep', maya_filename, flags=re.I)
            if project_match:
                project_name = project_match.group(1)
                lprint(u"[自动填充] 检测到项目: {}".format(project_name))
                
                # 设置数据中心的当前项目
                if self.data_center:
                    for project in self.data_center.project_list:
                        if project.project_name.upper() == project_name.upper():
                            self.data_center.current_project = project
                            break
            
            # 解析集场镜信息
            ep_match = re.search(r'(EP\w+?)_', maya_filename, flags=re.I)
            sc_match = re.search(r'(sc\d+)_', maya_filename, flags=re.I)
            shot_match = re.search(r'_(shot[0-9a-z]+?)[\._]+', maya_filename, flags=re.I)
            
            if self.data_center:
                if ep_match:

                    episode_name = ep_match.group(1)
                    self.data_center.current_episode_name = episode_name
                    lprint(u"[自动填充] 检测到集: {}".format(episode_name))
                
                if sc_match:
                    sequence_name = sc_match.group(1)
                    self.data_center.current_sequence_name = sequence_name
                    lprint(u"[自动填充] 检测到场: {}".format(sequence_name))
                
                if shot_match:
                    shot_name = shot_match.group(1)
                    lprint(u"[自动填充] 检测到镜头: {}".format(shot_name))
                    
                    # 查找并设置对应的镜头
                    if self.data_center.current_episode_name and self.data_center.current_sequence_name:
                        shots = self.data_center.get_shots_by_episode_sequence(
                            self.data_center.current_episode_name,
                            self.data_center.current_sequence_name
                        )
                        for shot in shots:
                            if shot.shot_name == shot_name:
                                self.data_center.current_shot = shot
                                break
            
            return True
            
        except Exception as e:
            lprint(u"[自动填充] 自动填充失败: {}".format(str(e)))
            return False
    
    def guess_shot_from_maya_filename(self):
        """从Maya文件名猜测镜头信息并填充UI"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return False
        
        try:
            from l_scripts import L_GV
            maya_filename = L_GV.getMayaFileName()
            lprint(u"[自动填充] 从Maya文件名猜测镜头信息: {}".format(maya_filename))
            
            ui = self.main_window.ui
            qttool = getattr(self.main_window, 'qttool', None)
            if not qttool:
                lprint(u"[自动填充] 警告: qttool未找到")
                return False
            
            # # 解析项目名称
            # project_match = re.search(r'(^\w+?)_(ep|pv)', maya_filename, flags=re.I)
            # if project_match:
            #     project_name = project_match.group(1)
            #     qttool.set_combobox_text(ui.projectCombo, project_name)
            #     lprint(u"[自动填充] 检测到项目: {}".format(project_name))
                
            #     # 通过数据中心设置项目
            #     if self.data_center:
            #         for project in self.data_center.project_list:
            #             if project == project_name:
            #                 self.data_center.current_project = project
            #                 break
            
            # 解析集信息
            
            ep_match = re.search(r'(EP\d+|PV\d+)_', maya_filename, flags=re.I)
            if ep_match:
                episode_name = ep_match.group(1)
                qttool.set_combobox_text(ui.epCombo, episode_name)
                lprint(u"[自动填充] 检测到集: {}".format(episode_name))
                
                # 通过数据中心设置当前集
                if self.data_center:
                    self.data_center.current_episode_name = episode_name
            
            # 解析场信息
            sc_match = re.search(r'(sc\d+)_', maya_filename, flags=re.I)
            if sc_match:
                sequence_name = sc_match.group(1)
                qttool.set_combobox_text(ui.scCombo, sequence_name)
                lprint(u"[自动填充] 检测到场: {}".format(sequence_name))
                
                # 通过数据中心设置当前场
                if self.data_center:
                    self.data_center.current_sequence_name = sequence_name
            
            # 解析镜头信息
            shot_match = re.search(r'_(shot[0-9a-z]+?)[\._]+', maya_filename, flags=re.I)
            if shot_match:
                shot_name = shot_match.group(1)
                qttool.set_combobox_text(ui.shotCombo, shot_name)
                lprint(u"[自动填充] 检测到镜头: {}".format(shot_name))
                
                # 通过数据中心设置当前镜头
                if self.data_center:
                    self.data_center.current_shot_name = shot_name
            
            # 更新实际目录
            if hasattr(self.main_window, 'getActuralDir'):
                self.main_window.getActuralDir()
            
            lprint(u"[自动填充] 镜头信息猜测完成！")
            return True
            
        except Exception as e:
            lprint(u"[自动填充] 猜测镜头信息失败: {}".format(str(e)))
            return False
    
    def get_project_name_from_maya_file(self):
        """从Maya文件名获取项目名称"""
        try:
            from l_scripts import L_GV
            maya_filename = L_GV.getMayaFileName()
            project_match = re.search(r'(^\w+?)_ep', maya_filename, flags=re.I)
            if project_match:
                return project_match.group(1)
            else:
                return ''
        except Exception as e:
            lprint(u"[自动填充] 获取项目名称失败: {}".format(str(e)))
            return ''
    
    def get_shot_entire_name_from_maya_file(self):
        """从Maya文件名获取完整镜头名称"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return ''
        
        try:
            from l_scripts import L_GV
            maya_filename = L_GV.getMayaFileName()
            
            # 解析各部分信息
            ep_match = re.search(r'(EP\w+?)_', maya_filename, flags=re.I)
            sc_match = re.search(r'(sc\d+)_', maya_filename, flags=re.I)
            shot_match = re.search(r'_(shot[0-9a-z]+?)[\._]+', maya_filename, flags=re.I)
            
            ui = self.main_window.ui
            qttool = getattr(self.main_window, 'qttool', None)
            
            # 更新UI组合框
            if ep_match and qttool:
                qttool.set_combobox_text(ui.epCombo, ep_match.group(1))
            if sc_match and qttool:
                qttool.set_combobox_text(ui.scCombo, sc_match.group(1))
            if shot_match and qttool:
                qttool.set_combobox_text(ui.shotCombo, shot_match.group(1))
            
            # 拼接结果
            result = '_'.join([
                ui.epCombo.currentText(),
                ui.scCombo.currentText(),
                ui.shotCombo.currentText()
            ])
            result = result.replace(u'未设置', '').replace(u'__', '_')
            return result
            
        except Exception as e:
            lprint(u"[自动填充] 获取完整镜头名称失败: {}".format(str(e)))
            return ''
    
    def update_actual_directory(self):
        """更新实际目录路径"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return
        
        try:
            ui = self.main_window.ui
            qttool = getattr(self.main_window, 'qttool', None)
            if not qttool:
                return
            
            shot_entire_name = self.get_shot_entire_name_from_maya_file()
            ex_dir = ui.exDirWgt.currentText()
            project_name = ui.projectCombo.currentText()
            
            actual_dir = '/'.join([ex_dir, project_name, shot_entire_name, 'abc_sim'])
            actual_dir = os.path.normpath(actual_dir)
            actual_dir = actual_dir.replace('\\_\\', '\\')
            
            qttool.set_combobox_text(ui.actualDirWgt, actual_dir)
            lprint(u"[自动填充] 实际目录已更新: {}".format(actual_dir))
            
        except Exception as e:
            lprint(u"[自动填充] 更新实际目录失败: {}".format(str(e)))


@singleton
class RefreshHelper(object):
    """刷新辅助类 - 处理UI刷新和项目设置 (单例)"""
    
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.auto_fill_helper = None
        self.export_name_helper = None
        self.data_center = None
    
    def set_helpers(self, auto_fill_helper, export_name_helper, data_center):
        """设置其他辅助类的引用"""
        self.auto_fill_helper = auto_fill_helper
        self.export_name_helper = export_name_helper
        self.data_center = data_center
    
    def refresh_project_setting(self):
        """刷新项目设置"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return
        
        try:
            qttool = getattr(self.main_window, 'qttool', None)
            if not qttool:
                return
            
            # 获取项目名称
            project_name = ""
            if self.auto_fill_helper:
                project_name = self.auto_fill_helper.get_project_name_from_maya_file()
            
            if project_name:
                qttool.set_combobox_text(self.main_window.ui.projectCombo, project_name)
                lprint(u"[刷新助手] 项目已设置为: {}".format(project_name))
            else:
                project_name = "Test"
                lprint(u"[刷新助手] 使用默认项目: {}".format(project_name))
        
        except Exception as e:
            lprint(u"[刷新助手] 刷新项目设置失败: {}".format(str(e)))
    
    def perform_full_refresh(self):
        """执行完整刷新流程"""
        try:
            # 1. 设置项目
            self.refresh_project_setting()
            
            # 2. 使用数据中心主导刷新数据
            if self.data_center:
                self.data_center.refresh_all_data()
            
            # 3. 更新实际目录
            if self.auto_fill_helper:
                self.auto_fill_helper.update_actual_directory()
            
            # 4. 使用ExportNameHelper处理UI填充
            if self.export_name_helper:
                # 设置时间轴范围
                self.export_name_helper.setup_timeline_range()
                # 填充Grid布局
                self.export_name_helper.populate_grid_layout()
                # 更新Grid中的导出名称
                self.export_name_helper.update_export_names_in_grid()
            
            lprint(u"[刷新助手] 完整刷新流程完成")
        
        except Exception as e:
            lprint(u"[刷新助手] 完整刷新失败: {}".format(str(e)))
    
    def select_export_group(self, row_index):
        """选择导出组"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return
        
        try:
            grid_layout = self.main_window.ui.exListGridLay
            
            # 获取选择对象
            sel_obj = grid_layout.itemAtPosition(row_index, 0).widget().text()
            namespace = sel_obj.split(':')[0] if ':' in sel_obj else ''
            
            # 获取组列表字符串
            group_list_widget = grid_layout.itemAtPosition(row_index, 2).widget()
            if not group_list_widget:
                return
            
            group_list_str = group_list_widget.text()
            if not group_list_str:
                return
            
            # 解析并构建选择列表
            sel_node_list = eval(group_list_str)
            if namespace:
                sel_node_list = [':'.join([namespace, x]) for x in sel_node_list]
            
            if not sel_node_list:
                sel_node_list = [sel_obj]
            
            # 在Maya中选择
            cmds.select(sel_node_list)
            lprint(u"[刷新助手] 已选择导出组: {}".format(sel_node_list))
        
        except Exception as e:
            lprint(u"[刷新助手] 选择导出组失败: {}".format(str(e)))


@singleton
class FileOperationHelper(object):
    """文件操作辅助类 - 处理文件对话框和目录操作 (单例)"""
    
    def __init__(self, main_window=None):
        self.main_window = main_window
    
    def browse_json_file(self):
        """浏览JSON预设文件"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return
        
        try:
            from PySide2.QtWidgets import QFileDialog
            
            current_path = self.main_window.ui.jsonPreset_Combo.currentText() or "A:/temp/MayaToUE/ExHis"
            
            file_path, _ = QFileDialog.getOpenFileName(
                self.main_window, 
                u"选择JSON预设文件", 
                current_path,
                "JSON Files (*.json);;All Files (*)"
            )
            
            if file_path:
                qttool = getattr(self.main_window, 'qttool', None)
                if qttool:
                    qttool.set_combobox_text(self.main_window.ui.jsonPreset_Combo, file_path)
                    lprint(u"[文件操作] 已选择JSON预设文件: {}".format(file_path))
        
        except Exception as e:
            lprint(u"[文件操作] 浏览JSON文件失败: {}".format(str(e)))
    
    def open_preset_directory(self):
        """打开预设文件所在目录"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return
        
        try:
            preset_file = self.main_window.ui.jsonPreset_Combo.currentText()
            if preset_file and os.path.exists(preset_file):
                preset_dir = os.path.dirname(preset_file)
                os.startfile(preset_dir)
                lprint(u"[文件操作] 已打开预设文件目录: {}".format(preset_dir))
            else:
                lprint(u"[文件操作] 预设文件路径不存在或为空")
        
        except Exception as e:
            lprint(u"[文件操作] 打开预设文件目录失败: {}".format(str(e)))
    
    def open_actual_directory(self):
        """打开实际导出目录"""
        if not self.main_window or not hasattr(self.main_window, 'ui'):
            return
        
        try:
            actual_dir = self.main_window.ui.actualDirWgt.currentText()
            if not os.path.exists(actual_dir):
                os.makedirs(actual_dir)
                lprint(u"[文件操作] 已创建目录: {}".format(actual_dir))
            
            os.startfile(actual_dir)
            lprint(u"[文件操作] 已打开实际目录: {}".format(actual_dir))
        
        except Exception as e:
            lprint(u"[文件操作] 打开实际目录失败: {}".format(str(e)))


@singleton
class MainWindowHelper(object):
    """主窗口助手类 - 数据驱动UI架构，UI助手只响应数据变化 (单例)"""
    
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.data_center = None
        

        
        # 创建各个助手 - 但不创建数据中心
        self.project_helper = None
        self.shot_helper = None
        self.episode_helper = None
        self.sequence_helper = None
        self.auto_fill_helper = AutoFillHelper(main_window)
        self.export_name_helper = ExportNameHelper(main_window)
        self.file_operation_helper = FileOperationHelper(main_window)
        self.refresh_helper = RefreshHelper(main_window)
        
        lprint(u"[主窗口助手] 单例初始化完成，等待数据中心驱动")
    

    
    def initial_ui_fill(self):
        """初始化UI填充 - 无JSON数据的基础UI填充"""
        try:
            if self.export_name_helper:
                # 设置时间轴范围
                self.export_name_helper.setup_timeline_range()
                lprint(u"[主窗口助手] 时间轴范围已初始化")
                
                # 填充Grid布局
                self.export_name_helper.populate_grid_layout()
                lprint(u"[主窗口助手] Grid布局已填充")
            
            lprint(u"[主窗口助手] 初始化UI填充完成")
        except Exception as e:
            lprint(u"[主窗口助手] 初始化UI填充失败: {}".format(str(e)))
    
    def register_to_data_center(self, data_center):
        """注册到数据中心 - 让数据中心驱动UI更新"""
        try:
            self.data_center = data_center
            
            # 获取UI控件
            if self.main_window and hasattr(self.main_window, 'ui'):
                ui = self.main_window.ui
                
                # 创建项目助手并注册到数据中心
                if hasattr(ui, 'projectCombo'):
                    project_helper = ProjectHelper(self.main_window, ui.projectCombo)
                    project_helper.data_center = data_center
                    self.project_helper = project_helper
                    lprint(u"[主窗口助手] 项目助手已注册到数据中心")
                
                # 创建镜头助手并注册到数据中心
                ep_combo = getattr(ui, 'epCombo', None)
                sc_combo = getattr(ui, 'scCombo', None)
                shot_combo = getattr(ui, 'shotCombo', None)
                
                if ep_combo or sc_combo or shot_combo:
                    shot_helper = ShotHelper(self.main_window, ep_combo, sc_combo, shot_combo)
                    shot_helper.set_data_center(data_center)
                    self.shot_helper = shot_helper
                    # 为了兼容data_center的调用，设置别名
                    self.episode_helper = shot_helper
                    self.sequence_helper = shot_helper
                    lprint(u"[主窗口助手] 镜头助手已注册到数据中心")
                
                # 自动填充助手也注册到数据中心
                self.auto_fill_helper.set_data_center(data_center)
                
                # 设置RefreshHelper的引用
                self.refresh_helper.set_helpers(self.auto_fill_helper, self.export_name_helper, data_center)
                
                lprint(u"[主窗口助手] 所有UI助手已注册到数据中心，等待数据驱动")
            
        except Exception as e:
            traceback.print_exc()
            lprint(u"[主窗口助手] 注册UI助手失败: {}".format(str(e)))
    
    def get_current_shot_info(self):
        """获取当前镜头信息 - 通过主窗口的数据中心获取"""
        if self.data_center:
            current_shot = self.data_center.get_current_shot_info()
            if current_shot:
                return {
                    'project': self.data_center.current_project,
                    'episode': current_shot['episode'],
                    'sequence': current_shot['sequence'],
                    'shot_name': current_shot['shot_name'],
                    'shot_url': current_shot['shot_url'],
                    'shot_path': current_shot['shot_path']
                }
        return None
