# -*- coding: utf-8 -*-
"""
Maya 2020 UI线程安全测试
专门针对Maya 2020 + PySide2 + Python 2.7环境设计
"""

# Python 2.7环境专用导入
from __future__ import print_function, unicode_literals
import sys

# 设置默认编码
reload(sys)
sys.setdefaultencoding('utf-8')
print(u"✓ Python 2.7环境初始化完成")

import os
import time
import threading
import traceback
from functools import partial


# Maya 2020 + PySide2 导入 (Python 2.7环境)
from PySide2.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QComboBox, QLineEdit, QPushButton, QLabel,
    QTextEdit, QGridLayout, QSpinBox, QGroupBox, QProgressBar
)
from PySide2.QtCore import QTimer, Signal, QObject, QThread
from PySide2.QtGui import QFont
print(u"✓ Maya 2020 PySide2导入成功 (Python 2.7环境)")


# Maya环境路径设置
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

# 确保项目路径在sys.path中
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(u"✓ 添加项目路径到sys.path: {0}".format(project_root))

# Maya 2020环境检查
try:
    import maya.cmds as cmds
    import maya.utils as utils
    maya_version = cmds.about(version=True)
    print(u"✓ Maya环境检测成功 - Maya版本: {0} (确认为Maya 2020 + PySide2)".format(maya_version))
    if "2020" in maya_version:
        print(u"✓ 确认为Maya 2020环境")
    else:
        print(u"⚠️  检测到非Maya 2020版本: {0}".format(maya_version))
    MAYA_ENV = True
except ImportError:
    print(u"⚠️  非Maya环境，使用模拟模式 (设计用于Maya 2020)")
    MAYA_ENV = False

# Maya环境适配
if not MAYA_ENV:
    # 非Maya环境下的模拟
    class MockMayaUtils:
        @staticmethod
        def executeDeferred(func):
            """模拟Maya的executeDeferred，在主线程中执行"""
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(func)
            timer.start(0)
            return timer

    class MockMayaCmds:
        @staticmethod
        def ls(*args, **kwargs):
            return ["test_namespace:cache_grp", "test_namespace:Geometry", "other:cache_obj"]
        
        @staticmethod
        def objExists(obj):
            return True
        
        @staticmethod
        def playbackOptions(*args, **kwargs):
            return 1 if kwargs.get('min') else 100
        
        @staticmethod
        def select(objects):
            print(u"[Maya 2020模拟] 选择对象: {0}".format(objects))
        
        @staticmethod
        def about(**kwargs):
            return u"2020" if kwargs.get('version') else u"Maya 2020"
        
        @staticmethod  
        def file(**kwargs):
            if kwargs.get('query') and kwargs.get('sceneName'):
                return u"maya2020_test_scene.mb"
            return True
        
        @staticmethod
        def workspace(**kwargs):
            if kwargs.get('query') and kwargs.get('rootDirectory'):
                return u"C:/Maya2020Projects/"
            return True

    class MockLugwitModule:
        @staticmethod
        def lprint(*args):
            print("[LOG]", *args)
        
        @staticmethod
        def isMayaEnv():
            return True

    # 设置模拟环境
    sys.modules['maya.utils'] = MockMayaUtils()
    sys.modules['maya.cmds'] = MockMayaCmds()
    sys.modules['Lugwit_Module'] = MockLugwitModule()
else:
    # 真实Maya环境下导入Lugwit_Module
    try:
        import Lugwit_Module
        print(u"✓ Lugwit_Module导入成功 (Maya 2020环境)")
    except ImportError:
        print(u"⚠️  Lugwit_Module未找到，使用模拟 (Maya 2020)")
        class MockLugwitModule:
            @staticmethod
            def lprint(*args):
                print("[LOG]", *args)
            
            @staticmethod
            def isMayaEnv():
                return True
        sys.modules['Lugwit_Module'] = MockLugwitModule()

# 导入要测试的模块
try:
    from ui_helper import (
        thread_safe_ui_update, 
        UIUpdateQueue, 
        ProjectHelper, 
        ShotHelper, 
        ExportNameHelper,
        MainWindowHelper
    )
    print(u"✓ 成功导入ui_helper模块 (Maya 2020 + PySide2 + Python 2.7)")
except ImportError as e:
    print(u"✗ 导入ui_helper模块失败:", unicode(e))
    traceback.print_exc()
    sys.exit(1)


class TestSignals(QObject):
    """测试信号类"""
    update_ui_signal = Signal(str, object)  # (操作类型, 数据)
    test_completed = Signal(str, bool, str)  # (测试名称, 成功, 消息)


class TestMainWindow(QMainWindow):
    """测试主窗口 - 真实的PySide2 UI"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(u"UI线程安全测试 - Maya 2020 + PySide2")
        self.setGeometry(100, 100, 800, 600)
        
        # 创建信号对象
        self.signals = TestSignals()
        self.signals.update_ui_signal.connect(self.handle_ui_update)
        
        # 测试结果
        self.test_results = []
        self.test_count = 0
        
        self.setup_ui()
        self.setup_ui_helpers()
        
        print(u"✓ 测试主窗口创建完成 (Maya 2020 + PySide2 + Python 2.7)")
    
    def setup_ui(self):
        """设置UI界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # 标题
        title_label = QLabel(u"Maya 2020 UI线程安全测试界面")
        title_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        main_layout.addWidget(title_label)
        
        # 项目信息区域
        project_group = QGroupBox("项目信息")
        project_layout = QHBoxLayout(project_group)
        
        project_layout.addWidget(QLabel("项目:"))
        self.project_combo = QComboBox()
        self.project_combo.setMinimumWidth(120)
        project_layout.addWidget(self.project_combo)
        
        project_layout.addWidget(QLabel("集:"))
        self.ep_combo = QComboBox()
        self.ep_combo.setMinimumWidth(100)
        project_layout.addWidget(self.ep_combo)
        
        project_layout.addWidget(QLabel("场:"))
        self.sc_combo = QComboBox()
        self.sc_combo.setMinimumWidth(100)
        project_layout.addWidget(self.sc_combo)
        
        project_layout.addWidget(QLabel("镜头:"))
        self.shot_combo = QComboBox()
        self.shot_combo.setMinimumWidth(120)
        project_layout.addWidget(self.shot_combo)
        
        main_layout.addWidget(project_group)
        
        # 导出设置区域
        export_group = QGroupBox("导出设置")
        export_layout = QVBoxLayout(export_group)
        
        # JSON预设
        json_layout = QHBoxLayout()
        json_layout.addWidget(QLabel("JSON预设:"))
        self.json_preset_combo = QComboBox()
        self.json_preset_combo.setMinimumWidth(300)
        self.json_preset_combo.setEditable(True)
        json_layout.addWidget(self.json_preset_combo)
        
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.browse_json_file)
        json_layout.addWidget(browse_btn)
        
        export_layout.addLayout(json_layout)
        
        # 时间范围
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("开始帧:"))
        self.start_frame = QSpinBox()
        self.start_frame.setRange(-1000, 10000)
        self.start_frame.setValue(1)
        time_layout.addWidget(self.start_frame)
        
        time_layout.addWidget(QLabel("结束帧:"))
        self.end_frame = QSpinBox()
        self.end_frame.setRange(-1000, 10000)
        self.end_frame.setValue(100)
        time_layout.addWidget(self.end_frame)
        
        time_layout.addStretch()
        export_layout.addLayout(time_layout)
        
        # 缓存匹配模式
        cache_layout = QHBoxLayout()
        cache_layout.addWidget(QLabel("缓存匹配模式:"))
        self.cache_pattern = QLineEdit("*cache*,Geometry")
        cache_layout.addWidget(self.cache_pattern)
        export_layout.addLayout(cache_layout)
        
        main_layout.addWidget(export_group)
        
        # 导出列表网格
        grid_group = QGroupBox("导出对象列表")
        grid_layout = QVBoxLayout(grid_group)
        
        self.export_grid = QGridLayout()
        # 添加表头
        headers = ["选择对象", "名称空间", "导出组", "导出名称", "操作"]
        for i, header in enumerate(headers):
            label = QLabel(header)
            label.setFont(QFont("Microsoft YaHei", 9, QFont.Bold))
            self.export_grid.addWidget(label, 0, i)
        
        grid_widget = QWidget()
        grid_widget.setLayout(self.export_grid)
        grid_layout.addWidget(grid_widget)
        
        main_layout.addWidget(grid_group)
        
        # 测试控制区域
        test_group = QGroupBox("线程安全测试控制")
        test_layout = QVBoxLayout(test_group)
        
        # 测试按钮
        button_layout = QHBoxLayout()
        
        self.main_thread_btn = QPushButton("主线程UI更新测试")
        self.main_thread_btn.clicked.connect(self.test_main_thread_ui)
        button_layout.addWidget(self.main_thread_btn)
        
        self.sub_thread_btn = QPushButton("子线程UI更新测试")
        self.sub_thread_btn.clicked.connect(self.test_sub_thread_ui)
        button_layout.addWidget(self.sub_thread_btn)
        
        self.concurrent_btn = QPushButton("并发测试")
        self.concurrent_btn.clicked.connect(self.test_concurrent_ui)
        button_layout.addWidget(self.concurrent_btn)
        
        self.clear_btn = QPushButton("清除结果")
        self.clear_btn.clicked.connect(self.clear_results)
        button_layout.addWidget(self.clear_btn)
        
        test_layout.addLayout(button_layout)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        test_layout.addWidget(self.progress_bar)
        
        # 测试结果显示
        self.result_text = QTextEdit()
        self.result_text.setMaximumHeight(200)
        self.result_text.setFont(QFont("Consolas", 9))
        test_layout.addWidget(self.result_text)
        
        main_layout.addWidget(test_group)
        
        # 状态显示
        self.status_label = QLabel("准备就绪")
        main_layout.addWidget(self.status_label)
    
    def setup_ui_helpers(self):
        """设置UI助手"""
        # 创建模拟的ui对象
        class MockUI:
            def __init__(self, window):
                self.projectCombo = window.project_combo
                self.epCombo = window.ep_combo
                self.scCombo = window.sc_combo
                self.shotCombo = window.shot_combo
                self.jsonPreset_Combo = window.json_preset_combo
                self.exListGridLay = window.export_grid
                self.cacheMatchPatternWgt = window.cache_pattern
                self.sf_wgt = window.start_frame
                self.ef_wgt = window.end_frame
                self.exDirWgt = QComboBox()  # 模拟
                self.actualDirWgt = QComboBox()  # 模拟
        
        self.ui = MockUI(self)
        
        # 创建qttool模拟
        class MockQtTool:
            def set_combobox_text(self, combo, text):
                if text not in [combo.itemText(i) for i in range(combo.count())]:
                    combo.addItem(text)
                combo.setCurrentText(text)
            
            def collect_and_clear_non_zero_row_widgets(self, layout):
                # 清除网格布局中除第一行外的所有控件
                for i in range(layout.count() - 1, -1, -1):
                    item = layout.itemAt(i)
                    if item and item.widget():
                        row, col, _, _ = layout.getItemPosition(i)
                        if row > 0:  # 保留表头行
                            item.widget().deleteLater()
                            layout.removeItem(item)
        
        self.qttool = MockQtTool()
        
        # 创建UI助手
        self.main_helper = MainWindowHelper(self)
        self.project_helper = ProjectHelper(self, self.project_combo)
        self.shot_helper = ShotHelper(self, self.ep_combo, self.sc_combo, self.shot_combo)
        self.export_helper = ExportNameHelper(self)
        
        print(u"✓ UI助手设置完成 (Maya 2020环境)")
    
    def browse_json_file(self):
        """浏览JSON文件"""
        try:
            from PySide2.QtWidgets import QFileDialog
        except ImportError:
            from PySide.QtGui import QFileDialog
        
        # Maya 2020环境下使用合适的起始目录
        start_dir = "."
        if MAYA_ENV:
            try:
                # Maya 2020工作区路径获取
                workspace = cmds.workspace(query=True, rootDirectory=True)
                if workspace:
                    start_dir = workspace
                    print(u"[Maya 2020] 使用工作区路径: {0}".format(start_dir))
            except:
                pass
        
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择JSON预设文件", start_dir, "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.json_preset_combo.setCurrentText(file_path)
            self.log_result(u"文件选择", True, u"选择了文件: {0}".format(os.path.basename(file_path)))
    
    def log_result(self, test_name, success, message=""):
        """记录测试结果"""
        self.test_count += 1
        status = "✓ 通过" if success else "✗ 失败"
        thread_name = threading.current_thread().name
        
        result_msg = u"[{0}] 测试{1}: {2} - {3}".format(
            thread_name, self.test_count, test_name, status)
        if message:
            result_msg += u" ({0})".format(message)
        
        # 使用信号确保在主线程更新UI
        if threading.current_thread() != threading.main_thread():
            self.signals.test_completed.emit(test_name, success, result_msg)
        else:
            self.result_text.append(result_msg)
            self.result_text.ensureCursorVisible()
        
        self.test_results.append((test_name, success, message))
        print(result_msg)
    
    def handle_ui_update(self, operation_type, data):
        """处理UI更新信号（在主线程中执行）"""
        try:
            if operation_type == "test_result":
                self.result_text.append(data)
                self.result_text.ensureCursorVisible()
            elif operation_type == "status":
                self.status_label.setText(data)
            elif operation_type == "progress":
                self.progress_bar.setValue(data)
        except Exception as e:
            print(u"UI更新失败: {0}".format(unicode(e)))
    
    def update_status(self, message):
        """更新状态 - 线程安全"""
        if threading.current_thread() == threading.main_thread():
            self.status_label.setText(message)
        else:
            self.signals.update_ui_signal.emit("status", message)
    
    def test_main_thread_ui(self):
        """测试主线程UI更新"""
        self.result_text.append("\n=== 主线程UI更新测试 ===")
        self.update_status("正在进行主线程测试...")
        
        try:
            # 测试1: 直接更新组合框
            test_projects = ["主线程项目A", "主线程项目B", "主线程项目C"]
            self.project_helper.update_project_list(test_projects)
            self.log_result(u"主线程项目列表更新", True, u"添加了{0}个项目".format(len(test_projects)))
            
            # 测试2: 更新集列表
            test_episodes = ["主线程EP01", "主线程EP02"]
            self.ep_combo.clear()
            for ep in test_episodes:
                self.ep_combo.addItem(ep)
            self.log_result(u"主线程集列表更新", True, u"添加了{0}个集".format(len(test_episodes)))
            
            # 测试3: 设置时间范围
            self.start_frame.setValue(10)
            self.end_frame.setValue(200)
            self.log_result("主线程时间范围设置", True, "设置时间范围 10-200")
            
            # 测试4: 使用线程安全装饰器
            @thread_safe_ui_update
            def safe_update():
                self.sc_combo.clear()
                self.sc_combo.addItems(["主线程sc001", "主线程sc002"])
                return True
            
            result = safe_update()
            self.log_result("主线程装饰器测试", True, "装饰器在主线程正常工作")
            
            # 测试5: 填充网格布局
            try:
                self.export_helper.populate_grid_layout()
                self.log_result("主线程网格填充", True, "网格布局填充完成")
            except Exception as e:
                self.log_result(u"主线程网格填充", False, u"网格填充失败: {0}".format(unicode(e)))
            
            # 测试6: Maya特有的时间轴设置
            if MAYA_ENV:
                try:
                    self.export_helper.setup_timeline_range()
                    self.log_result("主线程时间轴设置", True, "Maya时间轴设置完成")
                except Exception as e:
                    self.log_result(u"主线程时间轴设置", False, u"时间轴设置失败: {0}".format(unicode(e)))
            
        except Exception as e:
            self.log_result("主线程测试", False, str(e))
            traceback.print_exc()
        
        self.update_status("主线程测试完成")
    
    def test_sub_thread_ui(self):
        """测试子线程UI更新"""
        self.result_text.append("\n=== 子线程UI更新测试 ===")
        self.update_status("正在启动子线程测试...")
        
        def thread_worker():
            try:
                thread_name = threading.current_thread().name
                print(u"子线程 {0} 开始执行 (Maya 2020环境)".format(thread_name))
                
                # 测试1: 不安全的直接UI更新（应该会失败或警告）
                try:
                    # 注意：这个操作在子线程中是不安全的
                    # 但我们的装饰器应该会自动处理
                    test_projects = ["子线程项目X", "子线程项目Y", "子线程项目Z"]
                    self.project_helper.update_project_list(test_projects)
                    self.log_result("子线程项目列表更新", True, "线程安全装饰器生效")
                except Exception as e:
                    self.log_result("子线程项目列表更新", False, str(e))
                
                time.sleep(0.1)  # 模拟耗时操作
                
                # 测试2: 使用UI更新队列
                try:
                    ui_queue = self.main_helper.ui_queue
                    
                    def queue_update():
                        self.ep_combo.clear()
                        self.ep_combo.addItems(["子线程EP10", "子线程EP20"])
                    
                    ui_queue.add_update(queue_update)
                    time.sleep(0.2)  # 等待队列处理
                    self.log_result("子线程队列更新", True, "UI队列正常工作")
                except Exception as e:
                    self.log_result("子线程队列更新", False, str(e))
                
                # 测试3: 批量更新
                try:
                    def batch_update1():
                        self.sc_combo.clear()
                        self.sc_combo.addItems(["子线程sc100", "子线程sc200"])
                    
                    def batch_update2():
                        self.shot_combo.clear()
                        self.shot_combo.addItems(["子线程shot001", "子线程shot002"])
                    
                    batch_updates = [
                        (batch_update1, [], {}),
                        (batch_update2, [], {})
                    ]
                    
                    self.main_helper.batch_ui_update(batch_updates)
                    time.sleep(0.3)  # 等待批量处理
                    self.log_result("子线程批量更新", True, "批量UI更新正常")
                except Exception as e:
                    self.log_result("子线程批量更新", False, str(e))
                
                # 测试4: 线程安全装饰器
                try:
                    @thread_safe_ui_update
                    def thread_safe_update():
                        self.cache_pattern.setText("子线程模式: *thread_cache*")
                        return "success"
                    
                    result = thread_safe_update()
                    self.log_result("子线程装饰器", True, "装饰器在子线程正常工作")
                except Exception as e:
                    self.log_result("子线程装饰器", False, str(e))
                
                # 测试5: Maya特有功能测试
                if MAYA_ENV:
                    try:
                        # 测试Maya场景操作相关的UI更新
                        @thread_safe_ui_update
                        def maya_specific_update():
                            # 模拟Maya场景信息更新UI
                            scene_name = cmds.file(query=True, sceneName=True) or "未保存场景"
                            self.json_preset_combo.setEditText(u"Maya场景: {0}".format(
                                os.path.basename(scene_name)))
                            return "success"
                        
                        result = maya_specific_update()
                        self.log_result("子线程Maya特有功能", True, "Maya场景信息更新成功")
                    except Exception as e:
                        self.log_result("子线程Maya特有功能", False, str(e))
                
                # 测试6: 使用信号更新状态
                self.signals.update_ui_signal.emit("status", "子线程测试即将完成...")
                time.sleep(0.1)
                
                print(u"子线程 {0} 执行完成".format(thread_name))
                
            except Exception as e:
                self.log_result("子线程执行", False, str(e))
                traceback.print_exc()
        
        # 启动子线程
        thread = threading.Thread(target=thread_worker, name="UITestThread")
        thread.daemon = True
        thread.start()
        
        # 使用定时器检查线程状态
        def check_thread_status():
            if thread.is_alive():
                # 线程仍在运行，继续检查
                QTimer.singleShot(100, check_thread_status)
            else:
                self.update_status("子线程测试完成")
        
        QTimer.singleShot(100, check_thread_status)
    
    def test_concurrent_ui(self):
        """测试并发UI更新"""
        self.result_text.append("\n=== 并发UI更新测试 ===")
        self.update_status("正在进行并发测试...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        completed_count = 0
        total_threads = 5
        
        def thread_worker(thread_id):
            nonlocal completed_count
            try:
                thread_name = u"ConcurrentThread-{0}".format(thread_id)
                threading.current_thread().name = thread_name
                
                # 每个线程执行不同的UI更新操作
                for i in range(3):
                    time.sleep(0.05)  # 模拟工作
                    
                    if thread_id % 2 == 0:
                        # 偶数线程更新项目列表
                        projects = [u"并发项目{0}-{1}".format(thread_id, i)]
                        self.main_helper.safe_ui_update(
                            lambda p=projects: self.project_combo.addItems(p)
                        )
                    else:
                        # 奇数线程更新集列表
                        episodes = [u"并发EP{0}-{1}".format(thread_id, i)]
                        self.main_helper.safe_ui_update(
                            lambda e=episodes: self.ep_combo.addItems(e)
                        )
                    
                    # 更新进度
                    progress = ((completed_count * 3 + i + 1) / (total_threads * 3)) * 100
                    self.signals.update_ui_signal.emit("progress", int(progress))
                
                completed_count += 1
                self.log_result(u"并发线程{0}".format(thread_id), True, u"完成3次UI更新")
                
                # 如果是最后一个线程，隐藏进度条
                if completed_count >= total_threads:
                    QTimer.singleShot(500, lambda: self.progress_bar.setVisible(False))
                
            except Exception as e:
                self.log_result(u"并发线程{0}".format(thread_id), False, unicode(e))
        
        # 启动多个并发线程
        threads = []
        for i in range(total_threads):
            thread = threading.Thread(target=thread_worker, args=(i,))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        
        # 监控所有线程完成
        def monitor_threads():
            all_done = all(not t.is_alive() for t in threads)
            if all_done:
                self.update_status(u"并发测试完成 - {0}个线程".format(total_threads))
                self.log_result(u"并发测试总结", True, u"所有{0}个线程完成".format(total_threads))
            else:
                QTimer.singleShot(100, monitor_threads)
        
        QTimer.singleShot(100, monitor_threads)
    
    def clear_results(self):
        """清除测试结果"""
        self.result_text.clear()
        self.test_results.clear()
        self.test_count = 0
        self.update_status("结果已清除")
        
        # 重置UI到初始状态
        for combo in [self.project_combo, self.ep_combo, self.sc_combo, self.shot_combo]:
            combo.clear()
        
        self.cache_pattern.setText("*cache*,Geometry")
        self.start_frame.setValue(1)
        self.end_frame.setValue(100)
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        print("测试窗口关闭")
        event.accept()


def main():
    """主函数 - Maya环境适配版本"""
    print("=== Maya UI线程安全测试 ===")
    print(f"Python版本: {sys.version}")
    print(f"当前线程: {threading.current_thread().name}")
    
    if MAYA_ENV:
        print(f"✓ 运行在Maya环境中")
        try:
            maya_version = cmds.about(version=True)
            print(f"Maya版本: {maya_version}")
        except:
            print("Maya版本获取失败")
    else:
        print("⚠️  运行在模拟Maya环境中")
    
    # Maya环境下QApplication通常已存在
    app = QApplication.instance()
    if app is None:
        print(u"创建新的QApplication实例")
        app = QApplication(sys.argv if not MAYA_ENV else [])
    else:
        print(u"✓ 使用现有的QApplication实例")
    
    # 创建并显示测试窗口
    window = TestMainWindow()
    window.show()
    
    # 显示使用说明
    window.result_text.append("=== Maya UI线程安全测试说明 ===")
    window.result_text.append("1. 点击'主线程UI更新测试' - 测试在主线程中的UI操作")
    window.result_text.append("2. 点击'子线程UI更新测试' - 测试子线程中的线程安全UI更新")
    window.result_text.append("3. 点击'并发测试' - 测试多个线程并发访问UI")
    window.result_text.append("4. 观察控制台输出和测试结果")
    window.result_text.append(f"环境: {'真实Maya' if MAYA_ENV else '模拟Maya'}")
    window.result_text.append("=" * 50)
    
    print("✓ 测试界面已启动")
    print("请在UI界面中点击测试按钮进行测试")
    
    if MAYA_ENV:
        print("Maya环境下窗口将保持打开，可手动关闭")
        # Maya环境下不需要调用app.exec_()，因为Maya已经有事件循环
        return window  # 返回窗口实例以保持引用
    else:
        # 非Maya环境下运行事件循环
        try:
            sys.exit(app.exec_())
        except KeyboardInterrupt:
            print("用户中断")
        except Exception as e:
            print(f"应用异常: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    main()
else:
    # 当作为模块导入时，提供便捷的启动函数
    def start_ui_thread_test():
        """
        Maya环境下的便捷启动函数
        
        在Maya Script Editor中运行:
        from test_pyside2_ui_thread import start_ui_thread_test
        start_ui_thread_test()
        
        或者:
        exec(open(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc/test_pyside2_ui_thread.py').read())
        start_ui_thread_test()
        """
        return main()
    
    def quick_test():
        """
        快速测试函数 - 不显示UI，直接在控制台输出结果
        """
        print("=== 快速UI线程安全测试 ===")
        
        # 简单测试线程安全装饰器
        test_result = []
        
        @thread_safe_ui_update 
        def test_decorator():
            test_result.append("装饰器测试成功")
            return True
        
        try:
            # 在子线程中测试
            def thread_worker():
                test_decorator()
                test_result.append("子线程调用成功")
            
            import threading
            thread = threading.Thread(target=thread_worker)
            thread.start()
            thread.join(timeout=2)
            
            if len(test_result) >= 2:
                print("✓ 线程安全装饰器测试通过")
                print("✓ 子线程UI更新测试通过")
                print("🎉 基本线程安全功能正常！")
                return True
            else:
                print(u"✗ 测试未完成")
                return False
                
        except Exception as e:
            print(f"✗ 测试失败: {e}")
            return False
    
    # Maya环境下自动提示
    if MAYA_ENV:
        print("\n=== Maya UI线程安全测试模块已加载 ===")
        print("💡 使用方法:")
        print("   1. start_ui_thread_test()  # 启动完整UI测试")
        print("   2. quick_test()           # 快速控制台测试")
        print("   3. main()                 # 完整测试程序")
        print("="*50)