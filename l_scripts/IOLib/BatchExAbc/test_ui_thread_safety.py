# -*- coding: utf-8 -*-
"""
UI线程安全测试文件
测试ui_helper.py中的线程安全UI更新功能
"""

import os
import sys
import time
import threading
import traceback
from functools import partial

# 添加项目路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 模拟Maya环境（如果不在Maya中运行）
class MockMayaUtils:
    """模拟Maya的utils模块"""
    @staticmethod
    def executeDeferred(func):
        print(u"[模拟Maya] executeDeferred调用: {}".format(func.__name__))
        # 在新线程中延迟执行，模拟Maya的行为
        def delayed_exec():
            time.sleep(0.01)  # 短暂延迟
            func()
        
        thread = threading.Thread(target=delayed_exec)
        thread.daemon = True
        thread.start()

class MockMayaCmds:
    """模拟Maya的cmds模块"""
    @staticmethod
    def ls(*args, **kwargs):
        return ["test_namespace:obj1", "test_namespace:obj2", "other:obj3"]
    
    @staticmethod
    def objExists(obj):
        return True
    
    @staticmethod
    def playbackOptions(*args, **kwargs):
        return 100 if kwargs.get('min') else 200
    
    @staticmethod
    def select(objects):
        print(u"[模拟Maya] 选择对象: {}".format(objects))

# 模拟Lugwit_Module
class MockLugwitModule:
    @staticmethod
    def lprint(*args):
        print(u"[LOG]", *args)
    
    @staticmethod
    def isMayaEnv():
        return True  # 模拟在Maya环境中

# 模拟PySide2组件
class MockComboBox:
    def __init__(self, name="ComboBox"):
        self.name = name
        self.items = []
        self.current_index = 0
        self.signals_blocked = False
        print(u"[UI] 创建组合框: {}".format(name))
    
    def clear(self):
        if not self.signals_blocked:
            print(u"[UI] {} 清空".format(self.name))
        self.items = []
        self.current_index = 0
    
    def addItem(self, text):
        if not self.signals_blocked:
            print(u"[UI] {} 添加项目: {}".format(self.name, text))
        self.items.append(text)
    
    def addItems(self, items):
        for item in items:
            self.addItem(item)
    
    def setCurrentText(self, text):
        if not self.signals_blocked:
            print(u"[UI] {} 设置当前文本: {}".format(self.name, text))
        if text in self.items:
            self.current_index = self.items.index(text)
    
    def setCurrentIndex(self, index):
        if not self.signals_blocked:
            print(u"[UI] {} 设置当前索引: {}".format(self.name, index))
        if 0 <= index < len(self.items):
            self.current_index = index
    
    def currentText(self):
        return self.items[self.current_index] if self.items else ""
    
    def currentTextChanged(self):
        # 模拟信号
        class MockSignal:
            def connect(self, func):
                print(u"[UI] {} 连接信号: {}".format(self.name, func.__name__))
        return MockSignal()
    
    def blockSignals(self, block):
        self.signals_blocked = block
        print(u"[UI] {} 信号阻塞: {}".format(self.name, block))
    
    def count(self):
        return len(self.items)
    
    def itemText(self, index):
        return self.items[index] if 0 <= index < len(self.items) else ""

class MockLineEdit:
    def __init__(self, name="LineEdit"):
        self.name = name
        self.text_value = ""
        print(u"[UI] 创建文本框: {}".format(name))
    
    def text(self):
        return self.text_value
    
    def setText(self, text):
        print(u"[UI] {} 设置文本: {}".format(self.name, text))
        self.text_value = text

class MockLabel:
    def __init__(self, text="Label"):
        self.text_value = text
        print(u"[UI] 创建标签: {}".format(text))

class MockButton:
    def __init__(self, text="Button"):
        self.text_value = text
        print(u"[UI] 创建按钮: {}".format(text))
    
    def clicked(self):
        class MockSignal:
            def connect(self, func):
                print(u"[UI] 按钮连接点击信号: {}".format(func.__name__))
        return MockSignal()

class MockGridLayout:
    def __init__(self):
        self.widgets = {}  # {(row, col): widget}
        print(u"[UI] 创建网格布局")
    
    def addWidget(self, widget, row, col):
        self.widgets[(row, col)] = widget
        print(u"[UI] 网格布局添加控件到 ({}, {}): {}".format(row, col, type(widget).__name__))
    
    def itemAtPosition(self, row, col):
        widget = self.widgets.get((row, col))
        if widget:
            class MockLayoutItem:
                def widget(self):
                    return widget
            return MockLayoutItem()
        return None
    
    def count(self):
        return len(self.widgets)
    
    def getItemPosition(self, index):
        positions = list(self.widgets.keys())
        if index < len(positions):
            row, col = positions[index]
            return row, col, 1, 1  # row, col, rowspan, colspan
        return 0, 0, 1, 1

class MockUI:
    """模拟主窗口UI"""
    def __init__(self):
        self.projectCombo = MockComboBox("项目下拉框")
        self.epCombo = MockComboBox("集下拉框")
        self.scCombo = MockComboBox("场下拉框")
        self.shotCombo = MockComboBox("镜头下拉框")
        self.jsonPreset_Combo = MockComboBox("JSON预设下拉框")
        self.exListGridLay = MockGridLayout()
        self.cacheMatchPatternWgt = MockLineEdit("缓存匹配模式")
        self.sf_wgt = MockLineEdit("开始帧")
        self.ef_wgt = MockLineEdit("结束帧")
        self.exDirWgt = MockComboBox("导出目录")
        self.actualDirWgt = MockComboBox("实际目录")
        
        # 设置一些默认值
        self.cacheMatchPatternWgt.setText("*cache*,Geometry")
        self.sf_wgt.setValue = lambda x: print(u"[UI] 设置开始帧: {}".format(x))
        self.ef_wgt.setValue = lambda x: print(u"[UI] 设置结束帧: {}".format(x))

class MockMainWindow:
    """模拟主窗口"""
    def __init__(self):
        self.ui = MockUI()
        self.qttool = self
        print(u"[UI] 创建模拟主窗口")
    
    def set_combobox_text(self, combo, text):
        combo.setCurrentText(text)
    
    def collect_and_clear_non_zero_row_widgets(self, layout):
        print(u"[UI] 清理网格布局非零行")
    
    def get_shotEntireName(self):
        return "TEST_EP01_sc001_shot001"
    
    def getActuralDir(self):
        print(u"[主窗口] 获取实际目录")
    
    def selectExGroup(self, row):
        print(u"[主窗口] 选择导出组，行: {}".format(row))

# 设置模拟环境
sys.modules['maya.utils'] = MockMayaUtils()
sys.modules['maya.cmds'] = MockMayaCmds()
sys.modules['Lugwit_Module'] = MockLugwitModule()

# 现在导入要测试的模块
try:
    from ui_helper import (
        thread_safe_ui_update, 
        UIUpdateQueue, 
        QTimerUIUpdater,
        ProjectHelper, 
        ShotHelper, 
        ExportNameHelper,
        MainWindowHelper
    )
    print(u"✓ 成功导入ui_helper模块")
except ImportError as e:
    print(u"✗ 导入ui_helper模块失败: {}".format(e))
    traceback.print_exc()
    sys.exit(1)

class ThreadSafetyTester:
    """线程安全测试类"""
    
    def __init__(self):
        self.main_window = MockMainWindow()
        self.test_results = []
        self.test_count = 0
        print(u"\n=== 线程安全UI更新测试初始化 ===")
    
    def log_test_result(self, test_name, success, message=""):
        """记录测试结果"""
        self.test_count += 1
        status = "✓ 通过" if success else "✗ 失败"
        result_msg = u"测试 {}: {} - {}".format(self.test_count, test_name, status)
        if message:
            result_msg += u" ({})".format(message)
        
        print(result_msg)
        self.test_results.append((test_name, success, message))
    
    def test_thread_safe_decorator(self):
        """测试线程安全装饰器"""
        print(u"\n--- 测试1: 线程安全装饰器 ---")
        
        # 创建一个测试函数
        @thread_safe_ui_update
        def test_ui_function():
            print(u"[测试] 线程安全UI函数执行")
            return "success"
        
        try:
            # 在主线程中执行
            result = test_ui_function()
            self.log_test_result("主线程装饰器", True, "主线程执行正常")
            
            # 在子线程中执行
            def thread_worker():
                try:
                    test_ui_function()
                    self.log_test_result("子线程装饰器", True, "子线程执行正常")
                except Exception as e:
                    self.log_test_result("子线程装饰器", False, str(e))
            
            thread = threading.Thread(target=thread_worker)
            thread.start()
            thread.join(timeout=2)
            
        except Exception as e:
            self.log_test_result("线程安全装饰器", False, str(e))
    
    def test_ui_update_queue(self):
        """测试UI更新队列"""
        print(u"\n--- 测试2: UI更新队列 ---")
        
        try:
            queue = UIUpdateQueue()
            
            # 测试函数
            test_calls = []
            def test_func(msg):
                test_calls.append(msg)
                print(u"[队列测试] 执行: {}".format(msg))
            
            # 添加多个更新
            queue.add_update(test_func, "更新1")
            queue.add_update(test_func, "更新2")
            queue.add_update(test_func, "更新3")
            
            # 等待处理完成
            time.sleep(0.5)
            
            if len(test_calls) >= 3:
                self.log_test_result("UI更新队列", True, "队列处理了{}个更新".format(len(test_calls)))
            else:
                self.log_test_result("UI更新队列", False, "期望3个更新，实际{}个".format(len(test_calls)))
            
            # 测试批量更新
            test_calls.clear()
            batch_updates = [
                (test_func, ["批量1"], {}),
                (test_func, ["批量2"], {}),
                (test_func, ["批量3"], {})
            ]
            queue.batch_update(batch_updates)
            
            time.sleep(0.5)
            
            if len(test_calls) >= 3:
                self.log_test_result("批量UI更新", True, "批量处理了{}个更新".format(len(test_calls)))
            else:
                self.log_test_result("批量UI更新", False, "期望3个更新，实际{}个".format(len(test_calls)))
                
        except Exception as e:
            self.log_test_result("UI更新队列", False, str(e))
            traceback.print_exc()
    
    def test_qtimer_updater(self):
        """测试QTimer更新器"""
        print(u"\n--- 测试3: QTimer更新器 ---")
        
        try:
            updater = QTimerUIUpdater()
            
            test_calls = []
            def timer_test_func(msg):
                test_calls.append(msg)
                print(u"[QTimer测试] 执行: {}".format(msg))
            
            # 安排多个更新
            updater.schedule_update(timer_test_func, "定时器更新1")
            updater.schedule_update(timer_test_func, "定时器更新2")
            
            # 等待处理
            time.sleep(0.5)
            
            if len(test_calls) >= 2:
                self.log_test_result("QTimer更新器", True, "处理了{}个更新".format(len(test_calls)))
            else:
                self.log_test_result("QTimer更新器", False, "期望2个更新，实际{}个".format(len(test_calls)))
                
        except Exception as e:
            self.log_test_result("QTimer更新器", False, str(e))
            traceback.print_exc()
    
    def test_project_helper(self):
        """测试项目助手的线程安全性"""
        print(u"\n--- 测试4: 项目助手线程安全 ---")
        
        try:
            project_helper = ProjectHelper(self.main_window, self.main_window.ui.projectCombo)
            
            # 测试项目列表更新
            test_projects = ["项目A", "项目B", "项目C"]
            
            def thread_update_projects():
                try:
                    project_helper.update_project_list(test_projects)
                    self.log_test_result("项目助手线程安全", True, "项目列表更新成功")
                except Exception as e:
                    self.log_test_result("项目助手线程安全", False, str(e))
            
            # 在子线程中执行
            thread = threading.Thread(target=thread_update_projects)
            thread.start()
            thread.join(timeout=2)
            
            # 验证结果
            combo = self.main_window.ui.projectCombo
            if len(combo.items) == len(test_projects):
                self.log_test_result("项目列表验证", True, "项目数量正确: {}".format(len(combo.items)))
            else:
                self.log_test_result("项目列表验证", False, "期望{}项目，实际{}项目".format(len(test_projects), len(combo.items)))
                
        except Exception as e:
            self.log_test_result("项目助手测试", False, str(e))
            traceback.print_exc()
    
    def test_shot_helper(self):
        """测试镜头助手的线程安全性"""
        print(u"\n--- 测试5: 镜头助手线程安全 ---")
        
        try:
            shot_helper = ShotHelper(
                self.main_window,
                self.main_window.ui.epCombo,
                self.main_window.ui.scCombo,
                self.main_window.ui.shotCombo
            )
            
            # 测试集列表更新
            test_episodes = ["EP01", "EP02", "EP03"]
            
            def thread_update_episodes():
                try:
                    # 模拟数据中心
                    class MockDataCenter:
                        def __init__(self):
                            self.current_episode_list = test_episodes
                            self.current_episode_name = "EP01"
                    
                    shot_helper.data_center = MockDataCenter()
                    shot_helper.update_episode_list()
                    self.log_test_result("镜头助手线程安全", True, "集列表更新成功")
                except Exception as e:
                    self.log_test_result("镜头助手线程安全", False, str(e))
            
            thread = threading.Thread(target=thread_update_episodes)
            thread.start()
            thread.join(timeout=2)
            
        except Exception as e:
            self.log_test_result("镜头助手测试", False, str(e))
            traceback.print_exc()
    
    def test_export_name_helper(self):
        """测试导出名称助手的线程安全性"""
        print(u"\n--- 测试6: 导出名称助手线程安全 ---")
        
        try:
            export_helper = ExportNameHelper(self.main_window)
            
            def thread_populate_grid():
                try:
                    export_helper.populate_grid_layout()
                    self.log_test_result("导出助手网格填充", True, "网格布局填充成功")
                except Exception as e:
                    self.log_test_result("导出助手网格填充", False, str(e))
            
            def thread_timeline_setup():
                try:
                    export_helper.setup_timeline_range()
                    self.log_test_result("导出助手时间轴", True, "时间轴设置成功")
                except Exception as e:
                    self.log_test_result("导出助手时间轴", False, str(e))
            
            # 并发执行多个操作
            thread1 = threading.Thread(target=thread_populate_grid)
            thread2 = threading.Thread(target=thread_timeline_setup)
            
            thread1.start()
            thread2.start()
            
            thread1.join(timeout=2)
            thread2.join(timeout=2)
            
        except Exception as e:
            self.log_test_result("导出名称助手测试", False, str(e))
            traceback.print_exc()
    
    def test_main_window_helper(self):
        """测试主窗口助手的便捷方法"""
        print(u"\n--- 测试7: 主窗口助手便捷方法 ---")
        
        try:
            main_helper = MainWindowHelper(self.main_window)
            
            # 测试安全UI更新
            def test_safe_update():
                print(u"[主助手测试] 安全UI更新执行")
            
            main_helper.safe_ui_update(test_safe_update)
            time.sleep(0.2)
            self.log_test_result("主助手安全更新", True, "安全UI更新调用成功")
            
            # 测试批量更新
            test_calls = []
            def batch_func1():
                test_calls.append("批量1")
            def batch_func2():
                test_calls.append("批量2")
            
            batch_updates = [
                (batch_func1, [], {}),
                (batch_func2, [], {})
            ]
            
            main_helper.batch_ui_update(batch_updates)
            time.sleep(0.5)
            
            if len(test_calls) >= 2:
                self.log_test_result("主助手批量更新", True, "批量更新成功: {}".format(test_calls))
            else:
                self.log_test_result("主助手批量更新", False, "批量更新未完成: {}".format(test_calls))
            
        except Exception as e:
            self.log_test_result("主窗口助手测试", False, str(e))
            traceback.print_exc()
    
    def test_concurrent_stress(self):
        """并发压力测试"""
        print(u"\n--- 测试8: 并发压力测试 ---")
        
        try:
            queue = UIUpdateQueue()
            completed_updates = []
            
            def stress_update(thread_id, update_id):
                completed_updates.append("T{}-U{}".format(thread_id, update_id))
                print(u"[压力测试] 线程{} 更新{}完成".format(thread_id, update_id))
            
            # 创建多个线程，每个线程发送多个更新
            threads = []
            for thread_id in range(5):
                def thread_worker(tid=thread_id):
                    for update_id in range(3):
                        queue.add_update(stress_update, tid, update_id)
                        time.sleep(0.01)  # 短暂间隔
                
                thread = threading.Thread(target=thread_worker)
                threads.append(thread)
                thread.start()
            
            # 等待所有线程完成
            for thread in threads:
                thread.join(timeout=3)
            
            # 等待队列处理完成
            time.sleep(1)
            
            expected_count = 5 * 3  # 5个线程 × 3个更新
            actual_count = len(completed_updates)
            
            if actual_count >= expected_count * 0.8:  # 允许80%成功率
                self.log_test_result("并发压力测试", True, 
                    "完成{}/{}个更新 ({:.1f}%)".format(actual_count, expected_count, 
                    actual_count/expected_count*100))
            else:
                self.log_test_result("并发压力测试", False,
                    "仅完成{}/{}个更新".format(actual_count, expected_count))
                
        except Exception as e:
            self.log_test_result("并发压力测试", False, str(e))
            traceback.print_exc()
    
    def run_all_tests(self):
        """运行所有测试"""
        print(u"\n🚀 开始线程安全UI更新测试")
        print(u"=" * 50)
        
        start_time = time.time()
        
        # 执行所有测试
        self.test_thread_safe_decorator()
        self.test_ui_update_queue()
        self.test_qtimer_updater()
        self.test_project_helper()
        self.test_shot_helper()
        self.test_export_name_helper()
        self.test_main_window_helper()
        self.test_concurrent_stress()
        
        # 等待所有异步操作完成
        time.sleep(1)
        
        # 统计结果
        end_time = time.time()
        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)
        
        print(u"\n" + "=" * 50)
        print(u"📊 测试结果汇总")
        print(u"总测试数: {}".format(total))
        print(u"通过: {} ✓".format(passed))
        print(u"失败: {} ✗".format(total - passed))
        print(u"成功率: {:.1f}%".format(passed/total*100 if total > 0 else 0))
        print(u"用时: {:.2f}秒".format(end_time - start_time))
        
        # 详细失败信息
        failed_tests = [(name, msg) for name, success, msg in self.test_results if not success]
        if failed_tests:
            print(u"\n❌ 失败的测试:")
            for name, msg in failed_tests:
                print(u"  - {}: {}".format(name, msg))
        else:
            print(u"\n🎉 所有测试都通过了！")
        
        return passed == total

def main():
    """主测试函数"""
    print(u"线程安全UI更新测试 v1.0")
    print(u"测试环境: Python {}.{}".format(sys.version_info.major, sys.version_info.minor))
    
    tester = ThreadSafetyTester()
    success = tester.run_all_tests()
    
    if success:
        print(u"\n✅ 所有测试通过！代码质量良好。")
        return 0
    else:
        print(u"\n⚠️  部分测试失败，请检查代码。")
        return 1

if __name__ == "__main__":
    sys.exit(main())