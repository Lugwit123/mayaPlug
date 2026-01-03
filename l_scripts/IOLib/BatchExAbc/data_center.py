# -*- coding: utf-8 -*-
"""
数据中心模块 - Python 2.7兼容版本
用于从文件系统读取项目数据并驱动UI更新
参考assemble_step/ui_helpers/data_center.py的设计模式
"""

import os
import sys
import json
import codecs
import logging
import traceback
from collections import defaultdict
from Lugwit_Module import lprint
import re
import Lugwit_Module as LM




# Qt线程导入 - 使用PySide2进行异步数据加载
from PySide2.QtCore import QThread, Signal as pyqtSignal, QObject
try:
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from ui_helper import MainWindowHelper
except:
    pass


# 简单的配置管理函数
def get_config_manager():
    """简单的配置管理器"""
    class SimpleConfig:
        def __init__(self):
            self._project_short_names = {}
            self._load_project_info()
        
        def _load_project_info(self):
            """加载项目信息配置"""
            try:
                config_dir = os.path.dirname(os.path.abspath(__file__))
                config_file = os.path.join(config_dir, "config", "project_info.json")
                
                if os.path.exists(config_file):
                    with codecs.open(config_file, 'r', encoding='utf-8') as f:
                        project_info = json.load(f)
                        self._project_short_names = project_info.get("project_short_names", {})
                        lprint(u"加载项目简称映射: {}".format(self._project_short_names))
                else:
                    lprint(u"项目信息配置文件不存在: {}".format(config_file))
            except Exception as e:
                lprint(u"加载项目信息配置失败: {}".format(str(e)))
        
        def get_project_short_name(self, project_name):
            """获取项目简称"""
            return self._project_short_names.get(project_name, project_name)
        
        def get_root_path(self):
            return "G:/"
        def get_project_path(self, project_name):
            return "G:/{}".format(project_name)
        def get_shots_path(self, project_name):
            return "G:/{}/Shot".format(project_name)
        def get_assets_path(self, project_name):
            return "G:/{}/Asset".format(project_name)
        def get_shot_path(self, project_name, episode, sequence, shot_name):
            return "G:/{}/Shot/{}/{}/{}".format(project_name, episode, sequence, shot_name)
        def get_asset_path(self, project_name, asset_type, asset_name):
            return "G:/{}/Asset/{}/{}".format(project_name, asset_type, asset_name)
        def get_preset_js_path(self, project_name, episode, sequence, shot):
            # 使用项目简称
            project_short_name = self.get_project_short_name(project_name)
            common_ExHisFileDir = "{}/Temp/MayaToUE/ExHis/{}/all_exCfg_file".format(
                LM.Lugwit_publicDisc, project_name).replace("\\", "/")
            return u"{}/exAniClip_{}_{}_{}_{}_*.json".format(
                common_ExHisFileDir, project_short_name,episode, sequence, shot).replace("\\", "/").replace("//", "/")
    return SimpleConfig()

# 可索引的集合类
class IndexableSet(set):
    """继承自set的可索引集合，支持[0]索引访问"""
    
    def __getitem__(self, index):
        """支持索引访问"""
        if isinstance(index, int):
            if index < 0 or index >= len(self):
                raise IndexError("IndexableSet index out of range")
            return list(self)[index]
        else:
            raise TypeError("IndexableSet indices must be integers")
    
    def first(self):
        """获取第一个元素"""
        if len(self) == 0:
            return None
        return self[0]
    
    def sorted_list(self):
        """返回排序后的列表"""
        return sorted(list(self))
    
    def __str__(self):
        """字符串表示，显示为排序后的列表"""
        return str(self.sorted_list())
    
    def __repr__(self):
        """详细字符串表示"""
        return "IndexableSet({})".format(self.sorted_list())

# 简单的工具类
class FileUtils:
    @staticmethod
    def find_files(directory, pattern="*", recursive=True):
        import glob
        import os
        if recursive:
            return glob.glob(os.path.join(directory, "**", pattern), recursive=True)
        else:
            return glob.glob(os.path.join(directory, pattern))

class JSONUtils:
    @staticmethod
    def load_json(file_path, default=None):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except:
            return default

class PathUtils:
    @staticmethod
    def normalize_path(path):
        return os.path.normpath(path).replace('\\', '/')

# ==================== 异步镜头数据加载线程 ====================

class ShotsDataLoader(QThread):
    """镜头数据异步加载线程 - 只加载镜头数据"""
    
    # 信号定义
    shots_loaded = pyqtSignal(list)  # 镜头数据加载完成
    loading_progress = pyqtSignal(str)  # 加载进度
    loading_finished = pyqtSignal()  # 加载完成
    loading_error = pyqtSignal(str)  # 加载错误
        
    def __init__(self, data_center, project_name):
        super(ShotsDataLoader, self).__init__()
        self.data_center = data_center
        self.project_name = project_name
        self._is_cancelled = False
    
    def cancel(self):
        """取消加载"""
        self._is_cancelled = True
    
    def run(self):
        """在子线程中执行镜头数据加载"""
        if self._is_cancelled:
            return
        
        lprint(u"[异步加载] 开始加载镜头数据: {}".format(self.project_name))
        
        # 加载镜头数据
        self.loading_progress.emit(u"正在加载镜头数据...")
        shots = self._load_shots_in_thread()
        
        if self._is_cancelled:
            return
        
        self.shots_loaded.emit(shots)
        
        lprint(u"[异步加载] 镜头数据加载完成")
        self.loading_finished.emit()
    
    def _load_shots_in_thread(self):
        """在子线程中加载镜头数据"""
        if not self.project_name:
            return []
        
        shots = []
        config_manager = self.data_center.config_manager
        shots_path = config_manager.get_shots_path(self.project_name)
        
        if not os.path.exists(shots_path):
            return []
        lprint(u"异步加载数据从",self.project_name,shots_path)
        # 快速扫描：只扫描文件夹结构
        for episode_dir in os.listdir(shots_path):
            if self._is_cancelled:
                break
            if not re.search("^[EP]",episode_dir):
                continue
            episode_path = os.path.join(shots_path, episode_dir)
            if not os.path.isdir(episode_path):
                continue
            # lprint(episode_dir,os.listdir(episode_path))
            for sequence_dir in os.listdir(episode_path):
                if self._is_cancelled:
                    break

                if sequence_dir.lower()=='sc00':
                    continue      
                sequence_path = os.path.join(episode_path, sequence_dir)
                if not os.path.isdir(sequence_path):
                    continue
                
                for shot_dir in os.listdir(sequence_path):
                    if self._is_cancelled:
                        break
                    if not re.search("^Shot",shot_dir,flags=re.I):
                        continue    
                    shot_path = os.path.join(sequence_path, shot_dir)
                    if not os.path.isdir(shot_path):
                        continue
                    
                    # 创建镜头字典（简化版本）
                    shot = {
                        'episode': episode_dir,
                        'sequence': sequence_dir,
                        'shot_name': shot_dir,
                        'project_name': self.project_name,
                        'shot_url': "{}/{}/{}".format(episode_dir, sequence_dir, shot_dir),
                        'shot_path': shot_path
                    }
                    shots.append(shot)
        lprint(shots[:3],len(shots))
        # 快速排序
        return self.data_center._sort_shots(shots)
    



class DataCenter(QObject):
    """
    数据中心 - 用于管理项目数据并驱动UI更新
    
    主要功能：
    1. 从文件系统读取项目、镜头数据
    2. 使用PySide2 QThread异步加载，避免UI卡顿
    3. 提供数据属性，支持自动UI更新
    4. 管理当前集、场、镜选择状态
    """
    

    
    def __init__(self, main_window=None):
        """
        初始化数据中心
        
        Args:
            main_window: 主窗口实例，用于UI更新回调
        """
        super(DataCenter, self).__init__()
        self.main_window = main_window
        
        # 配置管理器
        self.config_manager = get_config_manager()
        
        # 项目数据
        self._current_project = ""
        self._project_list = []  # 项目代码列表
        
        # 镜头数据
        self._current_pro_shots_list = []  # 当前项目的镜头列表
        
        # 当前选择状态
        self._current_episode_name = ""  # 当前选中的集名称
        self._current_sequence_name = ""  # 当前选中的场名称
        self._current_shot_name = ""  # 当前选中的镜头名称
        
        # 列表数据
        self._current_episode_list = IndexableSet()  # 当前项目的集列表
        self._current_sequence_list = IndexableSet()  # 当前选中集的场列表
        self._current_shot_list = IndexableSet()  # 当前选中集场的镜头列表
        self._current_preset_list = []  # 当前镜头的预设文件列表
        self._current_preset_file = ""  # 当前选中的预设文件路径
        
        # 数据根路径配置
        self.data_root_path = self.config_manager.get_root_path()
        
        # UI助手引用 - 数据中心主导
        self.ui_helper = None
        try:
            self.ui_helper = MainWindowHelper()
        except:
            pass
        # 异步加载相关
        self._current_loader = None  # 当前的镜头数据加载线程
        
        lprint(u"数据中心初始化完成，异步镜头加载已启用")
    

    
    def initialize_data(self):
        """初始化数据 - 数据中心主导的数据加载"""
        try:
            lprint(u"[数据中心] 开始主导数据初始化")
            
            # 1. 加载项目列表
            self.load_projects_from_filesystem()
            
            # 2. 自动填充Maya文件信息
            # if self.ui_helper and self.ui_helper.auto_fill_helper:
            #     self.ui_helper.auto_fill_helper.auto_fill_from_maya_filename()
            
            lprint(u"[数据中心] 数据初始化完成")
            
        except Exception as e:
            lprint(u"[数据中心] 数据初始化失败: {}".format(str(e)))
    
    def refresh_all_data(self):
        """刷新所有数据 - 数据中心主导"""
        try:
            lprint(u"[数据中心] 开始刷新所有数据")
            self.initialize_data()
            
        except Exception as e:
            lprint(u"[数据中心] 刷新数据失败: {}".format(str(e)))
    
    # ==================== 属性定义 ====================
    
    @property
    def current_project(self):
        """当前项目代码"""
        return self._current_project
    
    @current_project.setter
    def current_project(self, project_name):
        """设置当前项目，异步加载数据避免UI卡顿"""
        if self._current_project != project_name:
            lprint(u"项目切换: {}".format(project_name))
            
            # 取消之前的加载任务
            self._cancel_current_loading()
            
            self._current_project = project_name
            
            if project_name:
                # 异步加载镜头数据
                self._start_async_shots_loading(project_name)

    
    @property
    def project_list(self):
        """项目列表"""
        return self._project_list
    
    @project_list.setter
    def project_list(self, projects):
        """设置项目列表 - 数据中心主导UI更新"""
        self._project_list = projects
        lprint(u"[数据中心] 项目列表已更新: {} 个项目".format(len(projects)))
        
        # 数据中心主导：自动驱动UI更新
        self.ui_helper.project_helper.update_project_list(projects)
        self.current_project = projects[0]
        # self._drive_project_list_ui_update(projects)
    
    @property
    def current_pro_shots_list(self):
        """当前项目的镜头列表"""
        return self._current_pro_shots_list
    
    @current_pro_shots_list.setter
    def current_pro_shots_list(self, shots_list):
        """设置镜头列表，自动更新集场列表"""
        self._current_pro_shots_list = shots_list
        
        # 自动提取集列表并设置，会自动触发UI更新
        episodes = IndexableSet()
        for shot in shots_list:
            episodes.add(shot['episode'])
        self.current_episode_list = episodes
        

    @property
    def current_episode_list(self):
        """当前项目的集列表"""
        return self._current_episode_list
    
    @current_episode_list.setter
    def current_episode_list(self, episodes):
        """设置集列表并直接更新UI"""
        self._current_episode_list = episodes
        
        # 直接调用ui_helper更新集下拉框
        lprint("更新集列表为",episodes)
        self.ui_helper.episode_helper.update_episode_list(episodes) # ignore
        
        # 如果当前没有选中集，自动选择第一个
        self.current_episode_name = self._current_episode_list[0]
    
    @property
    def current_sequence_list(self):
        """当前选中集的场列表"""
        return self._current_sequence_list
    
    @current_sequence_list.setter
    def current_sequence_list(self, sequences):
        """设置场列表并直接更新UI"""
        self._current_sequence_list = sorted(sequences)
        #filtered_shots = (filtered_shots)
        # 直接调用ui_helper更新场下拉框
        self.ui_helper.sequence_helper.update_sequence_list(sequences)
        
        self.current_sequence_name = self._current_sequence_list[0]
    
    @property
    def current_shot_list(self):
        """当前选中集场的镜头列表"""
        return self._current_shot_list
    
    @current_shot_list.setter
    def current_shot_list(self, shots_data):
        """设置镜头列表并直接更新UI"""
        # 过滤为当前集和当前场的镜头
        filtered_shots = IndexableSet()
        for shot in shots_data:
            if shot['episode'] == self._current_episode_name and shot['sequence'] == self._current_sequence_name:
                filtered_shots.add(shot['shot_name'])
        filtered_shots = sorted(filtered_shots)
        self._current_shot_list = filtered_shots
        lprint("更新镜为", filtered_shots[:3])
        
        # 直接调用ui_helper更新镜头下拉框
        self.ui_helper.shot_helper.update_shot_list(self._current_shot_list)
        
        # 如果当前没有选中镜头，自动选择第一个
        if self._current_shot_list:
            self.current_shot_name = self._current_shot_list[0]
    
    @property
    def current_episode_name(self):
        """当前选中的集名称"""
        return self._current_episode_name
    
    @current_episode_name.setter
    def current_episode_name(self, episode_name):
        """设置当前集，直接更新UI和场列表"""
        lprint(u"集切换: {}".format(episode_name))
        self._current_episode_name = episode_name
        
        # 直接更新UI中的集选择
        self.ui_helper.episode_helper.set_current_episode(episode_name)
        
        # 获取当前集的场列表并设置，会自动触发UI更新
        sequences = IndexableSet()
        lprint(self._current_pro_shots_list[:3],len(self._current_pro_shots_list))
        for shot in self._current_pro_shots_list:
            if shot['episode'] == self._current_episode_name:
                sequences.add(shot['sequence'])
        lprint("更新场为",sequences)
        self.current_sequence_list = sequences
    
    @property
    def current_sequence_name(self):
        """当前选中的场名称"""
        return self._current_sequence_name
    
    @current_sequence_name.setter
    def current_sequence_name(self, sequence_name):
        """设置当前场，直接更新UI和镜头列表"""
        lprint(u"场切换: {}".format(sequence_name))
        self._current_sequence_name = sequence_name
        
        # 直接更新UI中的场选择
        self.ui_helper.sequence_helper.set_current_sequence(sequence_name)
        
        # 获取当前集场的镜头列表并设置，会自动触发UI更新
        # 传递所有镜头数据，过滤逻辑移动到 current_shot_list setter 中
        self.current_shot_list = self._current_pro_shots_list
    
    @property
    def current_shot_name(self):
        """当前选中的镜头名称"""
        return self._current_shot_name
    
    @current_shot_name.setter
    def current_shot_name(self, shot_name):
        """设置当前镜头，直接更新UI"""
        lprint(u"镜头切换: {}".format(shot_name))
        self._current_shot_name = shot_name
        
        # 直接更新UI中的镜头选择
        if self.ui_helper and hasattr(self.ui_helper, 'shot_helper'):
            self.ui_helper.shot_helper.set_current_shot(shot_name)
        
        # 更新预设文件列表
        import glob

        search_pattern = self.config_manager.get_preset_js_path(
            self._current_project, self._current_episode_name, 
            self._current_sequence_name, self._current_shot_name)
        preset_files = glob.glob(search_pattern)
        lprint(search_pattern,preset_files,self._current_episode_name)
        if preset_files:
            preset_files.sort()
        self.current_preset_list = preset_files
        self.ui_helper.shot_helper.update_actual_dir()
    
    @property
    def current_preset_list(self):
        """当前镜头的预设文件列表"""
        return self._current_preset_list
    
    @current_preset_list.setter
    def current_preset_list(self, preset_list):
        """设置预设文件列表并更新UI"""
        lprint(preset_list)
        self._current_preset_list = sorted(preset_list)
        self.ui_helper.shot_helper.update_preset_list(preset_list)
    
    @property
    def current_preset_file(self):
        """当前选中的预设文件路径"""
        return self._current_preset_file
    
    @current_preset_file.setter
    def current_preset_file(self, preset_file_path):
        """设置当前预设文件并更新相关数据"""
        if self._current_preset_file != preset_file_path:
            lprint(u"[数据中心] 预设文件切换: {}".format(preset_file_path))
            self._current_preset_file = preset_file_path
            
            # 通过ExportNameHelper更新UI和数据
            self.ui_helper.export_name_helper.load_preset_json(preset_file_path)
            self.ui_helper.export_name_helper.update_export_names_in_grid()
    

    # ==================== 数据加载方法 ====================
    
    def load_projects_from_filesystem(self):
        """从文件系统扫描并加载项目列表"""
        lprint(u"开始从文件系统扫描项目...")
        
        projects = []
        
        try:
            root_path = str(self.data_root_path)
            if not os.path.exists(root_path):
                lprint(u"数据根路径不存在: {}".format(root_path))
                return projects
            
            # 扫描根路径下的项目文件夹
            items = os.listdir(root_path)
            for item in items:
                project_path = self.config_manager.get_project_path(item)
                
                # 检查是否为项目文件夹（包含Shot和Asset子文件夹）
                if (os.path.isdir(project_path) and 
                    os.path.exists(self.config_manager.get_shots_path(item)) and
                    os.path.exists(self.config_manager.get_assets_path(item))):
                    
                    projects.append(item)  # 只保存项目代码字符串
                    
            lprint(u"扫描完成，找到 {} 个项目".format(len(projects)))
            self.project_list = projects
                
        except Exception as e:
            lprint(u"扫描项目时出错: {}".format(str(e)))
            traceback.print_exc()
            
        return projects
    
    def _sort_shots(self, shots_list):
        """对镜头列表进行排序"""
        try:
            import re
            
            def sort_key(shot):
                # 提取集、场、镜头的数字部分进行排序
                ep_num = 999
                seq_num = 999
                shot_num = 999
                
                ep_match = re.search(r'(\d+)', shot['episode'])
                if ep_match:
                    ep_num = int(ep_match.group(1))
                
                seq_match = re.search(r'(\d+)', shot['sequence'])
                if seq_match:
                    seq_num = int(seq_match.group(1))
                
                shot_match = re.search(r'(\d+)', shot['shot_name'])
                if shot_match:
                    shot_num = int(shot_match.group(1))
                
                return (ep_num, seq_num, shot_num, shot['shot_name'])
            
            return sorted(shots_list, key=sort_key)
            
        except Exception as e:
            lprint(u"镜头排序失败: {}".format(str(e)))
            return shots_list
    


    

    
    # ==================== 查询方法 ====================
    
    def get_shots_by_episode_sequence(self, episode_name, sequence_name):
        """获取指定集场下的镜头列表"""
        shots = []
        for shot in self._current_pro_shots_list:
            if shot['episode'] == episode_name and shot['sequence'] == sequence_name:
                shots.append(shot)
        return shots
    
    def get_shot_by_url(self, shot_url):
        """根据镜头URL查找镜头数据"""
        for shot in self._current_pro_shots_list:
            if shot['shot_url'] == shot_url:
                return shot
        return None
    
    def get_current_shot_info(self):
        """获取当前镜头信息"""
        if self._current_shot_name:
            for shot in self._current_pro_shots_list:
                if (shot['episode'] == self._current_episode_name and
                    shot['sequence'] == self._current_sequence_name and
                    shot['shot_name'] == self._current_shot_name):
                    return shot
        return None
    
    # ==================== 异步数据加载管理方法 ====================
    
    def _cancel_current_loading(self):
        """取消当前的镜头数据加载任务"""
        if self._current_loader and self._current_loader.isRunning():
            lprint(u"[异步加载] 取消当前镜头加载任务")
            self._current_loader.cancel()
            self._current_loader.wait(1000)  # 等待最多1秒
            if self._current_loader.isRunning():
                self._current_loader.terminate()
        self._current_loader = None
    
    def _start_async_shots_loading(self, project_name):
        """开始异步加载镜头数据"""
        lprint(u"[异步加载] 开始异步加载镜头: {}".format(project_name))
        
        # 创建新的镜头加载线程
        self._current_loader = ShotsDataLoader(self, project_name)
        
        # 连接信号
        self._current_loader.shots_loaded.connect(self._on_shots_loaded)
        # self._current_loader.loading_finished.connect(self._on_loading_finished)
        self._current_loader.loading_error.connect(self._on_loading_error)
        
        # 启动线程
        self._current_loader.start()
    
    def _on_shots_loaded(self, shots_list):
        """镜头数据加载完成的回调"""
        lprint(u"[异步加载] 镜头数据加载完成: {} 个镜头".format(len(shots_list)))
        self.current_pro_shots_list = shots_list
    
    def _on_loading_finished(self):
        """加载完成回调"""
        lprint(u"[异步加载] 镜头数据加载完成")
        self._current_loader = None
    
    def _on_loading_error(self, error_message):
        """加载错误回调"""
        lprint(u"[异步加载] 加载错误: {}".format(error_message))
        self._current_loader = None
    
    # ==================== 数据中心驱动UI更新方法 ====================
    

    
    # ==================== 工具方法 ====================
    
    def refresh_current_project_data(self):
        """刷新当前项目的所有数据"""
        if self._current_project:
            lprint(u"刷新当前项目数据: {}".format(self._current_project))
            self._start_async_shots_loading(self._current_project)

    
    def get_data_summary(self):
        """获取数据摘要"""
        return {
            'current_project': self._current_project,
            'project_count': len(self._project_list),
            'shots_count': len(self._current_pro_shots_list),
            'episodes_count': len(self._current_episode_list),
            'sequences_count': len(self._current_sequence_list),
            'shot_list_count': len(self._current_shot_list),
            'current_episode': self._current_episode_name,
            'current_sequence': self._current_sequence_name,
            'current_shot': self._current_shot_name,
            'current_preset_file': self._current_preset_file
        }
    


# ==================== 使用示例 ====================

def create_data_center_example():
    """创建数据中心使用示例"""
    
    # 创建数据中心实例
    data_center = DataCenter()
    
    # 现在使用属性驱动，不需要复杂的信号连接
    
    # 加载项目列表
    projects = data_center.load_projects_from_filesystem()
    
    # 设置当前项目（会自动触发数据加载）
    if projects:
        data_center.current_project = projects[0]
        
        # 等待异步加载完成后设置选择
        # 在实际使用中，这些会通过信号回调自动设置
    
    # 打印数据摘要
    summary = data_center.get_data_summary()
    lprint(u"数据摘要: {}".format(summary))
    
    return data_center


if __name__ == "__main__":
    # 运行示例
    dc = create_data_center_example()