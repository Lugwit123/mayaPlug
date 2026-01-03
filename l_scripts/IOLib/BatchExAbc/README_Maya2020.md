# Maya 2020 UI线程安全测试使用指南

## 🎯 环境要求

- **Maya版本**: Maya 2020
- **Python版本**: Python 2.7 (Maya 2020内置)
- **UI框架**: PySide2 (Maya 2020内置)
- **操作系统**: Windows/Linux/macOS

## 🚀 快速开始

### 方法1: 使用快速启动器（推荐）

在Maya 2020的Script Editor中执行：

```python
# 快速启动完整UI测试
exec(open(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc/maya2020_ui_test_launcher.py').read())
maya2020_ui_test()
```

或者：

```python
# 快速控制台测试（无UI界面）
exec(open(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc/maya2020_ui_test_launcher.py').read())
quick_maya2020_test()
```

### 方法2: 直接执行测试文件

```python
# 执行完整测试程序
exec(open(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc/test_pyside2_ui_thread.py').read())
```

### 方法3: 作为模块导入

```python
import sys
sys.path.append(r'd:/TD_Depot/plug_in/Lugwit_plug/mayaPlug/l_scripts/IOLib/BatchExAbc')

from test_pyside2_ui_thread import start_ui_thread_test, quick_test
start_ui_thread_test()  # 启动UI测试
# 或
quick_test()  # 控制台测试
```

## 🧪 测试功能说明

### 1. 主线程UI更新测试
- 验证正常的UI操作流程
- 测试项目、集、场、镜头下拉框更新
- 验证时间轴范围设置
- 测试网格布局填充

### 2. 子线程UI更新测试
- 验证[@thread_safe_ui_update](../ui_helper.py#L52-L76)装饰器功能
- 测试UI更新队列机制
- 验证批量UI更新
- 测试Maya特有功能（场景文件操作等）

### 3. 并发压力测试
- 多线程同时访问UI
- 验证线程安全机制的稳定性
- 测试高并发场景下的UI响应

## 📊 测试结果解读

### 成功标志
- ✓ 绿色勾号：测试通过
- 📊 统计信息：显示成功/失败比例
- 🎉 庆祝图标：所有测试通过

### 失败标志
- ✗ 红色叉号：测试失败
- ⚠️ 警告符号：部分功能异常
- 💻 控制台输出：详细错误信息

## 🔧 故障排除

### 常见问题

#### 1. PySide2导入失败
```
✗ Maya 2020应该包含PySide2，导入失败
```
**解决方案**：
- 确认Maya 2020版本
- 重启Maya
- 检查Maya安装完整性

#### 2. ui_helper模块导入失败
```
✗ 导入ui_helper模块失败
```
**解决方案**：
- 检查文件路径是否正确
- 确认ui_helper.py文件存在
- 检查sys.path设置

#### 3. 线程安全测试失败
```
✗ 子线程装饰器测试失败
```
**解决方案**：
- 检查Maya的utils.executeDeferred功能
- 验证threading模块可用性
- 查看详细错误日志

### 调试模式

启用详细日志：

```python
# 在执行测试前设置
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 💡 最佳实践

### 1. 测试前准备
- 确保Maya场景已保存
- 关闭不必要的Maya插件
- 清理Script Editor历史

### 2. 测试过程中
- 观察控制台输出
- 注意UI界面变化
- 记录异常情况

### 3. 测试后分析
- 查看测试结果统计
- 分析失败原因
- 验证线程安全功能

## 📝 技术细节

### 线程安全机制

1. **@thread_safe_ui_update装饰器**
   - 自动检测当前线程
   - 使用Maya的executeDeferred确保主线程执行
   - 提供异常处理和日志记录

2. **UIUpdateQueue队列**
   - 批量处理UI更新
   - 避免频繁线程切换
   - 防重复处理机制

3. **便捷更新方法**
   - safe_ui_update(): 单个UI更新
   - batch_ui_update(): 批量UI更新
   - 简化开发者使用流程

### Maya 2020特性支持

- **PySide2完全兼容**：利用Maya 2020内置PySide2
- **Python 2.7优化**：兼容Python 2.7语法和特性
- **Maya API集成**：支持Maya场景操作、工作空间路径等
- **版本检测**：自动识别Maya版本和环境

## 🔗 相关文件

- [ui_helper.py](./ui_helper.py) - 核心线程安全UI更新模块
- [test_pyside2_ui_thread.py](./test_pyside2_ui_thread.py) - 完整测试程序
- [maya2020_ui_test_launcher.py](./maya2020_ui_test_launcher.py) - 快速启动器

## 📞 技术支持

如遇到问题，请提供以下信息：
- Maya版本信息
- Python版本
- 错误日志
- 测试环境描述

---

**注意**：此测试工具专门针对Maya 2020环境优化，在其他Maya版本中可能需要适当调整。