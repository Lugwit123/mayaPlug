# -*- coding: utf-8 -*-
"""
Maya 2020 UI线程安全测试快速启动脚本
专门针对Maya 2020 + PySide2 + Python 2.7环境设计

使用方法：
在Maya 2020的Script Editor中执行：
exec(open(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc/maya2020_ui_test_launcher.py').read())
"""

from __future__ import print_function, unicode_literals
import sys
import os

def maya2020_ui_test():
    u"""Maya 2020专用UI线程安全测试启动器"""
    
    print(u"=== Maya 2020 UI线程安全测试启动器 ===")
    
    # 检查Maya环境
    try:
        import maya.cmds as cmds
        maya_version = cmds.about(version=True)
        print(u"✓ 检测到Maya版本: {0}".format(maya_version))
        
        if "2020" in maya_version:
            print(u"✓ 确认为Maya 2020环境")
        else:
            print(u"⚠️  当前不是Maya 2020，但将继续执行测试")
            
    except ImportError:
        print(u"✗ 未检测到Maya环境")
        return False
    
    # 检查PySide2
    try:
        from PySide2.QtCore import QTimer
        print(u"✓ PySide2可用")
    except ImportError:
        print(u"✗ PySide2不可用，Maya 2020应该包含PySide2")
        return False
    
    # 检查Python版本
    if sys.version_info[0] == 2:
        print(u"✓ Python 2.7环境")
    else:
        print(u"⚠️  非Python 2.7环境，Maya 2020通常使用Python 2.7")
    
    # 执行主测试文件
    test_file_path = os.path.join(
        os.path.dirname(__file__), 
        'test_pyside2_ui_thread.py'
    )
    
    if not os.path.exists(test_file_path):
        print(u"✗ 测试文件未找到: {0}".format(test_file_path))
        return False
    
    print(u"✓ 正在加载测试文件...")
    
    try:
        # 执行测试文件
        exec(open(test_file_path).read(), globals())
        
        # 启动UI测试
        if 'start_ui_thread_test' in globals():
            print(u"🚀 启动Maya 2020 UI线程安全测试界面...")
            window = start_ui_thread_test()
            print(u"✓ 测试界面已启动")
            return window
        else:
            print(u"⚠️  测试函数未找到，尝试直接运行main()")
            if 'main' in globals():
                return main()
            else:
                print(u"✗ 无法启动测试")
                return False
                
    except Exception as e:
        print(u"✗ 执行测试文件失败: {0}".format(unicode(e)))
        import traceback
        traceback.print_exc()
        return False

def quick_maya2020_test():
    u"""Maya 2020快速控制台测试"""
    
    print(u"=== Maya 2020快速线程安全测试 ===")
    
    try:
        # 导入测试文件中的函数
        test_file_path = os.path.join(
            os.path.dirname(__file__), 
            'test_pyside2_ui_thread.py'
        )
        
        if os.path.exists(test_file_path):
            exec(open(test_file_path).read(), globals())
            
            if 'quick_test' in globals():
                return quick_test()
            else:
                print(u"✗ quick_test函数未找到")
                return False
        else:
            print(u"✗ 测试文件未找到")
            return False
            
    except Exception as e:
        print(u"✗ 快速测试失败: {0}".format(unicode(e)))
        return False

# 主要执行函数
if __name__ == "__main__":
    # 如果直接运行此文件，启动完整测试
    maya2020_ui_test()
else:
    # 如果作为模块导入，提供便捷函数
    print(u"")
    print(u"=== Maya 2020 UI线程安全测试启动器已加载 ===")
    print(u"💡 可用命令:")
    print(u"   maya2020_ui_test()     # 启动完整UI测试")
    print(u"   quick_maya2020_test()  # 快速控制台测试")
    print(u"=" * 50)

"""
=== Maya 2020作为模块导入运行示例 ===

方法1: 直接exec执行（推荐）
-------------------------------
# 在Maya 2020 Script Editor中执行
exec(open(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc/maya2020_ui_test_launcher.py').read())
maya2020_ui_test()  # 启动UI测试
# 或
quick_maya2020_test()  # 快速控制台测试

方法2: 模块导入方式
-------------------------------
# 步骤1: 添加路径到sys.path
import sys
sys.path.append(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc')

# 步骤2: 导入模块
import maya2020_ui_test_launcher

# 步骤3: 调用函数
maya2020_ui_test_launcher.maya2020_ui_test()      # 完整UI测试
# 或
maya2020_ui_test_launcher.quick_maya2020_test()   # 快速测试

方法3: reload重新加载（开发调试用）
-------------------------------
# 如果已经导入过，需要重新加载
import sys
sys.path.append(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc')
import maya2020_ui_test_launcher
reload(maya2020_ui_test_launcher)  # Python 2.7重新加载模块
maya2020_ui_test_launcher.maya2020_ui_test()

方法4: 一行式快速启动
-------------------------------
# 复制粘贴到Maya Script Editor即可
exec(open(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc/maya2020_ui_test_launcher.py').read()); maya2020_ui_test()

注意事项:
- 使用正向斜杠(/)或双反斜杠(\\)作为路径分隔符
- 确保Maya 2020已启动并且Script Editor可用
- 建议使用方法1，最简单可靠
- 路径中不要包含中文字符，避免编码问题
"""