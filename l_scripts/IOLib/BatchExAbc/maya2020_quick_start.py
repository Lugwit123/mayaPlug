# -*- coding: utf-8 -*-
"""
Maya 2020专用UI线程安全测试快速启动
纯Python 2.7环境，无需考虑Python 3.x兼容性

使用方法：
在Maya 2020 Script Editor中一键执行：
exec(open(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc/maya2020_quick_start.py').read())
"""

from __future__ import print_function, unicode_literals
import sys
import os

# 确保编码正确
reload(sys)
sys.setdefaultencoding('utf-8')

def maya2020_quick_start():
    u"""Maya 2020一键启动UI测试"""
    
    print(u"🚀 Maya 2020 UI线程安全测试一键启动")
    
    # 基本环境检查
    try:
        import maya.cmds as cmds
        version = cmds.about(version=True)
        print(u"✓ Maya版本: {0}".format(version))
        
        # 检查PySide2
        from PySide2.QtCore import QTimer
        print(u"✓ PySide2可用")
        
        # 执行测试文件
        test_file = os.path.join(os.path.dirname(__file__), 'test_pyside2_ui_thread.py')
        
        if os.path.exists(test_file):
            print(u"✓ 加载测试模块...")
            exec(open(test_file).read(), globals())
            
            print(u"✓ 启动UI测试界面...")
            if 'start_ui_thread_test' in globals():
                return start_ui_thread_test()
            elif 'main' in globals():
                return main()
            else:
                print(u"✗ 启动函数未找到")
                return False
        else:
            print(u"✗ 测试文件未找到: {0}".format(test_file))
            return False
            
    except ImportError as e:
        print(u"✗ 环境检查失败: {0}".format(unicode(e)))
        return False
    except Exception as e:
        print(u"✗ 启动失败: {0}".format(unicode(e)))
        import traceback
        traceback.print_exc()
        return False

def maya2020_console_test():
    u"""Maya 2020控制台快速测试"""
    
    print(u"⚡ Maya 2020控制台快速测试")
    
    try:
        # 简单的装饰器测试
        test_file = os.path.join(os.path.dirname(__file__), 'test_pyside2_ui_thread.py')
        if os.path.exists(test_file):
            exec(open(test_file).read(), globals())
            if 'quick_test' in globals():
                return quick_test()
        
        print(u"✗ 快速测试函数未找到")
        return False
        
    except Exception as e:
        print(u"✗ 控制台测试失败: {0}".format(unicode(e)))
        return False

# 如果直接执行此文件，自动启动
if __name__ == "__main__":
    maya2020_quick_start()
else:
    print(u"")
    print(u"=== Maya 2020专用启动器 ===")
    print(u"💡 使用方法:")
    print(u"   maya2020_quick_start()     # 一键启动UI测试")
    print(u"   maya2020_console_test()    # 控制台快速测试")
    print(u"=" * 30)