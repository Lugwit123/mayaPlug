# coding:utf-8
from __future__ import print_function

import json
import os
import traceback
import datetime
import maya.cmds as cmds
import maya.api.OpenMayaUI as omui_api
try:
    import maya.api.OpenMaya as om_api
except ImportError:
    import maya.OpenMaya as om_api
# import Lugwit_Module as LM
# lprint = LM.lprint
import usualFunc
reload(usualFunc)
lprint = usualFunc.lprint



class AnalysisPanel:
    def __init__(self):
        self.window_name = "analysisPanel"
        self.window_title = u"物体分析与拍屏工具,场景修改后需要重启本窗口,多个视口时拍屏激活的视图摄像机"
        self.window_width = 400
        self.window_height = 600
        self.fps = 24
        self.selected_objects = []
        self.callback_camera = None
        self.speed_analysis = False  # 默认启用速度分析
        self.ground_analysis = False  # 默认不启用离地分析
        self.ground_threshold = 0.2
        self.ground_mesh = None  # 存储选择的地面物体
        self.output_dir = "D:/renders"
        self.company = "test_company"
        # Maya文件名
        self.maya_file_name = self.get_maya_file_name()
        # 从渲染设置获取默认分辨率
        self.current_camera = "persp"  # 当前视图摄像机
        try:
            default_width = cmds.getAttr("defaultResolution.width")
            default_height = cmds.getAttr("defaultResolution.height")
            self.resolution = (default_width, default_height)
        except:
            self.resolution = (1920, 1080)  # 备用默认值
        # HUD外观设置
        self.hud_font_size = "large"  # small, medium, large
        self.hud_font_color = [0.0, 1.0, 0.0]  # RGB绿色
        # HUD列表
        self.hud_list = ["speed_info", "ground_info", "frame_info", "camera_name",
                        "resolution_fps_info", "company_info", "focal_length_info", "date_info", "file_name_info"]
        # HUD显示状态
        self.hud_visible = False
        # 关闭窗口时是否删除HUD
        self.delete_hud_on_close = False  # 默认不清除HUD
        # 强制更新HUD列表
        self.froce_updata_hud_list = ["frame_info", "focal_length_info"]  # 需要强制更新的HUD名称列表
        # 窗口生命周期代码
        self.window_open_code = 'evaluationManager -mode "off";'
        self.window_close_code = 'evaluationManager -mode "parallel";'
        # self.file_name = "test_analysis"
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name)
        
        # 获取当前摄像机
        try:
            self.get_current_camera_info()
            self.current_camera = self.camera_name or "persp"
        except:
            self.current_camera = "persp"
            
        self.create_ui()
    
    def get_maya_file_name(self):
        """获取当前Maya文件名"""
        try:
            maya_file_path = cmds.file(q=True, sceneName=True)
            if maya_file_path:
                # 只返回文件名，不包含路径和扩展名
                file_name = os.path.splitext(os.path.basename(maya_file_path))[0]
                return file_name
            else:
                return "untitled"
        except:
            return "untitled"
    
    def create_update_expression(self):
        """根据froce_updata_hud_list创建表达式"""
        try:
            # 删除可能存在的旧表达式
            if cmds.objExists("updata_hud"):
                cmds.delete("updata_hud")
            
            if self.froce_updata_hud_list:
                # 构建表达式内容
                expression_commands = []
                for hud_name in self.froce_updata_hud_list:
                    expression_commands.append('headsUpDisplay -r "{}";'.format(hud_name))
                
                expression_content = "".join(expression_commands)
                
                # 创建表达式
                cmds.expression(name="updata_hud", string=expression_content)
                print(u"已创建HUD更新表达式: updata_hud")
                print(u"表达式内容: {}".format(expression_content))
            
        except Exception as e:
            print(u"创建HUD更新表达式失败: {}".format(str(e)))
    
    def delete_update_expression(self):
        """删除HUD更新表达式"""
        try:
            if cmds.objExists("updata_hud"):
                cmds.delete("updata_hud")
                print(u"已删除HUD更新表达式: updata_hud")
        except Exception as e:
            print(u"删除HUD更新表达式失败: {}".format(str(e)))

    def on_window_close(self, *args):
        """窗口关闭时的回调函数"""
        try:
            # 取消注册的时间线回调，传入from_window_close=True
            self.unregister_callback(from_window_close=True)
            print(u"窗口关闭，已自动取消注册时间线回调")
        except Exception as e:
            print(u"窗口关闭时取消注册失败: {}".format(str(e)))
        
        # 删除HUD更新表达式
        self.delete_update_expression()
        
        # 执行窗口关闭时的代码
        try:
            self.execute_lifecycle_code(self.window_close_code, "窗口关闭")
        except Exception as e:
            print(u"执行窗口关闭代码失败: {}".format(str(e)))
    
    def register_timeline_callback(self):
        """注册时间线回调，使用默认参数"""
        global time_changed_callback_id
        

        self.get_current_camera_info()
        fps = self.fps
        resolution = self.resolution_info or (1920, 1080)
        company = self.company
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        
        # 使用空的分析数据，因为只是为了HUD显示
        empty_data = {}
        total_frames = int(cmds.playbackOptions(q=True, max=True) - cmds.playbackOptions(q=True, min=True) + 1)
        
        # 保存回调参数
        self.callback_data = empty_data
        self.callback_total_frames = total_frames
        self.callback_fps = fps
        self.callback_resolution = resolution
        self.callback_company = company
        self.callback_date = date
        
        # 注册事件回调
        if hasattr(self, 'time_changed_callback_id') and self.time_changed_callback_id:
            # 如果已经有回调，先移除
            try:
                om_api.MMessage.removeCallback(self.time_changed_callback_id)
            except:
                pass
        
        time_changed_callback_id = om_api.MEventMessage.addEventCallback(
            "timeChanged",
            self.on_time_changed
        )
        self.time_changed_callback_id = time_changed_callback_id
        print(u"时间线回调注册成功，开始监听帧变化（主要用于速度和踩地分析）")
        print(u"注意：帧数和焦距信息现在使用属性绑定，会自动更新")

    # ui界面
    def create_ui(self):
        # 在窗口打开前创建HUD更新表达式
        self.create_update_expression()
        
        # 创建主窗口，添加窗口关闭回调
        cmds.window(
            self.window_name, 
            title=self.window_title, 
            widthHeight=(self.window_width, self.window_height),
            closeCommand=self.on_window_close  # 添加窗口关闭回调
        )
        main_layout = cmds.columnLayout(adj=True)

        # 标题
        cmds.text(label=self.window_title, height=30, font="boldLabelFont", align="center")

        # 创建Tab布局
        self.tab_layout = cmds.tabLayout()
        
        # 第一个Tab：主要功能（原有UI）
        self.main_tab = cmds.columnLayout(adj=True)
        self.create_main_ui()  # 创建原有的UI内容
        cmds.setParent(self.tab_layout)
        
        # 第二个Tab：设置信息
        self.settings_tab = cmds.columnLayout(adj=True)
        self.create_settings_tab()
        cmds.setParent(self.tab_layout)
        
        # 设置Tab标签
        cmds.tabLayout(self.tab_layout, edit=True, 
                      tabLabel=[(self.main_tab, u"主要功能"), 
                               (self.settings_tab, u"设置信息")])
        

        # UI创建完成后自动显示HUD
        try:
            self.show_hud_preview()
            # 更新按钮状态以反映HUD已显示
            if hasattr(self, 'toggle_hud_button') and cmds.button(self.toggle_hud_button, exists=True):
                cmds.button(self.toggle_hud_button, edit=True, label=u"隐藏HUD", backgroundColor=(0.8, 0.6, 0.4))
                self.hud_visible = True
            print("HUD automatically displayed on UI startup-------------------------------")
        except Exception as e:
            traceback.print_exc()


        # 界面创建完成后自动注册时间线回调
        try:
            self.register_timeline_callback()
            print(u"界面打开时自动注册时间线回调成功")
        except Exception as e:
            print(u"自动注册时间线回调失败: {}".format(str(e)))
        
        # 执行窗口打开时的代码
        try:
            self.execute_lifecycle_code(self.window_open_code, u"窗口打开")
        except Exception as e:
            print(u"执行窗口打开代码失败: {}".format(str(e)))
        
        cmds.showWindow()

    def create_main_ui(self):
        """创建原有的主要功能UI"""
        # --- 物体选择区域 ---
        cmds.frameLayout(label=u"物体选择", collapsable=True, collapse=False, mw=5, mh=5)
        cmds.columnLayout(adj=True)

        self.object_list = cmds.textScrollList(
            numberOfRows=4,
            allowMultiSelection=True,
            sc=self.update_selection
        )

        cmds.button(label=u"选中当前物体", command=self.populate_object_list)
        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout

        # --- 分析设置区域 ---
        cmds.frameLayout(label=u"分析设置", collapsable=True, collapse=False, mw=5, mh=5)
        cmds.columnLayout(adj=True)

        # 分析类型复选框和踩地阈值在同一行
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=1,
                       columnAttach=[(1, 'both', 5), (2, 'left', 10)])
        cmds.checkBoxGrp(
            "analysisTypeGrp",
            label=u"分析类型:",
            labelArray2=[u"速度分析", u"踩地分析"],
            numberOfCheckBoxes=2,
            value1=self.speed_analysis,
            value2=self.ground_analysis,
            cc=self.update_analysis_type
        )
        self.ground_threshold_field = cmds.floatFieldGrp(
            label=u"踩地阈值:",
            value1=self.ground_threshold,
            enable=False,
            pre=3,
            columnWidth=[(1, 40), (2, 50)]
        )
        cmds.setParent("..")  # rowLayout

        # 地面选择控件（简化）
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=2,
                       columnAttach=[(1, 'right', 5), (2, 'both', 5), (3, 'left', 5)])
        cmds.text(label=u"地面物体:")
        self.ground_mesh_menu = cmds.textScrollList(enable=False, numberOfRows=2, sc=self.update_ground_selection)
        cmds.button(label=u"绑定选中", command=self.set_selected_as_ground)
        cmds.setParent("..")  # rowLayout


        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout

        # --- 基础信息区域 ---
        cmds.frameLayout(label=u"基础信息", collapsable=True, collapse=False, mw=5, mh=5)
        cmds.columnLayout(adj=True)
        
        # 在同一行
        # 一行布局：摄像机、公司名、分辨率
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=3,
                       columnAttach=[(1, 'both', 5), (2, 'both', 5), (3, 'both', 5)])
        self.camera_field = cmds.textFieldGrp(
            label=u"摄像机:",
            text=self.current_camera,
            editable=False,
            columnWidth=[(1, 40), (2, 140)]
        )
        self.company_field = cmds.textFieldGrp(
            label=u"公司名:",
            text=self.company,
            columnWidth=[(1, 40), (2, 140)],
            changeCommand=self.on_company_name_changed
        )
        self.resolution_field = cmds.textFieldGrp(
            label=u"分辨率:",
            text="{}x{}".format(self.resolution[0], self.resolution[1]),
            editable=False,
            columnWidth=[(1, 40), (2, 140)]
        )
        cmds.setParent("..")  # rowLayout
        
        # 第四行：刷新按钮
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=3,
                       columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'both', 5)])
        cmds.button(label=u"刷新摄像机", width=80, command=self.refresh_camera_info)
        cmds.button(label=u"刷新分辨率", width=80, command=self.refresh_resolution_info)
        cmds.text(label="")  # 占位符
        cmds.setParent("..")  # rowLayout

        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout

        # 输出路径
        cmds.frameLayout(label=u"输出设置", collapsable=True, collapse=False, mw=5, mh=5)
        cmds.columnLayout(adj=True)
        
        # 输出路径文本框
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2,
                       columnAttach=[(1, 'right', 5), (2, 'both', 5)])
        cmds.text(label=u"路径:")
        self.output_path_field = cmds.textField(text=self.get_expected_video_path())
        cmds.setParent("..")  # rowLayout
        
        # 操作按钮
        cmds.rowLayout(numberOfColumns=3, adjustableColumn=3,
                       columnAttach=[(1, 'left', 5), (2, 'left', 5), (3, 'left', 5)])
        cmds.button(label=u"浏览", width=50, command=self.browse_output_dir)
        cmds.button(label=u"打开目录", width=60, command=self.open_output_dir)
        cmds.button(label=u"QuickTime播放", width=80, command=self.play_with_quicktime)
        cmds.setParent("..")  # rowLayout
        
        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout

        # ===== HUD 设置 =====
        cmds.frameLayout(label=u"HUD设置", collapsable=True, collapse=False, mw=5, mh=5)
        cmds.columnLayout(adj=True)
        cmds.rowLayout(numberOfColumns=1, adjustableColumn=1,
                       columnAttach=[(1, 'both', 5)])
        cmds.button(
            label=u"清除所有HUD",
            height=40,
            command=self.remove_sg_hud
        )
        cmds.setParent("..")  # rowLayout
        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout

        # --- 拍屏按钮 ---
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2,
                       columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        self.toggle_hud_button = cmds.button(
            label=u"显示HUD",
            height=40,
            command=self.toggle_hud_display,
            backgroundColor=(0.4, 0.6, 0.8)
        )
        cmds.button(
            label=u"执行拍屏分析",
            height=40,
            command=self.execute_playblast,
            backgroundColor=(0.3, 0.6, 0.3)
        )
        cmds.setParent("..")  # rowLayout

    def create_settings_tab(self):
        """创建设置信息Tab页"""
        # 工具信息
        cmds.frameLayout(label=u"工具信息", collapsable=True, collapse=True, mw=5, mh=5)
        cmds.columnLayout(adj=True)
        
        cmds.text(label=u"工具名称: 物体分析与拍屏工具", align="left")
        cmds.text(label=u"版本: v1.0", align="left")
        cmds.text(label=u"作者: TYYF 研发团队", align="left")
        cmds.text(label=u"更新日期: 2024-08-18", align="left")
        
        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout
        
        # 当前设置信息
        cmds.frameLayout(label=u"当前设置", collapsable=True, collapse=True, mw=5, mh=5)
        cmds.columnLayout(adj=True)
        
        # 获取Maya信息
        maya_version = cmds.about(version=True)
        maya_product = cmds.about(product=True)
        current_unit = cmds.currentUnit(query=True, linear=True)
        time_unit = cmds.currentUnit(query=True, time=True)
        
        cmds.text(label=u"Maya 版本: {} {}".format(maya_product, maya_version), align="left")
        cmds.text(label=u"线性单位: {}".format(current_unit), align="left")
        cmds.text(label=u"时间单位: {}".format(time_unit), align="left")
        
        # 设置信息更新按钮
        cmds.button(label=u"刷新设置信息", command=self.refresh_settings_info)
        
        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout
        
        # 分析配置信息
        cmds.frameLayout(label=u"分析配置", collapsable=True, collapse=True, mw=5, mh=5)
        cmds.columnLayout(adj=True)
        
        # 显示当前配置
        self.config_text = cmds.scrollField(
            text=self.get_current_config_text(),
            height=150,
            editable=False,
            wordWrap=True
        )
        
        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout
        
        # HUD外观设置
        cmds.frameLayout(label=u"HUD外观设置", collapsable=True, collapse=False, mw=5, mh=5)
        cmds.columnLayout(adj=True)
        
        # 字体大小设置
        self.hud_font_size_menu = cmds.optionMenuGrp(
            label=u"字体大小:",
            columnWidth=[(1, 80), (2, 100)],
            cc=self.update_hud_font_size
        )
        cmds.menuItem(label=u"小")
        cmds.menuItem(label=u"大")
        # 设置默认值
        if self.hud_font_size == "small":
            cmds.optionMenuGrp(self.hud_font_size_menu, edit=True, select=1)
        else:  # large 或其他值都默认为大
            cmds.optionMenuGrp(self.hud_font_size_menu, edit=True, select=2)
        
        # 字体颜色设置
        self.hud_color_slider = cmds.colorSliderGrp(
            label=u"字体颜色:",
            rgb=self.hud_font_color,
            columnWidth=[(1, 80), (2, 200)],
            cc=self.update_hud_font_color
        )
        
        # 预设颜色按钮 - 第一行
        cmds.rowLayout(numberOfColumns=10, adjustableColumn=10,
                       columnAttach=[(1, 'left', 0), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5), (5, 'left', 5)])
        cmds.text(label=u"预设颜色:")
        cmds.button(label=u"白色", width=35, command=lambda *args: self.set_preset_color([1.0, 1.0, 1.0]))
        cmds.button(label=u"黄色", width=35, command=lambda *args: self.set_preset_color([1.0, 1.0, 0.0]))
        cmds.button(label=u"绿色", width=35, command=lambda *args: self.set_preset_color([0.0, 1.0, 0.0]))
        cmds.button(label=u"红色", width=35, command=lambda *args: self.set_preset_color([1.0, 0.0, 0.0]))
        # cmds.setParent("..")  # rowLayout
        
        # # 预设颜色按钮 - 第二行
        # cmds.rowLayout(numberOfColumns=5, adjustableColumn=5,
        #                columnAttach=[(1, 'left', 0), (2, 'left', 5), (3, 'left', 5), (4, 'left', 5), (5, 'left', 5)])
        # cmds.text(label="")
        cmds.button(label=u"蓝色", width=35, command=lambda *args: self.set_preset_color([0.0, 0.0, 1.0]))
        cmds.button(label=u"紫色", width=35, command=lambda *args: self.set_preset_color([1.0, 0.0, 1.0]))
        cmds.button(label=u"青色", width=35, command=lambda *args: self.set_preset_color([0.0, 1.0, 1.0]))
        cmds.button(label=u"灰色", width=35, command=lambda *args: self.set_preset_color([0.5, 0.5, 0.5]))
        cmds.setParent("..")  # rowLayout
        
        # 应用设置按钮
        cmds.button(
            label=u"应用HUD外观设置",
            height=30,
            command=self.apply_hud_appearance,
            backgroundColor=(0.4, 0.7, 0.4)
        )
        
        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout
        
        # 系统信息
        cmds.frameLayout(label=u"系统信息", collapsable=True, collapse=False, mw=5, mh=5)
        cmds.columnLayout(adj=True)
        
        # 获取系统信息
        os_info = cmds.about(operatingSystem=True)
        
        cmds.text(label=u"操作系统: {}".format(os_info), align="left")
        cmds.text(label=u"Python 版本: 2.7.x", align="left")
        
        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout
        
        # 窗口生命周期代码设置
        cmds.frameLayout(label=u"窗口生命周期代码", collapsable=True, collapse=False, mw=5, mh=5)
        cmds.columnLayout(adj=True)
        
        # 窗口打开时运行的代码
        cmds.text(label=u"窗口打开时运行的代码:", align="left")
        self.window_open_code_field = cmds.scrollField(
            text='evaluationManager -mode "off";',
            height=40,
            wordWrap=True,
            annotation=u"窗口打开时自动执行的MEL代码"
        )
        
        cmds.separator(height=10)
        
        # 窗口关闭时运行的代码
        cmds.text(label=u"窗口关闭时运行的代码:", align="left")
        self.window_close_code_field = cmds.scrollField(
            text='evaluationManager -mode "parallel";',
            height=40,
            wordWrap=True,
            annotation=u"窗口关闭时自动执行的MEL代码"
        )
        
        cmds.separator(height=10)
        
        # 应用按钮
        cmds.rowLayout(numberOfColumns=2, adjustableColumn=2,
                       columnAttach=[(1, 'both', 5), (2, 'both', 5)])
        cmds.button(
            label=u"应用设置",
            height=25,
            command=self.apply_lifecycle_code,
            backgroundColor=(0.4, 0.7, 0.4),
            annotation=u"保存当前的生命周期代码设置"
        )
        cmds.button(
            label=u"重置为默认",
            height=25,
            command=self.reset_lifecycle_code,
            backgroundColor=(0.7, 0.7, 0.4),
            annotation=u"重置为默认的生命周期代码"
        )
        cmds.setParent("..")  # rowLayout
        
        cmds.setParent("..")  # columnLayout
        cmds.setParent("..")  # frameLayout

    def apply_lifecycle_code(self, *args):
        """应用生命周期代码设置"""
        try:
            # 获取输入框中的代码
            self.window_open_code = cmds.scrollField(self.window_open_code_field, query=True, text=True)
            self.window_close_code = cmds.scrollField(self.window_close_code_field, query=True, text=True)
            
            print(u"已保存生命周期代码设置:")
            print(u"窗口打开时: {}".format(self.window_open_code))
            print(u"窗口关闭时: {}".format(self.window_close_code))
            
            cmds.confirmDialog(
                title=u"设置已保存",
                message=u"生命周期代码设置已保存！\n\n窗口打开时:\n{}\n\n窗口关闭时:\n{}".format(
                    self.window_open_code, self.window_close_code),
                button=[u"确定"],
                defaultButton=u"确定"
            )
            
        except Exception as e:
            cmds.warning(u"保存生命周期代码失败: {}".format(str(e)))

    def reset_lifecycle_code(self, *args):
        """重置生命周期代码为默认值"""
        try:
            # 重置为默认代码
            default_open_code = 'evaluationManager -mode "off";'
            default_close_code = 'evaluationManager -mode "parallel";'
            
            cmds.scrollField(self.window_open_code_field, edit=True, text=default_open_code)
            cmds.scrollField(self.window_close_code_field, edit=True, text=default_close_code)
            
            # 同时更新实例变量
            self.window_open_code = default_open_code
            self.window_close_code = default_close_code
            
            print(u"已重置生命周期代码为默认值")
            
        except Exception as e:
            cmds.warning(u"重置生命周期代码失败: {}".format(str(e)))

    def execute_lifecycle_code(self, code, context):
        """执行生命周期代码"""
        if not code or code.strip() == "":
            return
            
        try:
            import maya.mel as mel
            # 执行MEL代码
            mel.eval(code)
            print(u"{}时执行代码成功: {}".format(context, code))
        except Exception as e:
            print(u"{}时执行代码失败: {} - 错误: {}".format(context, code, str(e)))
 
    def refresh_settings_info(self, *args):
        """刷新设置信息"""
        # 更新配置信息文本
        if hasattr(self, 'config_text'):
            cmds.scrollField(self.config_text, edit=True, text=self.get_current_config_text())
        
    def get_current_config_text(self):
        """获取当前配置信息文本"""
        config_info = []
        config_info.append(u"• 速度分析: {}".format(u"开启" if self.speed_analysis else u"关闭"))
        config_info.append(u"• 踩地分析: {}".format(u"开启" if self.ground_analysis else u"关闭"))
        config_info.append(u"• 踩地阈值: {}".format(self.ground_threshold))
        config_info.append(u"• 选中物体数量: {}".format(len(self.selected_objects)))
        config_info.append(u"• 地面物体: {}".format(self.ground_mesh if self.ground_mesh else u"未设置"))
        config_info.append(u"• 输出目录: {}".format(self.output_dir))
        config_info.append(u"• 公司名称: {}".format(self.company))
        config_info.append(u"• 当前摄像机: {}".format(self.current_camera))
        config_info.append(u"• HUD字体大小: {}".format(self.hud_font_size))
        config_info.append(u"• HUD字体颜色: RGB({:.1f}, {:.1f}, {:.1f})".format(
            self.hud_font_color[0], self.hud_font_color[1], self.hud_font_color[2]))
        
        # 获取摄像机信息
        try:
            self.get_current_camera_info()
            config_info.append(u"• 当前摄像机: {}".format(self.camera_name or u"未知"))
            config_info.append(u"• 焦距: {}mm".format(self.focal_length or u"未知"))
            config_info.append(u"• FPS: {}".format(self.fps or u"未知"))
            resolution = self.resolution_info or [0, 0]
            config_info.append(u"• 分辨率: {}x{}".format(resolution[0], resolution[1]))
        except:
            config_info.append(u"• 摄像机信息: 获取失败")
        
        # 获取时间轴信息
        try:
            start_frame = int(cmds.playbackOptions(q=True, min=True))
            end_frame = int(cmds.playbackOptions(q=True, max=True))
            current_frame = int(cmds.currentTime(query=True))
            config_info.append(u"• 时间范围: {}-{} ({}帧)".format(start_frame, end_frame, end_frame - start_frame + 1))
            config_info.append(u"• 当前帧: {}".format(current_frame))
        except:
            config_info.append(u"• 时间轴信息: 获取失败")
        
        return u"\n".join(config_info)

    def update_hud_font_size(self, *args):
        """更新HUD字体大小并自动应用到所有HUD"""
        selected_index = cmds.optionMenuGrp(self.hud_font_size_menu, query=True, select=True)
        font_sizes = ["small", "large"]  # 只有小和大两个选项
        self.hud_font_size = font_sizes[selected_index - 1]
        
        # 自动应用到所有现有的HUD
        self.apply_font_size_to_existing_huds()
        
        # 刷新配置信息显示
        if hasattr(self, 'config_text'):
            cmds.scrollField(self.config_text, edit=True, text=self.get_current_config_text())
        
    def update_hud_font_color(self, *args):
        """更新HUD字体颜色并自动应用到所有HUD"""
        self.hud_font_color = cmds.colorSliderGrp(self.hud_color_slider, query=True, rgb=True)
        
        # 自动应用到所有现有的HUD
        self.apply_color_to_existing_huds()
        
        # 刷新配置信息显示
        if hasattr(self, 'config_text'):
            cmds.scrollField(self.config_text, edit=True, text=self.get_current_config_text())
        
    def set_preset_color(self, color):
        """设置预设颜色并自动应用"""
        self.hud_font_color = color
        cmds.colorSliderGrp(self.hud_color_slider, edit=True, rgb=color)
        
        # 自动应用到所有现有的HUD
        self.apply_color_to_existing_huds()
        
        # 刷新配置信息显示
        if hasattr(self, 'config_text'):
            cmds.scrollField(self.config_text, edit=True, text=self.get_current_config_text())
        
    def apply_hud_appearance(self, *args):
        """应用HUD外观设置"""
        # 获取所有存在的HUD
        updated_huds = []
        for hud_name in self.hud_list:
            if cmds.headsUpDisplay(hud_name, exists=True):
                try:
                    # 直接修改现有HUD的外观设置
                    cmds.headsUpDisplay(
                        hud_name,
                        edit=True,
                        blockSize="small",
                        labelFontSize=self.hud_font_size,
                        dataFontSize=self.hud_font_size
                    )
                    updated_huds.append(hud_name)
                except Exception as e:
                    print("Update HUD appearance failed:", hud_name, str(e))
        
        # 应用颜色设置
        self.apply_color_to_existing_huds()
        
        if updated_huds:
            cmds.confirmDialog(
                title=u"应用成功",
                message=u"已更新 {} 个HUD的外观设置\n字体大小: {}\n字体颜色: RGB({:.1f}, {:.1f}, {:.1f})".format(
                    len(updated_huds), 
                    self.hud_font_size,
                    self.hud_font_color[0], 
                    self.hud_font_color[1], 
                    self.hud_font_color[2]
                ),
                button=[u"确定"],
                defaultButton=u"确定"
            )
        else:
            cmds.warning(u"没有找到任何HUD，请先执行拍屏分析后再设置")
        
    def apply_font_size_to_existing_huds(self):
        """应用字体大小到所有现有的HUD"""
        updated_count = 0
        for hud_name in self.hud_list:
            if cmds.headsUpDisplay(hud_name, exists=True):
                try:
                    # 直接修改现有HUD的字体大小设置
                    cmds.headsUpDisplay(
                        hud_name,
                        edit=True,
                        blockSize="small",
                        labelFontSize=self.hud_font_size,
                        dataFontSize=self.hud_font_size
                    )
                    updated_count += 1
                except Exception as e:
                    # 使用简单的错误处理，避免编码问题
                    print("Update HUD failed:", hud_name, str(e))
        
        if updated_count > 0:
            print("Updated HUD font size:", updated_count, "items, size:", self.hud_font_size)
        elif self.hud_visible:
            print("No HUDs found to update font size")
        # 如果HUD不可见，不显示任何消息
            
    def apply_color_to_existing_huds(self):
        """应用字体颜色到所有现有的HUD（通过displayColor命令）"""
        try:
            # 使用Maya的displayColor命令设置HUD颜色
            # 根据RGB值计算最接近的颜色索引
            color_index = self.rgb_to_color_index(self.hud_font_color)
            
            # 设置HUD标签和数值的颜色
            cmds.displayColor('headsUpDisplayLabels', color_index, c=1, dormant=1)
            cmds.displayColor('headsUpDisplayValues', color_index, c=1, dormant=1)
            
            print("HUD color updated to index:", color_index, "RGB:", self.hud_font_color)
                
        except Exception as e:
            print("HUD color update failed:", repr(e))
    
    def rgb_to_color_index(self, rgb_color):
        """将RGB颜色转换为最接近的Maya颜色索引"""
        # Maya常用颜色索引和RGB值的对应关系
        color_map = {
            16: [1.0, 1.0, 1.0],  # 白色
            17: [1.0, 1.0, 0.0],  # 黄色
            14: [0.0, 1.0, 0.0],  # 绿色
            13: [1.0, 0.0, 0.0],  # 红色
            6:  [0.0, 0.0, 1.0],  # 蓝色
            9:  [1.0, 0.0, 1.0],  # 紫色
            18: [0.0, 1.0, 1.0],  # 青色
            1:  [0.0, 0.0, 0.0],  # 黑色
            3:  [0.5, 0.5, 0.5],  # 灰色
        }
        
        # 计算距离最小的颜色
        min_distance = float('inf')
        closest_index = 16  # 默认白色
        
        for index, color in color_map.items():
            # 计算欧几里得距离
            distance = sum((rgb_color[i] - color[i]) ** 2 for i in range(3)) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_index = index
        
        return closest_index

    def toggle_hud_display(self, *args):
        """切换HUD显示状态"""
        try:
            if self.hud_visible:
                # 当前显示中，隐藏HUD
                self.clear_hud()
                cmds.button(self.toggle_hud_button, edit=True, label=u"显示HUD", backgroundColor=(0.4, 0.6, 0.8))
                self.hud_visible = False
                print("HUD hidden")
            else:
                # 当前隐藏，显示HUD
                self.show_hud_preview()
                cmds.button(self.toggle_hud_button, edit=True, label=u"隐藏HUD", backgroundColor=(0.8, 0.6, 0.4))
                self.hud_visible = True
                print("HUD displayed")
                
        except Exception as e:
            traceback.print_exc()
            cmds.warning(u"切换HUD显示失败: {}".format(repr(e)))
    
    def clear_hud(self, *args):
        """清理所有HUD（不仅仅是插件创建的）"""
        try:
            # 获取所有存在的HUD
            all_huds = cmds.headsUpDisplay(listHeadsUpDisplays=True) or []
            
            if all_huds:
                print("Found {} HUDs to remove: {}".format(len(all_huds), all_huds))
                # 清理所有HUD
                for hud in all_huds:
                    try:
                        if cmds.headsUpDisplay(hud, exists=True):
                            cmds.headsUpDisplay(hud, remove=True)
                            print("Removed HUD:", hud)
                    except Exception as e:
                        print("Failed to remove HUD {}: {}".format(hud, str(e)))
                        
                print("All HUDs cleared")
            else:
                print("No HUDs found to clear")
                
        except Exception as e:
            print("Clear HUD failed:", str(e))
            # 备用清理方案：仍然尝试清理插件定义的HUD
            for hud_block in self.hud_list:
                try:
                    if cmds.headsUpDisplay(hud_block, exists=True):
                        cmds.headsUpDisplay(hud_block, remove=True)
                        print("Fallback removed HUD:", hud_block)
                except:
                    pass
    
    def create_huds(self):
        """创建所有HUD，使用属性绑定方式实现自动更新"""
        # 获取当前激活摄像机用于属性绑定
        current_camera = self.get_current_active_camera()
        
        # 使用hud_list创建HUD，采用更高效的属性绑定方式
        for hud_name in self.hud_list:
            if hud_name == "speed_info":
                cmds.headsUpDisplay(hud_name,
                                    section=3, block=1,
                                    blockSize="small",
                                    label='------',
                                    labelFontSize=self.hud_font_size,
                                    dataFontSize=self.hud_font_size,
                                    allowOverlap=True)
            elif hud_name == "ground_info" and self.ground_analysis:
                # 只有在启用踩地分析时才创建ground_info HUD
                cmds.headsUpDisplay(hud_name,
                                    section=3, block=2,
                                    blockSize="small",
                                    label='------',
                                    labelFontSize=self.hud_font_size,
                                    dataFontSize=self.hud_font_size,
                                    allowOverlap=True)
            elif hud_name == "frame_info":
                # 直接绑定时间属性，自动跟随时间线变化
                cmds.headsUpDisplay(hud_name,
                                    section=9, block=1,
                                    blockSize="small",
                                    label="Frames:",
                                    labelFontSize=self.hud_font_size,
                                    dataFontSize=self.hud_font_size,
                                    command=self.get_frame_info,
                                    event='timeChanged' ,
                                    allowOverlap=True)
            elif hud_name == "camera_name":
                # 使用Maya内置的cameraNames预设

                cmds.headsUpDisplay(hud_name,
                                    section=0, block=1,
                                    blockSize="small",
                                    preset="cameraNames",  # 使用Maya内置的cameraNames预设
                                    labelFontSize=self.hud_font_size,
                                    dataFontSize=self.hud_font_size,
                                    allowOverlap=True)
                print(u"使用Maya内置cameraNames预设创建HUD")

            elif hud_name == "resolution_fps_info":
                cmds.headsUpDisplay(hud_name,
                                    section=8, block=1,
                                    blockSize="small",
                                    label="------",
                                    labelFontSize=self.hud_font_size,
                                    dataFontSize=self.hud_font_size,
                                    allowOverlap=True)
            elif hud_name == "company_info":
                cmds.headsUpDisplay(hud_name,
                                    section=4, block=1,
                                    blockSize="small",
                                    label="------",
                                    labelFontSize=self.hud_font_size,
                                    dataFontSize=self.hud_font_size,
                                    allowOverlap=True)
            elif hud_name == "focal_length_info":
                print (u"创建焦距信息HUD")
                cmds.headsUpDisplay(hud_name,
                                    section=5, block=1,
                                    blockSize="small",
                                    label="",
                                    dataWidth = 10,
                                    labelFontSize=self.hud_font_size,
                                    dataFontSize=self.hud_font_size,
                                    command=self.get_current_focal_length,
                                    event='timeChanged' ,
                                    allowOverlap=True)
            elif hud_name == "date_info":
                cmds.headsUpDisplay(hud_name,
                                    section=6, block=1,
                                    blockSize="small",
                                    label="------",
                                    labelFontSize=self.hud_font_size,
                                    dataFontSize=self.hud_font_size,
                                    allowOverlap=True)
            elif hud_name == "file_name_info":
                cmds.headsUpDisplay(hud_name,
                                    section=0, block=2,  # 与摄像机名称相同section，但block为2（下方）
                                    blockSize="small",
                                    label="------",
                                    labelFontSize=self.hud_font_size,
                                    dataFontSize=self.hud_font_size,
                                    allowOverlap=True)
    
    def get_current_active_camera(self):
        """获取当前激活的摄像机名称（用于属性绑定）"""
        view = omui_api.M3dView.active3dView()
        camera_path = view.getCamera()
        camera_fn = om_api.MFnCamera(camera_path)

        # 摄像机名称
        self.camera_name = camera_fn.name()
        return self.camera_name

    
    def get_current_focal_length(self):
        """获取当前摄像机的焦距（用于HUD command参数）"""
        try:
            camera = self.get_current_active_camera()
            if camera and cmds.objExists(camera):
                focal_length = cmds.getAttr(camera + ".focalLength")
                return "Focal Length: {}".format(str(focal_length)[:2])
            else:
                return "--"
        except Exception as e:
            return "Error: {}".format(str(e))
    
    def get_fps_from_time_unit(self):
        """从Maya时间单位获取帧速率"""
        try:
            unit = cmds.currentUnit(query=True, time=True)
            fps_table = {
                "game": 15, "film": 24, "pal": 25, "ntsc": 30,
                "show": 48, "palf": 50, "ntscf": 60,
                "2fps": 2, "3fps": 3, "4fps": 4, "5fps": 5,
                "6fps": 6, "8fps": 8, "10fps": 10, "12fps": 12,
                "16fps": 16, "20fps": 20, "40fps": 40, "75fps": 75,
                "80fps": 80, "100fps": 100, "120fps": 120,
                "125fps": 125, "150fps": 150, "200fps": 200,
                "240fps": 240, "250fps": 250, "300fps": 300,
                "375fps": 375, "400fps": 400, "500fps": 500,
                "600fps": 600, "750fps": 750, "1200fps": 1200,
                "1500fps": 1500, "2000fps": 2000, "3000fps": 3000,
                "6000fps": 6000
            }
            return fps_table.get(unit, 24)
        except:
            return 24  # 默认值

    def get_frame_info(self):
        """获取详细的帧信息（起始帧/当前帧/总帧数）"""
        try:
            current_frame = int(cmds.currentTime(query=True))
            start_frame = int(cmds.playbackOptions(q=True, min=True))
            end_frame = int(cmds.playbackOptions(q=True, max=True))
            total_frames = end_frame - start_frame + 1
            return "{}/{}/{}f".format(start_frame, current_frame, total_frames)
        except Exception as e:
            return "Error: {}".format(str(e))

    
    def update_hud_preview_content(self):
        """更新HUD为预览内容，适配属性绑定方式"""
        # 使用hud_list更新HUD内容为预览文本
        for hud_name in self.hud_list:
            if cmds.headsUpDisplay(hud_name, exists=True):
                if hud_name == "speed_info":
                    cmds.headsUpDisplay(hud_name, edit=True, label=u'速度: -- cm/s')
                elif hud_name == "ground_info" and self.ground_analysis:
                    # 只有在启用踩地分析时才更新ground_info HUD
                    cmds.headsUpDisplay(hud_name, edit=True, label=u'踩地')
                elif hud_name == "frame_info":
                    # frame_info现在使用attributeChange绑定，会自动显示当前帧
                    # 不需要手动设置label，让其显示真实的当前帧数
                    pass  # HUD会自动显示当前时间轴位置
                elif hud_name == "camera_name":
                    # camera_info使用command绑定，会自动显示当前摄像机
                    # 不需要手动设置，让其显示真实的当前摄像机
                    pass  # HUD会自动显示当前激活的摄像机
                elif hud_name == "resolution_fps_info":

                                         # 获取真实的分辨率和帧率
                     width = cmds.getAttr("defaultResolution.width")
                     height = cmds.getAttr("defaultResolution.height")
                     fps = self.get_fps_from_time_unit()
                     cmds.headsUpDisplay(hud_name, edit=True, label="{}*{}    FPS: {}".format(int(width), int(height), int(fps)))

                elif hud_name == "company_info":
                    cmds.headsUpDisplay(hud_name, edit=True, label=self.company)
                elif hud_name == "date_info":
                    import datetime
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    cmds.headsUpDisplay(hud_name, edit=True, label="Date: {}".format(current_date))
                elif hud_name == "file_name_info":
                    # 更新文件名信息
                    current_file_name = self.get_maya_file_name()
                    self.maya_file_name = current_file_name
                    cmds.headsUpDisplay(hud_name, edit=True, label="File: {}".format(current_file_name))

    def show_hud_preview(self, *args):
        """显示HUD预览，使用现有HUD或创建新HUD"""
        self.clear_hud()  # 先清除现有的，保证一致性
        self.create_huds()


        # 更新HUD为预览内容
        self.update_hud_preview_content()

        # 应用颜色设置
        self.apply_color_to_existing_huds()


    def populate_object_list(self, *args):
        """仅添加当前选中的 transform 类型物体到列表中"""
        cmds.textScrollList(self.object_list, e=True, removeAll=True)
        selection = cmds.ls(selection=True, type='transform', long=True)

        if not selection:
            cmds.warning(u"未选中任何 transform 类型物体")
            return

        for obj in selection:
            cmds.textScrollList(self.object_list, e=True, append=obj)
        self.selected_objects = selection


    def update_selection(self, *args):
        """更新选中的物体列表"""
        selected = cmds.textScrollList(self.object_list, query=True, selectItem=True) or []
        self.selected_objects = selected


    def set_selected_as_ground(self, *args):
        selection = cmds.ls(selection=True, type='transform', long=True)
        if not selection:
            cmds.warning(u"未选择地面物体")
            return

        ground = selection[0]  # 只取第一个
        self.ground_mesh = ground

        cmds.textScrollList(self.ground_mesh_menu, edit=True, removeAll=True)
        cmds.textScrollList(self.ground_mesh_menu, edit=True, append=ground)
        cmds.textScrollList(self.ground_mesh_menu, edit=True, selectItem=ground)


    def update_ground_selection(self, *args):
        """更新地面物体选择"""
        self.ground_mesh = cmds.textScrollList(self.ground_mesh_menu, query=True)


    def update_analysis_type(self, *args):
        """更新分析类型"""
        self.speed_analysis = cmds.checkBoxGrp("analysisTypeGrp", query=True, value1=True)
        self.ground_analysis = cmds.checkBoxGrp("analysisTypeGrp", query=True, value2=True)

        # 启用/禁用踩地相关设置
        cmds.floatFieldGrp(
            self.ground_threshold_field,
            edit=True,
            enable=self.ground_analysis
        )
        cmds.textScrollList(
            self.ground_mesh_menu,
            edit=True,
            enable=self.ground_analysis
        )
        
        # 如果当前有HUD显示，重新创建HUD以确保ground_info的显示状态正确
        if self.hud_visible:
            self.clear_hud()
            self.show_hud_preview()
            print("HUD recreated due to analysis type change")


    def refresh_camera_info(self, *args):
        """刷新摄像机信息"""
        try:
            self.get_current_camera_info()
            self.current_camera = self.camera_name or "persp"
            cmds.textFieldGrp(self.camera_field, edit=True, text=self.current_camera)
            print(u"摄像机信息已刷新: {}".format(self.current_camera))
        except Exception as e:
            cmds.warning(u"刷新摄像机信息失败: {}".format(str(e)))

    def refresh_resolution_info(self, *args):
        """刷新分辨率信息"""
        try:
            # 从渲染设置获取最新分辨率
            width = cmds.getAttr("defaultResolution.width")
            height = cmds.getAttr("defaultResolution.height")
            self.resolution = (width, height)
            
            # 更新UI显示
            resolution_text = "{}x{}".format(width, height)
            cmds.textFieldGrp(self.resolution_field, edit=True, text=resolution_text)
            print(u"分辨率信息已刷新: {}".format(resolution_text))
        except Exception as e:
            cmds.warning(u"刷新分辨率信息失败: {}".format(str(e)))
    
    def on_company_name_changed(self, *args):
        """公司名变更时的回调函数"""
        try:
            # 更新内部状态
            new_company_name = cmds.textFieldGrp(self.company_field, query=True, text=True)
            self.company = new_company_name
            
            # 如果当前HUD可见，实时更新company_info HUD
            if cmds.headsUpDisplay('company_info', exists=True):
                company_info_text = u"{}".format(self.company)
                cmds.headsUpDisplay('company_info', edit=True, label=company_info_text)
                print(u"公司信息已更新: {}".format(self.company))
            
            # 刷新配置信息显示
            if hasattr(self, 'config_text'):
                cmds.scrollField(self.config_text, edit=True, text=self.get_current_config_text())
                
        except Exception as e:
            cmds.warning(u"更新公司信息失败: {}".format(str(e)))
            
    def browse_output_dir(self, *args):
        """浏览输出目录"""
        path = cmds.fileDialog2(fileMode=3, dialogStyle=2)
        if path:
            cmds.textField(self.output_path_field, edit=True, text=self.get_expected_video_path(path[0]))
            self.output_dir = path[0]
            
    def get_expected_video_path(self, output_dir=None):
        """获取预期的mov文件完整路径"""
        if output_dir is None:
            output_dir = self.output_dir
            
        # 生成文件名逻辑与 playblast_with_analysis 中相同
        maya_file_path = cmds.file(q=True, sceneName=True)
        if not maya_file_path:
            file_base_name = "untitled"
        else:
            file_base_name = os.path.splitext(os.path.basename(maya_file_path))[0]
        
        return os.path.join(output_dir, "{}.mov".format(file_base_name))
            
    def open_output_dir(self, *args):
        """打开输出目录"""
        import subprocess
        import platform
        
        # 获取当前输出路径（可能是完整文件路径）
        current_path = cmds.textField(self.output_path_field, query=True, text=True)
        
        # 如果是文件路径，提取目录部分
        if current_path.endswith('.mov') or current_path.endswith('.mp4'):
            directory_path = os.path.dirname(current_path)
        else:
            directory_path = current_path
        
        if not os.path.exists(directory_path):
            cmds.warning(u"目录不存在: {}".format(directory_path))
            return
            
        try:
            # 根据操作系统打开文件管理器
            if platform.system() == "Windows":
                os.startfile(directory_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", directory_path])
            else:  # Linux
                subprocess.call(["xdg-open", directory_path])
                
            print(u"已打开目录: {}".format(directory_path))
        except Exception as e:
            cmds.warning(u"打开目录失败: {}".format(str(e)))
            
    def play_with_quicktime(self, video_path=None, *args):
        """使用QuickTime播放指定的mov文件"""
        import subprocess
        import platform
        
        # 如果没有提供路径参数，则从输入框获取
        if video_path is None:
            mov_file_path = cmds.textField(self.output_path_field, query=True, text=True)
        else:
            mov_file_path = video_path
        
        if not os.path.exists(mov_file_path):
            cmds.warning(u"mov文件不存在: {}".format(mov_file_path))
            return
            
        try:
            # 根据操作系统打开视频
            if platform.system() == "Windows":
                # Windows上使用注册表查找QuickTime的安装位置
                quicktime_path = self.find_quicktime_path()
                if quicktime_path:
                    try:
                        subprocess.Popen([quicktime_path, mov_file_path])
                        print(u"使用QuickTime播放视频: {}".format(mov_file_path))
                        return
                    except Exception as e:
                        print(u"QuickTime启动失败: {}".format(str(e)))
                

        except Exception as e:
            traceback.print_exc()
            cmds.warning(u"播放视频失败: {}".format(str(e)))
    

    def find_quicktime_path(self):
        """使用注册表查找QuickTime的安装路径"""
        import platform
        
        if platform.system() != "Windows":
            return None
            
        try:
            import _winreg as winreg  # Python 2.7
        except ImportError:
            try:
                import winreg  # Python 3.x
            except ImportError:
                print("Cannot import winreg module")
                return None
                
        # 优先搜索Uninstall注册表项（标准做法）
        uninstall_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        
        for uninstall_path in uninstall_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_path) as uninstall_key:
                    # 遍历所有已安装的程序
                    i = 0
                    while True:
                        try:
                            subkey_name = winreg.EnumKey(uninstall_key, i)
                            subkey_path = "{}\\{}".format(uninstall_path, subkey_name)
                            
                            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path) as app_key:
                                try:
                                    # 检查程序名称是否包含QuickTime
                                    display_name, _ = winreg.QueryValueEx(app_key, "DisplayName")
                                    if "quicktime" in display_name.lower():
                                        try:
                                            # 仅使用InstallLocation字段
                                            install_location, _ = winreg.QueryValueEx(app_key, "InstallLocation")
                                            quicktime_exe = os.path.join(install_location, "QuickTimePlayer.exe")
                                            if os.path.exists(quicktime_exe):
                                                print("Found QuickTime via Uninstall registry: {}".format(quicktime_exe))
                                                return quicktime_exe
                                        except (WindowsError, FileNotFoundError, OSError):
                                            pass  # 如果没有InstallLocation就跳过
                                except (WindowsError, FileNotFoundError, OSError):
                                    pass
                            i += 1
                        except WindowsError:
                            break  # 没有更多的子项
            except:
                continue

                
        # 如果注册表中找不到，尝试常见的安装路径
        common_paths = [
            r"C:\Program Files\QuickTime\QuickTimePlayer.exe",
            r"C:\Program Files (x86)\QuickTime\QuickTimePlayer.exe",
            r"C:\Program Files\Apple\QuickTime\QuickTimePlayer.exe",
            r"C:\Program Files (x86)\Apple\QuickTime\QuickTimePlayer.exe"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                print("Found QuickTime at common path: {}".format(path))
                return path
                

        print("QuickTime not found in registry or common paths")
        return None


    def execute_playblast(self, *args):
        """执行拍屏分析"""
        # 更新设置
        output_path = cmds.textField(self.output_path_field, query=True, text=True)
        # 如果是完整文件路径，提取目录部分
        if output_path.endswith('.mov') or output_path.endswith('.mp4'):
            self.output_dir = os.path.dirname(output_path)
        else:
            self.output_dir = output_path
        self.ground_threshold = cmds.floatFieldGrp(self.ground_threshold_field, query=True, value1=True)
        self.ground_mesh = cmds.textScrollList(self.ground_mesh_menu, query=True, selectItem=True)
        if self.ground_mesh:
            self.ground_mesh = self.ground_mesh[0]
        else:
            self.ground_mesh = None

        # 更新预设信息
        self.company = cmds.textFieldGrp(self.company_field, query=True, text=True)
        # 刷新摄像机信息
        self.current_camera = cmds.textFieldGrp(self.camera_field, query=True, text=True)
        # self.file_name = cmds.textFieldGrp(self.file_name_field, query=True, text=True)

        # 检查地面物体是否有效（只有在启用踩地分析且没有选中物体时才需要地面物体）
        if self.ground_analysis and not self.ground_mesh:
            cmds.warning(u"请选择地面物体")
            return
        
        # 如果没有选中物体，给出提示但允许继续
        if not self.selected_objects:
            print(u"没有选中分析物体，将执行无物体分析的拍屏")

        # 创建输出目录
        path = self.output_dir

        if not os.path.exists(path):
            os.makedirs(path)  # 目录不存在时创建
        else:
            print("Directory already exists, skip creation")

        # 执行拍屏
        self.playblast_with_analysis()

    def remove_sg_hud(self, *args):
        """清理所有HUD并更新按钮状态"""
        self.clear_hud()
        # 更新按钮状态
        if hasattr(self, 'toggle_hud_button') and cmds.button(self.toggle_hud_button, exists=True):
            cmds.button(self.toggle_hud_button, edit=True, label=u"显示HUD", backgroundColor=(0.4, 0.6, 0.8))
            self.hud_visible = False
        print("All HUDs removed and button state updated")

    def update_hud_text(self, data, total_frames, camera, fps, resolution,  company, date, *args):
        f = cmds.currentTime(query=True)

        # 速度分析相关的数据，只有在有选择对象且有数据时才获取
        if self.selected_objects and data and f in data:
            # 有选择对象且有分析数据时，获取速度/踩地信息
            speed = data[f].get("speed", None)
            on_fround = data[f].get("on_ground", None)
            distance = data[f].get("distance", None)
        else:
            # 没有选择对象或没有分析数据时，速度分析显示默认值
            speed = None
            on_fround = None
            distance = None

        linear_unit = cmds.currentUnit(query=True, linear=True)
        if speed is not None:
            speed_info_text = u"速度: {0} {1}/s".format(speed, linear_unit)
        else:
            speed_info_text = u"速度: --"
        
        if cmds.headsUpDisplay('speed_info', exists=True):
            cmds.headsUpDisplay('speed_info', edit=True, label=speed_info_text)

        if distance is not None and self.ground_analysis:
            # 只有在启用踩地分析时才更新ground_info HUD
            ground_info_text = u"{}".format(u" 踩地" if distance <= 0 else u" 离地")
            if cmds.headsUpDisplay('ground_info', exists=True):
                cmds.headsUpDisplay('ground_info', edit=True, label=ground_info_text)

        # 帧数信息 - 现在由 get_frame_info 命令自动更新，无需手动设置


        self.get_current_camera_info()
        current_camera_name = self.camera_name
        camera_info_text = u"{}".format(current_camera_name)

        
        if cmds.headsUpDisplay('camera_name', exists=True):
            cmds.headsUpDisplay('camera_name', edit=True, label=camera_info_text)

        # 分辨率/FPS信息 - 实时获取准确的帧率
        try:
            # 获取真实的分辨率和帧率
            width = cmds.getAttr("defaultResolution.width") 
            height = cmds.getAttr("defaultResolution.height")
            real_fps = self.get_fps_from_time_unit()
            resolution_fps_info_text = u"{0}*{1}   FPS: {2}".format(int(width), int(height), real_fps)
        except:
            # 如果获取失败，使用传入的参数作为备选
            resolution_fps_info_text = u"{0}*{1}   FPS: {2}".format(resolution[0], resolution[1], fps)
        
        if cmds.headsUpDisplay('resolution_fps_info', exists=True):
            cmds.headsUpDisplay('resolution_fps_info', edit=True, label=resolution_fps_info_text)

        # 公司信息 - 使用实时的公司名
        company_info_text = u"{}".format(self.company)
        if cmds.headsUpDisplay('company_info', exists=True):
            cmds.headsUpDisplay('company_info', edit=True, label=company_info_text)


        # 日期信息
        date_info_text = u"Date: {}".format(date)
        if cmds.headsUpDisplay("date_info", exists=True):
            cmds.headsUpDisplay("date_info", edit=True, label=date_info_text)

        # 文件名信息
        current_file_name = self.get_maya_file_name()
        self.maya_file_name = current_file_name
        file_name_text = u"File: {}".format(current_file_name)
        if cmds.headsUpDisplay("file_name_info", exists=True):
            cmds.headsUpDisplay("file_name_info", edit=True, label=file_name_text)

    def register_callback(self, data, total_frames, camera, fps, resolution,  company, date):
        global time_changed_callback_id
        self.callback_data = data
        self.callback_total_frames = total_frames
        self.callback_camera = camera
        self.callback_fps = fps
        self.callback_resolution = resolution

        self.callback_company = company
        self.callback_date = date

        for hud_block in self.hud_list:
            if cmds.headsUpDisplay(hud_block, exists=True):
                cmds.headsUpDisplay(hud_block, remove=True)

        # 创建 HUD（只创建一次，之后内容用 update 编辑）
        all_huds = cmds.headsUpDisplay(listHeadsUpDisplays=True)

        # 删除所有 HUD（如果存在）
        try:
            all_huds = cmds.headsUpDisplay(listHeadsUpDisplays=True) or []
            if all_huds:
                print("Found {} existing HUDs, removing all: {}".format(len(all_huds), all_huds))
                for hud in all_huds:
                    try:
                        if cmds.headsUpDisplay(hud, exists=True):
                            cmds.headsUpDisplay(hud, remove=True)
                    except:
                        print("Failed to remove existing HUD: {}".format(hud))
            else:
                print("No existing HUDs found")
        except Exception as e:
            print("Failed to list/remove existing HUDs: {}".format(str(e)))

        # 使用统一的create_huds方法创建HUD
        self.create_huds()

        # 注册事件回调（注意：使用 maya.api.OpenMaya）
        time_changed_callback_id = om_api.MEventMessage.addEventCallback(
            "timeChanged",
            self.on_time_changed  # 使用实例方法而不是 lambda
        )
        self.time_changed_callback_id = time_changed_callback_id
        print("HUD registration completed, listening for frame changes")

    def on_time_changed(self, *args):
        """时间变化时的回调函数"""
        # 始终执行HUD更新，在update_hud_text内部处理选择对象的逻辑
        self.update_hud_text(
            data=self.callback_data,
            total_frames=self.callback_total_frames,
            camera=self.callback_camera,
            fps=self.callback_fps,
            resolution=self.callback_resolution,
            company=self.callback_company,
            date=self.callback_date
        )


    def unregister_callback(self, from_window_close=False):
        """取消注册回调
        Args:
            from_window_close: 是否来自窗口关闭回调，如果是则不操作UI元素
        """
        global time_changed_callback_id
        try:
            if hasattr(self, 'time_changed_callback_id') and self.time_changed_callback_id:
                om_api.MMessage.removeCallback(self.time_changed_callback_id)
                self.time_changed_callback_id = None
                print("Callback removed")
        except:
            pass
        
        # 只有在不是来自窗口关闭时才操作UI元素
        if not from_window_close:
            # 使用clear_hud方法清除HUD并更新按钮状态
            self.clear_hud()
            # 更新按钮状态
            if hasattr(self, 'toggle_hud_button') and cmds.button(self.toggle_hud_button, exists=True):
                cmds.button(self.toggle_hud_button, edit=True, label=u"显示HUD", backgroundColor=(0.4, 0.6, 0.8))
                self.hud_visible = False
        else:
            # 如果是窗口关闭，清理所有HUD，不操作UI按钮
            try:
                # 获取所有存在的HUD
                all_huds = cmds.headsUpDisplay(listHeadsUpDisplays=True) or []
                
                if all_huds:
                    print("Window closing: clearing {} HUDs".format(len(all_huds)))
                    for hud in all_huds:
                        try:
                            if cmds.headsUpDisplay(hud, exists=True):
                                cmds.headsUpDisplay(hud, remove=True)
                        except:
                            pass
                    print(u"窗口关闭时已清除所有HUD")
                else:
                    print(u"窗口关闭时未找到HUD")
            except:
                # 如果全部清理失败，仍然尝试清理插件定义的HUD
                for hud_name in self.hud_list:
                    try:
                        if cmds.headsUpDisplay(hud_name, exists=True):
                            cmds.headsUpDisplay(hud_name, remove=True)
                    except:
                        pass

    def playblast_with_analysis(self):
        """执行带分析的拍屏"""
        # 获取当前摄像机信息
        self.get_current_camera_info()
        camera = self.camera_name or "camera lose"
        focal_length = self.focal_length or 0
        fps = self.fps or 0
        resolution = self.resolution_info or [0, 0]

        # 生成文件名
        date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        maya_file_path = cmds.file(q=True, sceneName=True)
        if not maya_file_path:
            file_base_name = "untitled"
        else:
            file_base_name = os.path.splitext(os.path.basename(maya_file_path))[0]
        raw_video_path = os.path.join(self.output_dir, "{}.mov".format(file_base_name))

        # 获取帧范围
        start_frame = int(cmds.playbackOptions(q=True, min=True))
        end_frame = int(cmds.playbackOptions(q=True, max=True))
        total_frames = end_frame - start_frame + 1

        # 计算分析数据
        analysis_data = []

        # 计算速度数据（如果需要且有选中物体）
        speed_data = []
        if self.speed_analysis and self.selected_objects:
            speed_data = self.calculate_real_time_speed(
                fps=fps,
                resolution_w=resolution[0],
                resolution_h=resolution[1],
                camera=camera,
                start_frame=start_frame,
                end_frame=end_frame
            )

        # 计算离地数据（如果需要且有选中物体）
        ground_data = []
        if self.ground_analysis and self.selected_objects:
            ground_data = self.calculate_ground_data(
                resolution_w=resolution[0],
                resolution_h=resolution[1],
                camera=camera,
                start_frame=start_frame,
                end_frame=end_frame
            )

        # 合并数据
        frame_callback_data = {}
        for frame in range(start_frame, end_frame + 1):
            frame_data = {
                "frame": frame,
                "speed_info": {},
                "ground_info": {}
            }

            if frame not in frame_callback_data:
                frame_callback_data[frame] = {}

            # 添加速度数据
            for item in speed_data:
                if item["frame"] == frame:
                    for obj, data in item["objects"].items():
                        frame_data["speed_info"][obj] = data
                        frame_callback_data[frame]["speed"] = data.get("speed")

            # 添加离地数据
            for item in ground_data:
                if item["frame"] == frame:
                    for obj, data in item["objects"].items():
                        frame_data["ground_info"][obj] = data
                        frame_callback_data[frame]["on_ground"] = data.get("on_ground")
                        frame_callback_data[frame]["distance"] = data.get("distance")

            analysis_data.append(frame_data)



        # self.unregister_callback()
        self.register_callback(
            data=frame_callback_data,
            total_frames=total_frames,
            camera=camera,
            fps=fps,
            resolution=resolution,
            company=self.company,
            date=datetime.datetime.now().strftime("%Y/%m/%d")
        )
        # 执行拍屏
        sound_nodes = cmds.ls(type='audio')
        playblast_kwargs = {
            'format': 'qt',
            'compression': 'MPEG-4 Video',
            'filename': raw_video_path,
            'startTime': start_frame,
            'endTime': end_frame,
            'sequenceTime': False,
            'clearCache': True,
            'viewer': False,
            'showOrnaments': True,
            'fp': 4,
            'percent': 100,
            'quality': 100,
            'widthHeight': resolution,
            'forceOverwrite': True
        }

        if sound_nodes:
            playblast_kwargs['sound'] = sound_nodes[0]
            print("Found audio node '{}' and added to playblast".format(sound_nodes[0]))
        else:
            print("No audio nodes found in scene, playblast will not include sound")

        # 设置当前摄像机的overscan为1.3
        try:
            current_camera = self.current_camera or camera
            if current_camera and cmds.objExists(current_camera):
                # 保存原始overscan值
                original_overscan = None
                if cmds.attributeQuery('overscan', node=current_camera, exists=True):
                    original_overscan = cmds.getAttr(current_camera + '.overscan')
                
                # 设置overscan为1.3
                cmds.setAttr(current_camera + '.overscan', 1.3)
                print(u"已设置摄像机 {} 的overscan为1.3".format(current_camera))
                
                # 执行拍屏
                cmds.playblast(**playblast_kwargs)
                
                # 恢复原始overscan值（如果有的话）
                if original_overscan is not None:
                    cmds.setAttr(current_camera + '.overscan', original_overscan)
                    print(u"已恢复摄像机 {} 的overscan为{}".format(current_camera, original_overscan))
            else:
                print(u"警告：未找到有效的摄像机，使用默认设置执行拍屏")
                cmds.playblast(**playblast_kwargs)
        except Exception as e:
            print(u"设置摄像机overscan时出错: {}，使用默认设置继续".format(str(e)))
            cmds.playblast(**playblast_kwargs)

        # 拍屏完成弹窗，包含播放按钮
        result = cmds.confirmDialog(
            title=u"完成",
            message=u"拍屏分析已完成！\n视频保存至:\n{}".format(raw_video_path),
            button=[u"播放视频", u"确定"],
            defaultButton=u"确定",
            cancelButton=u"确定",
            dismissString=u"确定"
        )
        
        # 如果用户点击了播放视频按钮
        if result == u"播放视频":
            self.play_with_quicktime(raw_video_path)

    # 工具函数
    def get_current_camera_info(self):
        """
        获取当前活动视图的摄像机信息：名称、焦距、FPS、分辨率等
        将信息存储为实例属性
        """
        # 初始化属性
        self.camera_name = None
        self.focal_length = None
        self.fps = None
        self.resolution_info = None
        self.near_clip = None
        self.far_clip = None

        try:
            # 获取当前活动 3D 视图
            view = omui_api.M3dView.active3dView()
            camera_path = view.getCamera()
            camera_fn = om_api.MFnCamera(camera_path)

            # 摄像机名称
            self.camera_name = camera_fn.fullPathName().split('|')[1]

            # 焦距
            self.focal_length = int(round(camera_fn.focalLength))

            # 裁剪面
            self.near_clip = camera_fn.nearClippingPlane
            self.far_clip = camera_fn.farClippingPlane

            # FPS
            self.fps = self.get_fps_from_time_unit()

            # 分辨率
            width = cmds.getAttr("defaultResolution.width")
            height = cmds.getAttr("defaultResolution.height")
            self.resolution_info = (width, height)

        except Exception as e:
            om_api.MGlobal.displayWarning(u"获取摄像机信息失败: {0}".format(e))


    def get_active_camera(self):
        """获取当前激活的3D视图摄像机"""
        view = omui_api.M3dView.active3dView()
        camera_path = view.getCamera()
        return camera_path.fullPathName()

    def is_skinned_mesh(self, obj):
        """
        判断一个 transform 是否为被 skinCluster 控制的蒙皮模型
        """
        shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
        for shape in shapes:
            history = cmds.listHistory(shape) or []
            for h in history:
                if cmds.nodeType(h) == 'skinCluster':
                    return True
        return False

    def get_vertex_world_position(self, obj_name, vertex_index=0):
        """
        获取一个蒙皮模型某个顶点的世界坐标（默认第一个顶点）
        """
        selection = om_api.MSelectionList()
        selection.add(obj_name)
        dag_path = selection.getDagPath(0)

        mesh_fn = om_api.MFnMesh(dag_path)
        point = mesh_fn.getPoint(vertex_index, om_api.MSpace.kWorld)
        return [point.x, point.y, point.z]

    def get_object_world_position(self, obj):
        """
        根据对象类型自动判断如何取世界坐标
        """
        if self.is_skinned_mesh(obj):
            try:
                return om_api.MVector(*self.get_vertex_world_position(obj, vertex_index=0))
            except:
                return None
        else:
            try:
                pos = cmds.xform(obj, q=True, ws=True, t=True)
                return om_api.MVector(*pos) if pos else None
            except:
                return None

    def calculate_real_time_speed(self, fps, resolution_w, resolution_h, camera=None,
                                  start_frame=None, end_frame=None):
        """
        计算实时速度，支持普通物体与蒙皮模型，使用中心差分法计算的速度
        """
        if start_frame is None:
            start_frame = int(cmds.playbackOptions(query=True, minTime=True))
        if end_frame is None:
            end_frame = int(cmds.playbackOptions(query=True, maxTime=True))

        if start_frame >= end_frame:
            raise ValueError(u"起始帧和结束帧无效")

        frame_interval = 1.0 / float(fps)
        current_time = cmds.currentTime(q=True)
        result_list = []

        # 缓存所有帧的位置数据（包含首尾 + 1 帧用于中心差分）
        frame_positions = {frame: {} for frame in range(start_frame, end_frame + 1)}
        for frame in frame_positions:
            cmds.currentTime(frame, edit=True)
            for obj in self.selected_objects:
                pos = self.get_object_world_position(obj)
                if pos:
                    frame_positions[frame][obj] = pos

        try:
            for frame in range(start_frame, end_frame + 1):
                frame_data = {"frame": frame, "objects": {}}
                for obj in self.selected_objects:
                    try:
                        pos_curr = frame_positions.get(frame, {}).get(obj)

                        if frame == start_frame or frame == end_frame:
                            # 首尾帧速度强制为 0
                            if pos_curr:
                                frame_data["objects"][obj] = {
                                    "speed": 0,
                                    "velocity": [0.0, 0.0, 0.0],
                                    "position": [round(pos_curr.x, 2), round(pos_curr.y, 2), round(pos_curr.z, 2)],
                                }
                            continue

                        pos_prev = frame_positions.get(frame - 1, {}).get(obj)
                        pos_next = frame_positions.get(frame + 1, {}).get(obj)

                        if not (pos_prev and pos_next and pos_curr):
                            continue

                        # 中心差分计算速度
                        delta = pos_next - pos_prev
                        speed_vector = delta * (0.5 * fps)
                        speed = speed_vector.length()

                        frame_data["objects"][obj] = {
                            "speed": int(round(speed)),
                            "velocity": [round(v, 2) for v in [speed_vector.x, speed_vector.y, speed_vector.z]],
                            "position": [round(pos_curr.x, 2), round(pos_curr.y, 2), round(pos_curr.z, 2)],
                        }

                    except Exception as e:
                        print(u"计算速度失败: {0}".format(str(e)))

                result_list.append(frame_data)

        finally:
            cmds.currentTime(current_time, edit=True)
        return result_list

    def calculate_ground_data(self, resolution_w, resolution_h, camera=None,
                              start_frame=None, end_frame=None):
        """
        计算离地数据
        """
        if start_frame is None:
            start_frame = int(cmds.playbackOptions(query=True, minTime=True))
        if end_frame is None:
            end_frame = int(cmds.playbackOptions(query=True, maxTime=True))

        result_list = []
        current_time = cmds.currentTime(q=True)

        try:
            for frame in range(start_frame, end_frame + 1):
                cmds.currentTime(frame)
                frame_data = {"frame": frame, "objects": {}}
                for obj in self.selected_objects:
                    try:
                        # 分析踩地状态
                        bottom_face_index, distance_to_ground, result = self.is_on_ground(
                            obj,
                            self.ground_mesh,
                            self.ground_threshold
                        )
                        # 获取屏幕坐标
                        pos = cmds.xform(obj, q=True, ws=True, t=True)
                        frame_data["objects"][obj] = {
                            "on_ground": result,
                            "distance": round(distance_to_ground, 4),
                            "pos": pos,
                        }
                    except Exception as e:
                        print(u"计算离地状态出错: {0}".format(str(e)))

                result_list.append(frame_data)
        finally:
            cmds.currentTime(current_time)

        return result_list


    def get_view_from_camera(self, camera):
        """
        根据摄像机名称获取对应的 M3dView 视图。
        若未找到则返回当前活动视图。
        """
        panels = cmds.getPanel(type="modelPanel")
        for panel in panels:
            cam = cmds.modelEditor(panel, query=True, camera=True)
            if cam == camera:
                return omui_api.M3dView.getM3dViewFromModelEditor(panel)
        return omui_api.M3dView.active3dView()


    def is_on_ground(self, transform, ground_mesh, threshold=0.2):
        """
        通用判断物体是否踩地，自动容错，适配不同类型地面。
        返回: (底面索引, 离地距离, 是否踩地)
        """
        try:
            # 获取物体的 shape 和 MFnMesh
            all_descendants = cmds.listRelatives(transform, allDescendents=True, fullPath=True) or []
            shapes = [node for node in all_descendants if cmds.nodeType(node) in ("mesh", "nurbsCurve", "nurbsSurface")]
            shape = shapes[0]
            sel_list = om_api.MSelectionList()
            sel_list.add(shape)
            dag_path = sel_list.getDagPath(0)
            mesh_fn = om_api.MFnMesh(dag_path)

            # 找物体最低的面
            lowest_y = float('inf')
            bottom_face_index = None
            for i in range(mesh_fn.numPolygons):
                verts = mesh_fn.getPolygonVertices(i)
                points = [mesh_fn.getPoint(v, om_api.MSpace.kWorld) for v in verts]
                avg_y = sum(p.y for p in points) / float(len(points))
                if avg_y < lowest_y:
                    lowest_y = avg_y
                    bottom_face_index = i

            center = self.get_polygon_center(mesh_fn, bottom_face_index)
            normal = mesh_fn.getPolygonNormal(bottom_face_index, om_api.MSpace.kWorld).normalize()
            ray_dir = om_api.MVector(normal)  # 显式转换为 MVector
            offset = om_api.MVector(ray_dir.x * 0.01, ray_dir.y * 0.01, ray_dir.z * 0.01)
            ray_origin = center + offset
            if normal.y > 0:
                ray_dir = -normal  # 向下
            else:
                ray_dir = normal

            # 获取 ground_mesh 的 shape 和 MFnMesh
            ground_descendants = cmds.listRelatives(ground_mesh, allDescendents=True, fullPath=True) or []
            ground_shapes = [node for node in ground_descendants if cmds.nodeType(node) in ("mesh", "nurbsCurve", "nurbsSurface")]
            sel = om_api.MSelectionList()
            for ground_shape in ground_shapes:
                sel.add(ground_shape)
            dag = sel.getDagPath(0)
            ground_fn = om_api.MFnMesh(dag)

            # 首选: 使用closestIntersection获取物体面上的点到法线和地面交点的距离
            try:
                accel = ground_fn.autoUniformGridParams()
                result = ground_fn.closestIntersection(
                    om_api.MFloatPoint(ray_origin),
                    om_api.MFloatVector(ray_dir),
                    om_api.MSpace.kWorld,
                    99999.0,
                    False,
                    [],
                    [],
                    False,
                    accel,
                    1e-6
                )
                if result:
                    hit_point = result[0]
                    distance = (hit_point - ray_origin).length()
                    return bottom_face_index, distance, distance < threshold
            except:
                pass

            # 次选: 使用 getClosestPoint
            closest_point, _ = ground_fn.getClosestPoint(center, om_api.MSpace.kWorld)
            if closest_point.y > ray_origin.y:
                distance = (closest_point - center).length() * -1
            else:
                distance = (closest_point - center).length()

            return bottom_face_index, distance, distance < threshold

        except Exception as e:
            print(u"计算失败: {0}".format(e))
            return None, float('inf'), False


    def get_polygon_center(self, mesh_fn, face_index):
        """手动计算多边形面中心点"""
        vertex_ids = mesh_fn.getPolygonVertices(face_index)
        points = [mesh_fn.getPoint(vtx_id, om_api.MSpace.kWorld) for vtx_id in vertex_ids]

        avg_x = sum([p.x for p in points]) / float(len(points))
        avg_y = sum([p.y for p in points]) / float(len(points))
        avg_z = sum([p.z for p in points]) / float(len(points))

        return om_api.MPoint(avg_x, avg_y, avg_z)


# 创建面板
def show_analysis_panel():
    panel = AnalysisPanel()


# 运行面板
if __name__ == '__main__':
    show_analysis_panel()
    
def main():
    show_analysis_panel()
    
'''
import os,sys
sys.path.append(r'G:\TYYF\研发\pipeline工具开发\第二阶段\杨俊炜\面板整合\camera_dev')
import ani_play_balst
reload(ani_play_balst)
ani_play_balst.show_analysis_panel()
'''
