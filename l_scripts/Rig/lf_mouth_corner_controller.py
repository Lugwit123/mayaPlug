# -*- coding: utf-8 -*-
# Maya 2020 Python2 兼容版本 - 优化编码处理
"""
嘴角控制器参数调节面板
实现完整嘴角表达式组的参数化控制
包含左右嘴角的X、Y、Z轴控制
"""

# 导入Maya模块
try:
    import maya.cmds as cmds
    MAYA_MODE = True
    print(u"Maya环境检测成功")
except ImportError:
    MAYA_MODE = False
    print(u"错误：此脚本需要在Maya中运行")
    raise ImportError(u"请在Maya Script Editor中运行此脚本")

import math
from re import U
import traceback
import maya.mel as mel
import os
import json
from datetime import datetime
import Lugwit_Module as LM  # 导入 Lugwit_Module
import codecs
import sys
from Lugwit_Module import lprint# reload(sys)
# sys.setdefaultencoding('utf-8')

def safe_unicode_error(e):
    """安全地将异常转换为unicode字符串"""
    try:
        if isinstance(e, unicode):
            return e
        elif isinstance(e, str):
            return unicode(e, 'utf-8')
        else:
            return unicode(str(e), 'utf-8')
    except:
        return u"未知错误"


class MouthCornerController:
    def __init__(self):
        # 顶点名称列表
        self.vertices_name = [
            "Lf_browInner_Loc",
            "Rt_browlnner_Loc", 
            "Lf_browOuter_Loc", 
            "Rt_browOuter_Loc", 
            "Lf_eyeLid_Loc", 
            "Rt_eyeLid_Loc", 
            "Lf_eyeBall_Loc", 
            "Lf_eyeAim_Loc", 
            "Rt_eyeBall_Loc", 
            "Rt_eyeAim_Loc", 
            "Up_mouthLip_Loc", 
            "Dn_mouthLip_Loc", 
            "Lf_mouthCorner_Loc",  
            "Rt_mouthCorner_Loc", 
            "Mi_Jaw_Loc"
        ]
        
        # 控制器名称列表
        self.g_control_name = [
            "eyelid_ctl",
            "eyelid_ctl2",
            "brow2_ctl", 
            "brow2_ctl2",
            "mouth_ctl",
            "mouth_ctl2",
            "loc_eye_L2",
            "loc_eye_R2",
            "brow1_ctl",
            "brow1_ctl2",
            "lip_ctl",
            "jaw_ctl"
        ]

        # 控制器属性列表 - 根据默认表达式更新
        self.g_controls = [
            "Lf_browInner_Ctrl.translateX",
            "Lf_browInner_Ctrl.translateY",
            "Rt_browInner_Ctrl.translateX",
            "Rt_browInner_Ctrl.translateY",
            "Lf_browOuter_Ctrl.translateY",
            "Rt_browOuter_Ctrl.translateY",
            "Lf_eyeLid_Ctrl.translateY",
            "Rt_eyeLid_Ctrl.translateY",
            "Lf_eyeAim_Ctrl.translateX",
            "Lf_eyeAim_Ctrl.translateY",
            "Lf_eyeAim_Ctrl.translateZ",
            "Rt_eyeAim_Ctrl.translateX",
            "Rt_eyeAim_Ctrl.translateY",
            "Rt_eyeAim_Ctrl.translateZ",
            "Mi_Jaw_Ctrl.translateX",
            "Mi_Jaw_Ctrl.translateY",
            "Mi_Jaw_Ctrl.translateZ",
            "Lf_mouthCorner_Ctrl.translateX",
            "Lf_mouthCorner_Ctrl.translateY",
            "Lf_mouthCorner_Ctrl.translateZ",
            "Rt_mouthCorner_Ctrl.translateX",
            "Rt_mouthCorner_Ctrl.translateY",
            "Rt_mouthCorner_Ctrl.translateZ",
            "Up_mouthLip_Ctrl.translateX",
            "Up_mouthLip_Ctrl.translateY",
            "Up_mouthLip_Ctrl.translateZ",
            "Dn_mouthLip_Ctrl.translateX",
            "Dn_mouthLip_Ctrl.translateY",
            "Dn_mouthLip_Ctrl.translateZ"
        ]
        
        # 参数字典 - 增加上下嘴唇独立控制系数
        self.parameters = {
            "mouth_corner_coeff": {
                "name": u"嘴角控制系数",
                "value": 1.0,
                "min": 0.0,
                "max": 2.0
            },
            "up_lip_coeff": {
                "name": u"上嘴唇控制系数",
                "value": 1.0,
                "min": 0.0,
                "max": 2.0
            },
            "dn_lip_coeff": {
                "name": u"下嘴唇控制系数",
                "value": 1.0,
                "min": 0.0,
                "max": 2.0
            },
            "jaw_coeff": {
                "name": u"下颌控制系数",
                "value": 1.0,
                "min": 0.0,
                "max": 2.0
            },
            "brow_inner_coeff": {
                "name": u"眉毛内侧控制系数",
                "value": 1.0,
                "min": 0.0,
                "max": 2.0
            },
            "brow_outer_coeff": {
                "name": u"眉毛外侧控制系数",
                "value": 1.0,
                "min": 0.0,
                "max": 2.0
            }
        }
        
        self.window_name = "MouthCornerController"
        self.sliders = {}
        self.model_name_field = None
        # 帧范围输入字段
        self.start_frame_field = None
        self.end_frame_field = None
        # 表达式变量 Mapping_Expr
        self.aa = u""
        self.create_ui()
    
    def create_ui(self):
        """创建用户界面"""
        try:
            # 删除已存在的窗口
            if cmds.window(self.window_name, exists=True):
                cmds.deleteUI(self.window_name, window=True)
            
            # 创建主窗口
            self.window = cmds.window(self.window_name, 
                                     title=u"面部控制器参数调节面板",
                                     widthHeight=(700, 500),
                                     resizeToFitChildren=True)
            
            # 主布局
            main_layout = cmds.columnLayout(adjustableColumn=True, 
                                           columnOffset=('both', 10),
                                           rowSpacing=10)
            
            # 标题
            cmds.text(label=u"面部控制器表达式参数控制", 
                     font="boldLabelFont", 
                     height=30,
                     align="center")
            
            cmds.separator(height=10)
            
            # 创建列布局
            cmds.columnLayout(adjustableColumn=True)
            
            # 模型名称输入字段
            self.model_name_field = cmds.textFieldButtonGrp(
                                   label=u"选择源头模型名称",
                                   text="Newton_HeadFace",
                                   buttonLabel=u"确定",
                                   buttonCommand=self.new_name)
            
            # 功能按钮
            cmds.button(label=u"一键传递面补数据", command=self.auto_process_head)
            cmds.button(label=u"控制器参数归零", command=self.reset_controllers_to_zero, enableBackground=False, highlightColor=(0.1, 0.1, 0.1))
            # cmds.button(label=u"删除Mapping_Expr表达式", command=self.delete_mapping_expr, enableBackground=False)
            # cmds.button(label=u"创建默认表达式", command=self.create_default_expression_button)
            
            # 帧范围设置区域
            cmds.separator(height=10, style="in")
            cmds.text(label=u"自定义烘焙帧范围", font="boldLabelFont")
            
            # 创建行布局来并排显示起始帧和结束帧输入框
            frame_layout = cmds.rowColumnLayout(numberOfColumns=2, 
                                               columnWidth=[(1, 300), (2, 300)],
                                               columnSpacing=[(2, 5)])
            
            # 起始帧输入字段
            self.start_frame_field = cmds.intFieldGrp(
                label=u"起始帧",
                numberOfFields=1,
                value1=int(cmds.playbackOptions(query=True, minTime=True)),
                columnWidth2=[80, 70]
            )
            
            # 结束帧输入字段  
            self.end_frame_field = cmds.intFieldGrp(
                label=u"结束帧",
                numberOfFields=1,
                value1=int(cmds.playbackOptions(query=True, maxTime=True)),
                columnWidth2=[80, 70]
            )
            
            cmds.setParent('..')  # 返回上一级布局
            
            # 烘焙功能按钮
            cmds.button(label=u"烘焙表情动画到控制器", command=self.bake_animation_to_controllers)
            
            # 暗色警告文字（在按钮下方）
            cmds.text(label=u"(烘焙后无法使用预设表情)", 
                     font="smallPlainLabelFont",
                     enable=False,  # 使文字变暗
                     align="center",
                     height=18)
            
            # 表达式预设管理区域
            cmds.separator(height=10, style="in")
            cmds.text(label=u"表达式预设管理", font="boldLabelFont")
            
            # 预设选择下拉菜单（添加选择变化回调）
            self.preset_option_menu = cmds.optionMenu(label=u"选择预设", changeCommand=self.on_preset_selection_changed)
            self.update_preset_menu()
            cmds.setParent('..')  # 返回上一级布局
            
            # 预设管理按钮（只保留删除按钮）
            cmds.button(label=u"删除选中预设", command=self.delete_selected_preset)
            
            cmds.button(label=u"更新表达式并保存预设", command=self.update_expression_with_preset_save)
            
            cmds.separator(height=10, style="in")
            
            # 为每个参数创建滑条
            for param_key, param_info in self.parameters.items():
                # 参数分组
                param_frame = cmds.frameLayout(label=param_info["name"], 
                                              collapsable=False,
                                              marginWidth=5,
                                              marginHeight=5)
                
                param_layout = cmds.rowColumnLayout(numberOfColumns=2, 
                                                   columnWidth=[(1, 200), (2, 350)],
                                                   columnSpacing=[(2, 10)])
                
                # 数值显示
                value_text = u"当前值: " + str(round(param_info['value'], 3))
                value_label = cmds.text(label=value_text, align="left")
                
                # 滑条
                slider = cmds.floatSlider(min=param_info["min"], 
                                         max=param_info["max"],
                                         value=param_info["value"],
                                         step=0.001,
                                         dragCommand=lambda val, key=param_key: self.on_slider_change(key, val),
                                         changeCommand=lambda val, key=param_key: self.on_slider_change(key, val))
                
                self.sliders[param_key] = {
                    "slider": slider,
                    "value_label": value_label
                }
                
                cmds.setParent('..')  # 返回上一级布局
                cmds.setParent('..')  # 返回上一级布局
            
            # # 添加执行按钮
            # cmds.separator(height=10)
            # cmds.button(label=u"更新表达式并保存预设", 
            #            command=lambda x: self.execute_aa_expression(),
            #            backgroundColor=(0.5, 0.8, 0.5),
            #            height=30)
            
            # 显示窗口
            cmds.showWindow(self.window)
            
        except BaseException as e:
            print(u"创建用户界面失败")
            traceback.print_exc()
            
    def new_name(self, *args):
        """设置模型名称"""
        try:
            sel = cmds.ls(selection=True)
            if sel:
                cmds.textFieldButtonGrp(self.model_name_field, edit=True, text=sel[0])
                model_name = cmds.textFieldButtonGrp(self.model_name_field, query=True, text=True)
                print(u"设置模型名称为: " + str(model_name))
                
                # 将默认lambert材质赋予给该模型
                try:
                    # 获取默认lambert材质
                    default_lambert = "lambert1"
                    # 选择模型
                    cmds.select(model_name)
                    # 将默认lambert材质赋予给模型
                    cmds.hyperShade(assign=default_lambert)
                    print(u"已将默认lambert材质赋予给模型: " + str(model_name))
                except Exception as mat_error:
                    print(u"赋予材质时发生错误: " + str(mat_error))
                
                return model_name
            else:
                print(u"请先选择一个模型")
                return ""
        except Exception as e:
            print(u"设置模型名称时发生错误: " + str(e))
            return ""
            
    def auto_process_head(self, *args):
        """一键执行头部模型处理流程"""
        try:
            print(u"=== 开始执行头部模型自动处理流程 ===")
            
            # 步骤2：自动p出头部模型
            print(u"步骤2：正在处理头部模型...")
            self.p_head()
            print(u"步骤2：头部模型处理完成")
            
            # 步骤3：自动创建uv
            print(u"步骤3：正在创建UV映射...")
            self.create_uv()
            print(u"步骤3：UV映射创建完成")
            
            # 步骤4：删除继承源头模型的蒙皮信息
            print(u"步骤4：正在删除蒙皮信息...")
            self.delete_skin()
            print(u"步骤4：蒙皮信息删除完成")
            
            # 步骤5：删除继承源头模型非必要的历史
            print(u"步骤5：正在删除非必要历史...")
            self.delete_his()
            print(u"步骤5：历史删除完成")
            
            # 步骤6：重命名混合形状节点组
            print(u"步骤6：正在重命名混合形状节点组...")
            if self.rename_blendshape_node():
                print(u"步骤6：混合形状节点组重命名完成")
            else:
                print(u"步骤6：混合形状节点组重命名失败")
            
            # 步骤7：自动创建locator约束到模型上的点
            print(u"步骤7：正在创建定位器约束...")
            if self.create_locator():
                print(u"步骤7：定位器约束创建完成")
                
                # 步骤8：自动创建默认表达式
                print(u"步骤8：正在创建默认表达式...")
                if self.create_default_expression():
                    print(u"步骤8：默认表达式创建完成")
                else:
                    print(u"步骤8：默认表达式创建失败，请手动创建")
            else:
                print(u"步骤7：定位器约束创建失败，跳过表达式创建")
            
            print(u"=== 头部模型自动处理流程全部完成！ ===")
            
        except Exception as e:
            print(u"自动处理头部模型时发生错误: " + str(e))
            
    def reset_controllers_to_zero(self, *args):
        """将场景中self.g_controls组的控制器参数归零"""
        try:
            print(u"=== 开始重置控制器参数 ===")
            
            reset_count = 0
            failed_count = 0
            missing_controllers = []
            
            for ctrl_attr in self.g_controls:
                try:
                    # 检查控制器属性是否存在
                    if cmds.objExists(ctrl_attr):
                        # 设置属性值为0
                        cmds.setAttr(ctrl_attr, 0)
                        reset_count += 1
                        print(u"已重置: %s = 0" % ctrl_attr)
                    else:
                        missing_controllers.append(ctrl_attr)
                        print(u"控制器属性不存在: %s" % ctrl_attr)
                        
                except Exception as attr_error:
                    failed_count += 1
                    print(u"重置属性 %s 失败: %s" % (ctrl_attr, safe_unicode_error(attr_error)))
                    continue
            
            # 显示重置结果统计
            print(u"=== 控制器参数重置完成 ===")
            print(u"成功重置: %d 个属性" % reset_count)
            if failed_count > 0:
                print(u"重置失败: %d 个属性" % failed_count)
            if missing_controllers:
                print(u"缺少控制器: %d 个" % len(missing_controllers))
            
            # 不显示弹窗，只在控制台输出结果
                
        except Exception as e:
            error_msg = u"重置控制器参数时发生错误: " + safe_unicode_error(e)
            print(error_msg)
            
    def delete_mapping_expr(self, *args):
        """一键删除Mapping_Expr表达式"""
        try:
            print(u"=== 开始删除Mapping_Expr表达式 ===")
            
            # 检查Mapping_Expr表达式是否存在
            if cmds.objExists("Mapping_Expr"):
                try:
                    # 直接删除表达式
                    cmds.delete("Mapping_Expr")
                    print(u"Mapping_Expr表达式已成功删除")
                    
                except Exception as delete_error:
                    error_msg = u"删除Mapping_Expr表达式失败: " + safe_unicode_error(delete_error)
                    print(error_msg)
                    
            else:
                print(u"Mapping_Expr表达式不存在")
                
        except Exception as e:
            error_msg = u"删除Mapping_Expr表达式时发生错误: " + safe_unicode_error(e)
            print(error_msg)
            
    def create_default_expression_button(self, *args):
        """创建默认表达式按钮的回调函数"""
        try:
            print(u"=== 开始创建默认表达式 ===")
            
            if self.create_default_expression():
                print(u"默认表达式创建完成")
                
                # 显示成功信息
                cmds.confirmDialog(
                    title=u"创建成功",
                    message=u"默认表达式已成功创建",
                    button=[u"确定"],
                    defaultButton=u"确定",
                    icon=u"information"
                )
            else:
                print(u"默认表达式创建失败")
                
        except Exception as e:
            error_msg = u"创建默认表达式时发生错误: " + safe_unicode_error(e)
            print(error_msg)
            cmds.confirmDialog(
                title=u"创建失败",
                message=error_msg,
                button=[u"确定"],
                defaultButton=u"确定",
                icon=u"critical"
            )
    
    def bake_animation_to_controllers(self, *args):
        """烘焙当前动画帧数据到所有控制器"""
        try:
            print(u"=== 开始烘焙动画到控制器 ===")
            
            # 获取时间轴信息
            start_time = cmds.playbackOptions(query=True, minTime=True)
            end_time = cmds.playbackOptions(query=True, maxTime=True)
            current_time = cmds.currentTime(query=True)
            
            print(u"时间轴范围: %.0f - %.0f 帧" % (start_time, end_time))
            print(u"当前时间: %.0f 帧" % current_time)
            
            # 检查控制器是否存在
            existing_controllers = []
            missing_controllers = []
            
            # 从 g_controls 中提取控制器名称（去掉属性部分）
            controller_names = set()
            for ctrl_attr in self.g_controls:
                ctrl_name = ctrl_attr.split('.')[0]
                controller_names.add(ctrl_name)
            
            # 检查控制器存在性
            for ctrl_name in controller_names:
                if cmds.objExists(ctrl_name):
                    existing_controllers.append(ctrl_name)
                else:
                    missing_controllers.append(ctrl_name)
            
            print(u"找到控制器: %d 个" % len(existing_controllers))
            print(u"缺失控制器: %d 个" % len(missing_controllers))
            
            if missing_controllers:
                print(u"缺失的控制器:")
                for ctrl in missing_controllers:
                    print(u"  - %s" % ctrl)
            
            if not existing_controllers:
                print(u"错误: 没有找到任何控制器，无法执行烘焙")
                return
            
            # 获取自定义帧范围
            custom_start_frame = None
            custom_end_frame = None
            
            try:
                if self.start_frame_field:
                    custom_start_frame = cmds.intFieldGrp(self.start_frame_field, query=True, value1=True)
                if self.end_frame_field:
                    custom_end_frame = cmds.intFieldGrp(self.end_frame_field, query=True, value1=True)
            except:
                print(u"获取自定义帧范围失败，使用时间轴范围")
                custom_start_frame = None
                custom_end_frame = None
            
            # 设置烘焙范围 - 直接使用自定义范围，无需确认弹窗
            if custom_start_frame is not None and custom_end_frame is not None:
                # 验证自定义帧范围
                if custom_start_frame <= custom_end_frame:
                    bake_start = custom_start_frame
                    bake_end = custom_end_frame
                    print(u"使用自定义帧范围: %d - %d" % (custom_start_frame, custom_end_frame))
                else:
                    print(u"警告: 起始帧(%d)大于结束帧(%d)，使用时间轴范围" % (custom_start_frame, custom_end_frame))
                    bake_start = start_time
                    bake_end = end_time
                    print(u"使用时间轴范围: %.0f - %.0f" % (start_time, end_time))
            else:
                # 如果没有自定义范围，使用时间轴范围
                bake_start = start_time
                bake_end = end_time
                print(u"自定义帧范围无效，使用时间轴范围: %.0f - %.0f" % (start_time, end_time))
            
            # 执行烘焙
            print(u"开始烘焙动画...")
            
            # 选择所有存在的控制器
            cmds.select(existing_controllers, replace=True)
            
            # 使用Maya的bakeResults命令烘焙动画
            cmds.bakeResults(
                existing_controllers,
                time=(bake_start, bake_end),
                sampleBy=1,  # 每帧采样
                oversamplingRate=1,
                disableImplicitControl=True,
                preserveOutsideKeys=True,
                sparseAnimCurveBake=False,
                removeBakedAttributeFromLayer=False,
                removeBakedAnimFromLayer=False,
                bakeOnOverrideLayer=False,
                minimizeRotation=True,
                controlPoints=False,
                shape=False
            )
            
            print(u"烘焙完成！")
            print(u"已烘焙 %d 个控制器，时间范围: %.0f - %.0f" % (len(existing_controllers), bake_start, bake_end))
            
            # 显示成功信息（简化版本）
            cmds.confirmDialog(
                title=u"烘焙完成",
                message=u"动画烘焙成功！\n\n已烘焙 %d 个控制器\n时间范围: %.0f - %.0f 帧" % (
                    len(existing_controllers), bake_start, bake_end),
                button=[u"确定"],
                defaultButton=u"确定"
            )
            
        except Exception as e:
            print(u"烘焙动画时发生错误: " + safe_unicode_error(e))
            import traceback
            traceback.print_exc()
            
            # 显示错误信息
            cmds.confirmDialog(
                title=u"烘焙失败",
                message=u"烘焙动画时发生错误:\n%s" % safe_unicode_error(e),
                button=[u"确定"],
                defaultButton=u"确定",
                icon=u"warning"
            )
            
    def p_head(self):
        """自动p出头部模型"""
        try:
            model_name = cmds.textFieldButtonGrp(self.model_name_field, query=True, text=True)
            if not model_name:
                print(u"错误: 请先设置模型名称")
                return
                
            if cmds.objExists(model_name):
                cmds.select(model_name)
                cmds.parent(world=True)
                print(u"模型 " + str(model_name) + u" 已分离到世界空间")
            else:
                print(u"错误: 模型 " + str(model_name) + u" 不存在")
                
        except Exception as e:
            print(u"分离头部模型时发生错误: " + str(e))
            
    def create_uv(self):
        """创建模型uv"""
        try:
            model_name = cmds.textFieldButtonGrp(self.model_name_field, query=True, text=True)
            if not model_name:
                print(u"错误: 请先设置模型名称")
                return
                
            if not cmds.objExists(model_name):
                print(u"错误: 模型 " + str(model_name) + u" 不存在")
                return
                
            # 选择模型
            cmds.select(model_name, replace=True)
            
            # 获取模型的面数
            face_count = cmds.polyEvaluate(model_name, face=True)
            print(u"模型 " + str(model_name) + u" 有 " + str(face_count) + u" 个面")
            
            # 选择所有面
            cmds.select("%s.f[*]" % model_name, replace=True)
            
            # 删除现有UV集（如果有）
            uv_sets = cmds.polyUVSet(model_name, query=True, allUVSets=True)
            if uv_sets and len(uv_sets) > 1:  # 保留默认的map1
                for uv_set in uv_sets:
                    if uv_set != "map1":
                        try:
                            cmds.polyUVSet(delete=True, uvSet=uv_set)
                            print(u"删除UV集: " + str(uv_set))
                        except:
                            pass
            
            # 使用简化的自动投影创建UV
            try:
                # 先尝试使用Python API
                cmds.polyAutoProjection(
                    "%s.f[*]" % model_name,
                    layoutMethod=0,
                    projectBothDirections=0,
                    insertBeforeDeformers=1,
                    createNewMap=0,  # 不创建新UV集，使用现有的
                    layout=2,
                    scale=1,
                    optimize=1,
                    planes=6,
                    percentageSpace=0.2,
                    worldSpace=0
                )
                print(u"使用Python API完成UV映射")
            except Exception as uv_error:
                print(u"Python API创建UV失败，尝试MEL命令: " + str(uv_error))
                # 使用更简单的MEL命令
                mel.eval('select -r "%s";' % model_name)
                mel.eval('polyAutoProjection -lm 0 -pb 0 -ibd 1 -cm 0 -l 2 -sc 1 -o 1 -p 6 -ps 0.2 -ws 0;')
                print(u"使用MEL命令完成UV映射")
            
            # 尝试切换到UV编辑器（可选，如果失败不影响主要功能）
            try:
                mel.eval('TextureViewWindow;')
            except:
                print(u"提示: UV编辑器切换失败，但UV创建成功")
            
            print(u"UV映射创建完成")
            
        except Exception as e:
            print(u"创建UV时发生错误: " + str(e))
            # 最简单的备选方案
            try:
                model_name = cmds.textFieldButtonGrp(self.model_name_field, query=True, text=True)
                if model_name and cmds.objExists(model_name):
                    cmds.select(model_name, replace=True)
                    # 使用最基本的自动投影
                    mel.eval('polyAutoProjection;')
                    print(u"使用基本MEL命令完成UV映射")
            except Exception as e2:
                print(u"所有UV创建方案都失败: " + str(e2))
            
    def delete_skin(self):
        """删除动捕源头模型蒙皮信息"""
        try:
            model_name = cmds.textFieldButtonGrp(self.model_name_field, query=True, text=True)
            if not model_name:
                print(u"错误: 请先设置模型名称")
                return
                
            if cmds.objExists(model_name):
                cmds.select(model_name)
                shapes = cmds.listRelatives(model_name, shapes=True)
                if shapes:
                    skin_clusters = cmds.listConnections(shapes[0], type="skinCluster")
                    if skin_clusters:
                        cmds.delete(skin_clusters)
                        print(u"蒙皮信息删除完成")
                    else:
                        print(u"未找到蒙皮信息")
                else:
                    print(u"错误: 模型没有形状节点")
            else:
                print(u"错误: 模型 " + str(model_name) + u" 不存在")
                
        except Exception as e:
            print(u"删除蒙皮信息时发生错误: " + str(e))
            
    def delete_his(self):
        """删除动捕源头模型非变形器历史"""
        try:
            model_name = cmds.textFieldButtonGrp(self.model_name_field, query=True, text=True)
            if not model_name:
                print(u"错误: 请先设置模型名称")
                return
                
            if cmds.objExists(model_name):
                cmds.select(model_name)
                mel.eval('doBakeNonDefHistory(1, {"prePost"})')
                print(u"非变形器历史删除完成")
            else:
                print(u"错误: 模型 " + str(model_name) + u" 不存在")
                
        except Exception as e:
            print(u"删除历史时发生错误: " + str(e))
            
    def rename_blendshape_node(self):
        """重命名混合形状节点组为Newton_HeadFace_vnBS"""
        try:
            model_name = cmds.textFieldButtonGrp(self.model_name_field, query=True, text=True)
            if not model_name:
                print(u"错误: 请先设置模型名称")
                return False
                
            if not cmds.objExists(model_name):
                print(u"错误: 模型 " + str(model_name) + u" 不存在")
                return False
            
            # 查找模型的混合形状节点
            shapes = cmds.listRelatives(model_name, shapes=True)
            if not shapes:
                print(u"错误: 模型没有形状节点")
                return False
            
            # 获取连接到形状节点的混合形状节点
            blendshape_nodes = cmds.listConnections(shapes[0], type="blendShape")
            if not blendshape_nodes:
                print(u"警告: 未找到混合形状节点")
                return False
            
            # 取第一个混合形状节点
            current_blendshape = blendshape_nodes[0]
            target_name = "Newton_HeadFace_vnBS"
            
            # 检查目标名称是否已存在
            if cmds.objExists(target_name) and current_blendshape != target_name:
                print(u"警告: 目标名称 %s 已存在，将先删除现有节点" % target_name)
                try:
                    cmds.delete(target_name)
                except:
                    print(u"删除现有节点失败，尝试重命名为临时名称")
                    temp_name = target_name + "_old"
                    if cmds.objExists(temp_name):
                        cmds.delete(temp_name)
                    cmds.rename(target_name, temp_name)
            
            # 重命名混合形状节点
            if current_blendshape != target_name:
                try:
                    new_name = cmds.rename(current_blendshape, target_name)
                    print(u"混合形状节点已重命名: %s -> %s" % (current_blendshape, new_name))
                    blendshape_node = new_name
                except Exception as rename_error:
                    print(u"重命名混合形状节点失败: " + safe_unicode_error(rename_error))
                    return False
            else:
                print(u"混合形状节点名称已经是: %s" % target_name)
                blendshape_node = target_name
            
            # 将所有blendShape权重值在第0帧设为0
            try:
                print(u"正在将所有blendShape权重值在第0帧设为0...")
                
                # 获取blendShape节点的所有目标（权重属性）
                weight_attrs = cmds.listAttr(blendshape_node, multi=True, string="weight")
                if weight_attrs:
                    # 设置当前时间为第0帧
                    cmds.currentTime(0)
                    
                    reset_count = 0
                    for attr in weight_attrs:
                        try:
                            full_attr_name = blendshape_node + "." + attr
                            # 设置权重值为0
                            cmds.setAttr(full_attr_name, 0)
                            # 在第0帧设置关键帧
                            cmds.setKeyframe(full_attr_name, time=0, value=0)
                            reset_count += 1
                        except Exception as attr_error:
                            print(u"设置属性 %s 失败: %s" % (attr, safe_unicode_error(attr_error)))
                            continue
                    
                    print(u"已将 %d 个blendShape权重值在第0帧设为0" % reset_count)
                else:
                    print(u"警告: 未找到blendShape权重属性")
                    
            except Exception as reset_error:
                print(u"重置blendShape权重值时发生错误: " + safe_unicode_error(reset_error))
                # 即使重置失败，重命名成功仍返回True
            
            return True
                
        except Exception as e:
            print(u"重命名混合形状节点时发生错误: " + safe_unicode_error(e))
            return False
            
    def create_locator(self):
        """创建约束器"""
        try:
            print(u"=== 开始创建定位器 ===")
            
            model_name = cmds.textFieldButtonGrp(self.model_name_field, query=True, text=True)
            if not model_name:
                print(u"错误: 请先设置模型名称")
                return False
                
            print(u"模型名称: " + str(model_name))
                
            if not cmds.objExists(model_name):
                print(u"错误: 模型 " + str(model_name) + u" 不存在")
                return False
                
            print(u"模型存在，开始创建定位器...")
                
            # 顶点索引字典 - 使用字典形式方便查看对应关系
            vertex_indices_dict = {
                "Lf_browInner_Loc": 2304,
                "Rt_browInner_Loc": 3226, 
                "Lf_browOuter_Loc": 2296, 
                "Rt_browOuter_Loc": 3218, 
                "Lf_eyeLid_Loc": 2451, 
                "Rt_eyeLid_Loc": 3375,
                "Lf_eyeLidStart_Loc": 2451,  # 左眼睑起始位置
                "Lf_eyeLidEnd_Loc": 1625,    # 左眼睑结束位置
                "Rt_eyeLidStart_Loc": 3375,  # 右眼睑起始位置
                "Rt_eyeLidEnd_Loc": 1109,    # 右眼睑结束位置 
                "Lf_eyeBall_Loc": 6103, 
                "Lf_eyeAim_Loc": 5117, 
                "Rt_eyeBall_Loc": 6272, 
                "Rt_eyeAim_Loc": 5550, 
                "Up_mouthLip_Loc": 1549, 
                "Dn_mouthLip_Loc": 1387, 
                "Lf_mouthCorner_Loc": 1891,
                "Rt_mouthCorner_Loc": 2783, 
                "Mi_Jaw_Loc": 2875
            }
            
            # 检查并删除已存在的定位器（现在直接作为模型的子对象）
            # 删除可能存在的旧定位器组
            if cmds.objExists("vertexLocators"):
                cmds.delete("vertexLocators")
                print(u"已删除现有的定位器组")
            
            print(u"定位器将直接创建为模型的子对象")
            
            # 创建或查找Facial_Animation_GRP总组
            facial_animation_grp = "Facial_Animation_GRP"
            if not cmds.objExists(facial_animation_grp):
                facial_animation_grp = cmds.group(empty=True, name=facial_animation_grp)
                print(u"创建Facial_Animation_GRP总组: " + str(facial_animation_grp))
            else:
                print(u"找到已存在的Facial_Animation_GRP总组")
            
            # 确保Newton_HeadFace在Facial_Animation_GRP下
            if cmds.objExists(model_name):
                current_parent = cmds.listRelatives(model_name, parent=True)
                if not current_parent or current_parent[0] != facial_animation_grp:
                    cmds.parent(model_name, facial_animation_grp)
                    print(u"Newton_HeadFace已父级到Facial_Animation_GRP")
            
            # 创建或查找Follow_Face_GRP组
            follow_face_grp = "Follow_Face_GRP"
            if not cmds.objExists(follow_face_grp):
                follow_face_grp = cmds.group(empty=True, name=follow_face_grp)
                print(u"创建Follow_Face_GRP组: " + str(follow_face_grp))
            else:
                print(u"找到已存在的Follow_Face_GRP组")
            
            # 确保Follow_Face_GRP在Facial_Animation_GRP下
            current_parent = cmds.listRelatives(follow_face_grp, parent=True)
            if not current_parent or current_parent[0] != facial_animation_grp:
                cmds.parent(follow_face_grp, facial_animation_grp)
                print(u"Follow_Face_GRP已父级到Facial_Animation_GRP")
            
            success_count = 0
            total_count = len(vertex_indices_dict)
            
            # 遍历字典创建定位器
            for i, (locator_name, vertex_index) in enumerate(vertex_indices_dict.items()):
                try:
                    print(u"正在处理第 %d/%d 个定位器: %s (顶点索引: %d)" % (i+1, total_count, locator_name, vertex_index))
                    
                    vtx = "%s.vtx[%d]" % (model_name, vertex_index)
                    if cmds.objExists(vtx):
                        # 获取顶点位置
                        pos = cmds.pointPosition(vtx, world=True)
                        print(u"  顶点位置: [%.3f, %.3f, %.3f]" % (pos[0], pos[1], pos[2]))
                        
                        # 保存原始顶点位置，特殊处理将在创建locator后进行
                        
                        # 删除已存在的同名定位器
                        if cmds.objExists(locator_name):
                            cmds.delete(locator_name)
                            print(u"  删除已存在的定位器: " + str(locator_name))
                        
                        # 先选择指定的顶点
                        cmds.select(vtx, replace=True)
                        print(u"  已选择顶点: " + str(vtx))
                        
                        # 创建定位器（使用字典中的键作为定位器名称）
                        loc = cmds.spaceLocator(name=locator_name)[0]
                        print(u"  创建定位器: " + str(loc))
                        
                        # 将定位器移动到顶点位置（作为初始位置）
                        cmds.xform(loc, worldSpace=True, translation=pos)
                        print(u"  设置初始位置: [%.3f, %.3f, %.3f]" % (pos[0], pos[1], pos[2]))
                        
                        # 特殊处理定位器位置（应用偏移）
                        if locator_name == "Lf_eyeAim_Loc":
                            pos = [pos[0], pos[1], pos[2] + 3.5]
                        if locator_name == "Rt_eyeAim_Loc":
                            pos = [pos[0], pos[1], pos[2] + 3.5]
                        if locator_name == "Lf_eyeBall_Loc":
                            pos = [pos[0], pos[1], pos[2] - 1.6]
                        if locator_name == "Rt_eyeBall_Loc":
                            pos = [pos[0], pos[1], pos[2] - 1.6]
                        # 新增加的4个眼睑定位器特殊处理
                        if locator_name == "Lf_eyeLidStart_Loc":
                            pos = [pos[0], pos[1], pos[2]]  # 左眼睑起始位置保持原位置
                        if locator_name == "Lf_eyeLidEnd_Loc":
                            pos = [pos[0], pos[1] - 1.67, pos[2]]  # 左眼睑结束位置Y轴下移
                        if locator_name == "Rt_eyeLidStart_Loc":
                            pos = [pos[0], pos[1], pos[2]]  # 右眼睑起始位置保持原位置
                        if locator_name == "Rt_eyeLidEnd_Loc":
                            pos = [pos[0], pos[1] - 1.67, pos[2]]  # 右眼睑结束位置Y轴下移
                        
                        # 重新设置定位器位置（应用偏移后）
                        cmds.xform(loc, worldSpace=True, translation=pos)
                        print(u"  应用偏移后位置: [%.3f, %.3f, %.3f]" % (pos[0], pos[1], pos[2]))
                        
                        # 创建或查找Facial_Animation_GRP总组
                        facial_animation_grp = "Facial_Animation_GRP"
                        if not cmds.objExists(facial_animation_grp):
                            facial_animation_grp = cmds.group(empty=True, name=facial_animation_grp)
                            print(u"  创建Facial_Animation_GRP总组: " + str(facial_animation_grp))
                        else:
                            print(u"  找到已存在的Facial_Animation_GRP总组")
                        
                        # 确保Newton_HeadFace在Facial_Animation_GRP下
                        if cmds.objExists(model_name):
                            current_parent = cmds.listRelatives(model_name, parent=True)
                            if not current_parent or current_parent[0] != facial_animation_grp:
                                cmds.parent(model_name, facial_animation_grp)
                                print(u"  Newton_HeadFace已父级到Facial_Animation_GRP")
                        
                        # 创建或查找Follow_Face_GRP组
                        follow_face_grp = "Follow_Face_GRP"
                        if not cmds.objExists(follow_face_grp):
                            follow_face_grp = cmds.group(empty=True, name=follow_face_grp)
                            print(u"  创建Follow_Face_GRP组: " + str(follow_face_grp))
                        else:
                            print(u"  找到已存在的Follow_Face_GRP组")
                        
                        # 确保Follow_Face_GRP在Facial_Animation_GRP下
                        current_parent = cmds.listRelatives(follow_face_grp, parent=True)
                        if not current_parent or current_parent[0] != facial_animation_grp:
                            cmds.parent(follow_face_grp, facial_animation_grp)
                            print(u"  Follow_Face_GRP已父级到Facial_Animation_GRP")
                        
                        # 父级到Follow_Face_GRP组
                        cmds.parent(loc, follow_face_grp)
                        print(u"  已父级到Follow_Face_GRP组: " + str(follow_face_grp))
                        
                        # 居中轴点
                        cmds.select(loc, replace=True)
                        cmds.CenterPivot()
                        cmds.select(clear=True)
                        
                        # 冻结locator的变换
                        try:
                            cmds.select(loc, replace=True)
                            cmds.makeIdentity(apply=True, translate=True, rotate=True, scale=True, normal=False)
                            print(u"  已冻结locator变换: " + str(loc))
                            cmds.select(clear=True)
                        except Exception as freeze_error:
                            print(u"  冻结locator变换失败: " + str(freeze_error))
                        
                        # 创建点约束：用模型顶点对locator进行约束
                        try:
                            # 删除可能存在的同名约束
                            constraint_name = "%s_pointConstraint" % locator_name
                            if cmds.objExists(constraint_name):
                                cmds.delete(constraint_name)
                                print(u"  删除已存在的约束: " + str(constraint_name))
                            
                            # 选择顶点作为约束源
                            cmds.select(vtx, replace=True)
                            print(u"  选择约束源顶点: " + str(vtx))
                            
                            # 添加locator作为约束目标
                            cmds.select(loc, add=True)
                            print(u"  添加约束目标locator: " + str(loc))
                            
                            # 创建点约束：顶点约束locator
                            # 使用pointOnPolyConstraint，这是Maya中顶点约束的正确方式
                            # maintainOffset=True 保持locator的偏移位置
                            constraint_result = cmds.pointOnPolyConstraint(maintainOffset=True, name=constraint_name)
                            print(u"  创建点约束: " + str(constraint_result))
                            print(u"  约束关系: %s 约束 %s" % (vtx, loc))
                            
                        except Exception as constraint_error:
                            print(u"  点约束创建失败: " + str(constraint_error))
                            print(u"  错误详情: " + str(constraint_error))
                            print(u"  定位器将保持在当前位置")
                        
                        # 清除选择
                        cmds.select(clear=True)
                        
                        success_count += 1
                        print(u"✓ 成功创建定位器: " + str(locator_name) + u" 对应顶点: " + str(vtx))
                        
                    else:
                        print(u"✗ 警告: 顶点 " + str(vtx) + u" 不存在")
                        
                except Exception as loc_error:
                    print(u"✗ 创建定位器 %s 时发生错误: %s" % (locator_name, str(loc_error)))
                    import traceback
                    traceback.print_exc()
                    
            # 输出总结信息
            print(u"\n=== 定位器创建总结 ===")
            print(u"成功创建: %d/%d 个定位器" % (success_count, total_count))
            
            if success_count == total_count:
                print(u"✓ 所有定位器创建成功！")
                return True
            elif success_count > 0:
                print(u"⚠ 部分定位器创建成功，请检查错误信息")
                return True
            else:
                print(u"✗ 没有成功创建任何定位器")
                return False
            
        except Exception as e:
            print(u"创建定位器约束时发生错误: " + str(e))
            import traceback
            traceback.print_exc()
            return False
    
    def on_slider_change(self, param_key, value):
        """滑条值改变时的回调函数"""
        try:
            # 更新参数值
            self.parameters[param_key]["value"] = float(value)
            
            # 更新显示的数值
            updated_text = u"当前值: " + str(round(float(value), 3))
            cmds.text(self.sliders[param_key]["value_label"], 
                     edit=True, 
                     label=updated_text)
            
            # 更新表达式变量 Mapping_Expr
            self.update_expression()
            
            # 打印表达式变量
            print(u"表达式:")
            print(self.aa)
            
        except Exception as e:
            print(u"滑条值更新失败")
            traceback.print_exc()
    
    def update_expression(self):
        """更新表达式显示 - 包括嘴角、上下嘴唇、下颌、眉毛内外侧和眼部控制"""
        try:
            # 获取当前参数值
            mouthCorner = self.parameters["mouth_corner_coeff"]["value"]
            up_lip_coeff = self.parameters["up_lip_coeff"]["value"]
            dn_lip_coeff = self.parameters["dn_lip_coeff"]["value"]
            jaw_coeff = self.parameters["jaw_coeff"]["value"]
            brow_inner_coeff = self.parameters["brow_inner_coeff"]["value"]
            brow_outer_coeff = self.parameters["brow_outer_coeff"]["value"]
            
            # 转换系数为字符串，避免format方法造成乱码
            mouthCorner_str = str(round(mouthCorner, 3))
            up_lip_coeff_str = str(round(up_lip_coeff, 3))
            dn_lip_coeff_str = str(round(dn_lip_coeff, 3))
            jaw_coeff_str = str(round(jaw_coeff, 3))
            brow_inner_coeff_str = str(round(brow_inner_coeff, 3))
            brow_outer_coeff_str = str(round(brow_outer_coeff, 3))
            
            # 设置表达式变量 Mapping_Expr，包含嘴角、上下嘴唇、下颌、眉毛内外侧和眼部表达式组
            self.aa = (
                u"// 眉毛内侧\n"
                u"Lf_browInner_Ctrl.translateX = (clamp(-1, 0, Lf_browInner_Loc.translateX / 0.373)) * " + brow_inner_coeff_str + u";\n"
                u"Rt_browInner_Ctrl.translateX = (clamp(-1, 0, -Rt_browInner_Loc.translateX / 0.373)) * " + brow_inner_coeff_str + u";\n"
                u"Lf_browInner_Ctrl.translateY = (clamp(0, 1, Lf_browInner_Loc.translateY / 1.116) + clamp(-1, 0, Lf_browInner_Loc.translateY / 0.868)) * " + brow_inner_coeff_str + u";\n"
                u"Rt_browInner_Ctrl.translateY = (clamp(0, 1, Rt_browInner_Loc.translateY / 1.116) + clamp(-1, 0, Rt_browInner_Loc.translateY / 0.868)) * " + brow_inner_coeff_str + u";\n"
                
                u"// 眉毛外侧\n"
                u"Lf_browOuter_Ctrl.translateY = (clamp(0, 1, Lf_browOuter_Loc.translateY / 0.833) + clamp(-1, 0, Lf_browOuter_Loc.translateY)) * " + brow_outer_coeff_str + u";\n"
                u"Rt_browOuter_Ctrl.translateY = (clamp(0, 1, Rt_browOuter_Loc.translateY / 0.833) + clamp(-1, 0, Rt_browOuter_Loc.translateY)) * " + brow_outer_coeff_str + u";\n"

                u"// 眼睛\n"
                u"vector $lf_start_pos = `xform -q -ws -t Lf_eyeLidStart_Loc`;\n"
                u"vector $lf_end_pos = `xform -q -ws -t Lf_eyeLidEnd_Loc`;\n"
                u"float $lf_default_distance = mag($lf_end_pos - $lf_start_pos);\n"
                u"vector $lf_move_pos = `xform -q -ws -t Lf_eyeLid_Loc`;\n"
                u"float $lf_move_distance = mag($lf_end_pos - $lf_move_pos);\n"
                u"float $lf_percent = 1 - $lf_move_distance / $lf_default_distance;\n"
                u"Lf_eyeLid_Ctrl.translateY = clamp(0, 1, Lf_eyeLid_Loc.translateY / 0.313) + clamp(-1, 0, -$lf_percent);\n"
                u"\n"
                u"vector $rt_start_pos = `xform -q -ws -t Rt_eyeLidStart_Loc`;\n"
                u"vector $rt_end_pos = `xform -q -ws -t Rt_eyeLidEnd_Loc`;\n"
                u"float $rt_default_distance = mag($rt_end_pos - $rt_start_pos);\n"
                u"vector $rt_move_pos = `xform -q -ws -t Rt_eyeLid_Loc`;\n"
                u"float $rt_move_distance = mag($rt_end_pos - $rt_move_pos);\n"
                u"float $rt_percent = 1 - $rt_move_distance / $rt_default_distance;\n"
                u"Rt_eyeLid_Ctrl.translateY = clamp(0, 1, Rt_eyeLid_Loc.translateY / 0.313) + clamp(-1, 0, -$rt_percent);\n"
                u"\n"

                u"Lf_eyeAim_Ctrl.translateX = Lf_eyeAim_Loc.translateX;\n"
                u"Lf_eyeAim_Ctrl.translateY = Lf_eyeAim_Loc.translateY;\n"
                u"Lf_eyeAim_Ctrl.translateZ = Lf_eyeAim_Loc.translateZ;\n"
                u"Rt_eyeAim_Ctrl.translateX = Rt_eyeAim_Loc.translateX;\n"
                u"Rt_eyeAim_Ctrl.translateY = Rt_eyeAim_Loc.translateY;\n"
                u"Rt_eyeAim_Ctrl.translateZ = Rt_eyeAim_Loc.translateZ;\n"
                
                u"// 下颌\n"
                u"Mi_Jaw_Ctrl.translateX = (clamp(-1, 1, Mi_Jaw_Loc.translateX / 0.982)) * " + jaw_coeff_str + u";\n"
                u"Mi_Jaw_Ctrl.translateY = (min(clamp(-1, 0, Mi_Jaw_Loc.translateY / 2.745), clamp(-1, 0, Mi_Jaw_Loc.translateZ / 2.54))) * " + jaw_coeff_str + u";\n"
                u"Mi_Jaw_Ctrl.translateZ = (clamp(0, 1, Mi_Jaw_Loc.translateZ / 1.215)) * " + jaw_coeff_str + u";\n"
                
                
                u"// 嘴角\n"
                u"Lf_mouthCorner_Ctrl.translateX = (clamp(0, 1, Lf_mouthCorner_Loc.translateX / 1.01) + clamp(-1, 0, clamp(-1, 0, Lf_mouthCorner_Loc.translateX / 0.736) + clamp(0, 1, -Lf_mouthCorner_Loc.translateX / 0.489 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)))) * " + mouthCorner_str + u";\n"
                u"Rt_mouthCorner_Ctrl.translateX = (clamp(0, 1, -Rt_mouthCorner_Loc.translateX / 1.01) + clamp(-1, 0, clamp(-1, 0, -Rt_mouthCorner_Loc.translateX / 0.736) + clamp(0, 1, Rt_mouthCorner_Loc.translateX / 0.489 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)))) * " + mouthCorner_str + u";\n"
                u"Lf_mouthCorner_Ctrl.translateY = (clamp(0, 1, Lf_mouthCorner_Loc.translateY / 1.221) + clamp(-1, 0, clamp(-1, 0, Lf_mouthCorner_Loc.translateY / 1.221) + clamp(0, 1, -Lf_mouthCorner_Loc.translateY / 1.346 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)))) * " + mouthCorner_str + u";\n"
                u"Rt_mouthCorner_Ctrl.translateY = (clamp(0, 1, Rt_mouthCorner_Loc.translateY / 1.221) + clamp(-1, 0, clamp(-1, 0, Rt_mouthCorner_Loc.translateY / 1.221) + clamp(0, 1, -Rt_mouthCorner_Loc.translateY / 1.346 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)))) * " + mouthCorner_str + u";\n"
                u"Lf_mouthCorner_Ctrl.translateZ = (clamp(0, 1, Lf_mouthCorner_Loc.translateZ / 1.656) + clamp(-1, 0, clamp(-1, 0, Lf_mouthCorner_Loc.translateZ / 1.656) + clamp(0, 1, -Lf_mouthCorner_Loc.translateZ / 0.534 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)))) * " + mouthCorner_str + u";\n"
                u"Rt_mouthCorner_Ctrl.translateZ = (clamp(0, 1, Rt_mouthCorner_Loc.translateZ / 1.656) + clamp(-1, 0, clamp(-1, 0, Lf_mouthCorner_Loc.translateZ / 1.656) + clamp(0, 1, -Lf_mouthCorner_Loc.translateZ / 0.534 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)))) * " + mouthCorner_str + u";\n"
                
                u"// 嘴唇\n"
                u"Up_mouthLip_Ctrl.translateX = (clamp(-1, 1,  Up_mouthLip_Loc.translateX / 1.449)) * " + up_lip_coeff_str + u";\n"
                u"Dn_mouthLip_Ctrl.translateX = (clamp(-1, 1,  Dn_mouthLip_Loc.translateX / 1.328)) * " + dn_lip_coeff_str + u";\n"
                u"Up_mouthLip_Ctrl.translateY = (clamp(0, 1,  (Up_mouthLip_Loc.translateY - Lf_mouthCorner_Ctrl.translateX * Rt_mouthCorner_Ctrl.translateX * 0.425) / 1.013) + clamp(-1, 0, Up_mouthLip_Loc.translateY / 0.875)) * " + up_lip_coeff_str + u";\n"
                u"Dn_mouthLip_Ctrl.translateY = (clamp(0, 1,  (Dn_mouthLip_Loc.translateY - Lf_mouthCorner_Ctrl.translateX * Rt_mouthCorner_Ctrl.translateX * 0.812) / 0.812) + clamp(-1, 0, clamp(-1, 0, Dn_mouthLip_Loc.translateY / 1.195) + clamp(0, 1, -Dn_mouthLip_Loc.translateY / 3.7) * clamp(0, 1, -Mi_Jaw_Ctrl.translateY))) * " + dn_lip_coeff_str + u";\n"
                u"Up_mouthLip_Ctrl.translateZ = (clamp(-1, 0, clamp(-1, 0, -Up_mouthLip_Loc.rotateX / 27.225) + clamp(0, 1,  Up_mouthLip_Loc.rotateX / 0.329 * Lf_mouthCorner_Ctrl.translateX * Rt_mouthCorner_Ctrl.translateX))) * " + up_lip_coeff_str + u";\n"
                u"Dn_mouthLip_Ctrl.translateZ = (clamp(-1, 0, clamp(-1, 0,  Dn_mouthLip_Loc.rotateX / 55.783) + clamp(0, 1, -Dn_mouthLip_Loc.rotateX / 5.247 * Lf_mouthCorner_Ctrl.translateX * Rt_mouthCorner_Ctrl.translateX))) * " + dn_lip_coeff_str + u";\n"
                
                
            )
                
        except Exception as e:
            print(u"表达式更新失败")
            traceback.print_exc()
    
    def save_expression_preset(self, preset_name, expression_string, parameter_values):
        """保存表达式预设"""
        try:
            # 获取脚本文件自身的路径
            current_path = self.get_script_path()
            # 创建预设文件夹路径
            preset_dir = os.path.join(current_path, u"presets")
            
            # 如果预设文件夹不存在，则创建
            if not os.path.exists(preset_dir):
                os.makedirs(preset_dir)
            
            # 构建预设数据
            preset_data = {
                u"name": preset_name,
                u"expression": expression_string,
                u"parameters": parameter_values,
                u"create_time": datetime.now().strftime(u"%Y-%m-%d %H:%M:%S"),
                u"description": u"嘴角控制器表达式预设"
            }
            
            # 简化文件名处理，避免URL编码导致的乱码
            # 确保preset_name是unicode类型
            if isinstance(preset_name, str):
                try:
                    safe_preset_name = preset_name.decode(u'utf-8')
                except UnicodeDecodeError:
                    safe_preset_name = preset_name
            else:
                safe_preset_name = preset_name
            
            # 直接使用文件名，不进行URL编码
            # 如果文件名包含不安全字符，则替换为安全字符
            import re
            # 移除或替换文件名中的不安全字符
            safe_filename = re.sub(r'[<>:"/\\|?*]', '_', safe_preset_name)
            file_path = os.path.join(preset_dir, u"%s.json" % safe_filename)
            
            # 确保文件路径中的中文能正确处理
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
            
            with codecs.open(file_path, u'w', encoding=u"utf-8") as f:
                json.dump(preset_data, f, indent=4, ensure_ascii=False)
            
            print(u"表达式预设已保存: %s" % preset_name)
            return True
        except Exception as e:
            # 在Maya Python2环境中正确处理包含非ASCII字符的异常
            try:
                error_msg = unicode(str(e), u'utf-8')
            except:
                try:
                    error_msg = str(e).decode(u'utf-8')
                except:
                    error_msg = repr(e)
            print(u"保存表达式预设失败: %s" % error_msg)
            traceback.print_exc()
            return False
    
    def load_expression_preset(self, preset_name):
        """加载表达式预设"""
        try:
            # 获取脚本文件自身的路径
            current_path = self.get_script_path()
            # 创建预设文件夹路径
            preset_dir = os.path.join(current_path, u"presets")
            
            # 简化文件路径处理，避免URL编码
            # 确保preset_name是unicode类型
            if isinstance(preset_name, str):
                try:
                    safe_preset_name = preset_name.decode(u'utf-8')
                except UnicodeDecodeError:
                    safe_preset_name = preset_name
            else:
                safe_preset_name = preset_name
            
            # 直接使用文件名，与保存时的逻辑保持一致
            import re
            safe_filename = re.sub(r'[<>:"/\\|?*]', '_', safe_preset_name)
            file_path = os.path.join(preset_dir, u"%s.json" % safe_filename)
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                print(u"预设文件不存在: %s" % preset_name)
                return None
                
            # 读取JSON文件
            with codecs.open(file_path, u'r', encoding=u"utf-8") as f:
                preset_data = json.load(f)
            
            print(u"加载表达式预设: %s" % preset_name)
            return preset_data
        except Exception as e:
            # 在Maya Python2环境中正确处理包含非ASCII字符的异常
            try:
                error_msg = unicode(str(e), u'utf-8')
            except:
                try:
                    error_msg = str(e).decode(u'utf-8')
                except:
                    error_msg = repr(e)
            print(u"加载表达式预设时发生错误: %s" % error_msg)
            traceback.print_exc()
            return None
    
    def get_preset_files(self):
        """获取所有预设文件列表"""
        try:
            # 获取脚本文件自身的路径
            current_path = self.get_script_path()
            # 创建预设文件夹路径
            preset_dir = os.path.join(current_path, u"presets")
            
            # 检查文件夹是否存在
            if not os.path.exists(preset_dir):
                return []
                
            # 获取所有.json文件
            preset_files = []
                
            for file_name in os.listdir(preset_dir):
                if file_name.endswith(u'.json'):
                    # 简化文件名处理，直接去除.json后缀
                    try:
                        base_name = file_name[:-5]  # 去掉.json后缀
                        
                        # 确保文件名是unicode类型
                        if isinstance(base_name, str):
                            try:
                                preset_name = base_name.decode(u'utf-8')
                            except UnicodeDecodeError:
                                # 如果解码失败，直接使用原始名称
                                preset_name = base_name
                        else:
                            preset_name = base_name
                            
                    except Exception as e:
                        # 在Maya Python2环境中正确处理包含非ASCII字符的异常
                        try:
                            error_msg = unicode(str(e), u'utf-8')
                        except:
                            try:
                                error_msg = str(e).decode(u'utf-8')
                            except:
                                error_msg = repr(e)
                        print(u"处理文件名时发生错误: %s" % error_msg)
                        # 使用原始文件名（去掉.json后缀）
                        preset_name = file_name[:-5] if file_name.endswith(u'.json') else file_name
                        
                    preset_files.append(preset_name)
                    
            return sorted(preset_files)
        except Exception as e:
            # 在Maya Python2环境中正确处理包含非ASCII字符的异常
            try:
                error_msg = unicode(str(e), u'utf-8')
            except:
                try:
                    error_msg = str(e).decode(u'utf-8')
                except:
                    error_msg = repr(e)
            print(u"获取预设文件列表时发生错误: %s" % error_msg)
            traceback.print_exc()
            return []
    
    def save_preset_file(self, expression_content):
        u"""保存表达式到预设文件"""
        try:
            # 获取脚本文件自身的路径
            current_dir = self.get_script_path()
            # 创建预设文件夹路径
            preset_dir = os.path.join(current_dir, "presets")
            
            # 如果预设文件夹不存在，则创建
            if not os.path.exists(preset_dir):
                os.makedirs(preset_dir)
            
            # 创建文件名（使用时间戳确保唯一性）
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = "mouth_corner_preset_%s.txt" % timestamp
            file_path = os.path.join(preset_dir, filename)
            
            # 保存表达式到文件
            with codecs.open(file_path, "w", encoding="utf-8") as f:
                f.write(expression_content)
            
            print(u"表达式已保存到预设文件: %s" % file_path)
            return file_path
        except Exception as e:
            print(u"保存预设文件失败: %s" % str(e))
            traceback.print_exc()
            return None
    
    def execute_mapping_expr(self):
        u"""执行表达式 Mapping_Expr"""
        try:
            # 先根据当前滑条值重新生成表达式
            self.update_expression()
            
            # 获取当前的 Mapping_Expr 表达式
            expression_content = self.aa
            
            # 提取表达式内容（去掉 Mapping_Expr = 部分）
            if expression_content.startswith(u"Mapping_Expr = "):
                actual_expression = expression_content[15:]  # 去掉 "Mapping_Expr = "
            else:
                actual_expression = expression_content
            
            # 在Maya中执行表达式
            print(u"\n正在执行表达式")
            print(u"表达式内容:")
            print(actual_expression)
            
            # 检查是否所有滑条值都为默认值1.0
            all_default = True
            for param_key, param_info in self.parameters.items():
                if abs(param_info["value"] - 1.0) > 0.001:  # 考虑浮点数精度问题
                    all_default = False
                    break
            
            # 只有当滑条值不全为默认值1.0时才保存默认预设
            if not all_default:
                # 获取当前参数值用于保存
                current_parameters = {}
                for key, value in self.parameters.items():
                    current_parameters[key] = value["value"]
                
                # 检查是否所有滑条值都为默认值1.0，避免创建不必要的默认预设
                all_default = True
                for param_key, param_info in self.parameters.items():
                    if abs(param_info["value"] - 1.0) > 0.001:  # 考虑浮点数精度问题
                        all_default = False
                        break
                
                # 只有当滑条值不全为默认值1.0时才保存默认预设
                if not all_default:
                    self.save_expression_preset("默认", actual_expression, current_parameters)
            
            # 删除已存在的Mapping_Expr表达式
            self.cleanup_existing_expressions()
            
            # 删除旧表达式并创建新的（与facial_binding_tool_from_mel.py中的方法一致）
            if cmds.objExists("Mapping_Expr"):
                cmds.delete("Mapping_Expr")
                
                cmds.expression(name="Mapping_Expr", string=actual_expression)
            
            # 显示成功信息
            cmds.confirmDialog(
                title=u"执行成功",
                message=u"表达式已成功执行",
                button=[u"确定"],
                defaultButton=u"确定"
            )
            
            print(u"表达式执行成功")
                
        except Exception as e:
            traceback.print_exc()
            
            # 显示错误信息
            cmds.confirmDialog(
                title=u"执行失败",
                message=u"表达式执行失败，请检查Maya中是否存在相关的控制器对象",
                button=[u"确定"],
                defaultButton=u"确定",
                icon=u"warning"
            )
    
    def create_default_expression(self):
        """创建默认的Mapping_Expr表达式 - 规范化书写"""
        try:
            # 检查必需的定位器是否存在
            required_locators = [
                "Lf_browInner_Loc", "Rt_browInner_Loc", "Lf_browOuter_Loc", "Rt_browOuter_Loc",
                "Lf_eyeLid_Loc", "Rt_eyeLid_Loc", "Lf_eyeLidStart_Loc", "Lf_eyeLidEnd_Loc", 
                "Rt_eyeLidStart_Loc", "Rt_eyeLidEnd_Loc", "Lf_eyeBall_Loc", "Rt_eyeBall_Loc",
                "Lf_eyeAim_Loc", "Rt_eyeAim_Loc", "Up_mouthLip_Loc", "Dn_mouthLip_Loc",
                "Lf_mouthCorner_Loc", "Rt_mouthCorner_Loc", "Mi_Jaw_Loc"
            ]
            
            missing_locators = []
            for loc_name in required_locators:
                if not cmds.objExists(loc_name):
                    missing_locators.append(loc_name)
            
            if missing_locators:
                error_msg = u"缺少必需的定位器，请先创建定位器:\n" + u"\n".join(missing_locators)
                print(error_msg)
                cmds.confirmDialog(
                    title=u"缺少定位器",
                    message=error_msg,
                    button=[u"确定"],
                    defaultButton=u"确定",
                    icon=u"warning"
                )
                return False
            
            # 定义默认表达式内容 - 规范化格式
            default_expression = (
                u"// 眉毛\n"
                u"Lf_browInner_Ctrl.translateX = clamp(-1, 0, Lf_browInner_Loc.translateX / 0.373);\n"
                u"Rt_browInner_Ctrl.translateX = clamp(-1, 0, -Rt_browInner_Loc.translateX / 0.373);\n"
                u"Lf_browInner_Ctrl.translateY = clamp(0, 1, Lf_browInner_Loc.translateY / 1.116) + clamp(-1, 0, Lf_browInner_Loc.translateY / 0.868);\n"
                u"Rt_browInner_Ctrl.translateY = clamp(0, 1, Rt_browInner_Loc.translateY / 1.116) + clamp(-1, 0, Rt_browInner_Loc.translateY / 0.868);\n"
                u"Lf_browOuter_Ctrl.translateY = clamp(0, 1, Lf_browOuter_Loc.translateY / 0.833) + clamp(-1, 0, Lf_browOuter_Loc.translateY);\n"
                u"Rt_browOuter_Ctrl.translateY = clamp(0, 1, Rt_browOuter_Loc.translateY / 0.833) + clamp(-1, 0, Rt_browOuter_Loc.translateY);\n"
                u"\n"
                u"// 眼睛\n"
                u"vector $lf_start_pos = `xform -q -ws -t Lf_eyeLidStart_Loc`;\n"
                u"vector $lf_end_pos = `xform -q -ws -t Lf_eyeLidEnd_Loc`;\n"
                u"float $lf_default_distance = mag($lf_end_pos - $lf_start_pos);\n"
                u"vector $lf_move_pos = `xform -q -ws -t Lf_eyeLid_Loc`;\n"
                u"float $lf_move_distance = mag($lf_end_pos - $lf_move_pos);\n"
                u"float $lf_percent = 1 - $lf_move_distance / $lf_default_distance;\n"
                u"Lf_eyeLid_Ctrl.translateY = clamp(0, 1, Lf_eyeLid_Loc.translateY / 0.313) + clamp(-1, 0, -$lf_percent);\n"
                u"\n"
                u"vector $rt_start_pos = `xform -q -ws -t Rt_eyeLidStart_Loc`;\n"
                u"vector $rt_end_pos = `xform -q -ws -t Rt_eyeLidEnd_Loc`;\n"
                u"float $rt_default_distance = mag($rt_end_pos - $rt_start_pos);\n"
                u"vector $rt_move_pos = `xform -q -ws -t Rt_eyeLid_Loc`;\n"
                u"float $rt_move_distance = mag($rt_end_pos - $rt_move_pos);\n"
                u"float $rt_percent = 1 - $rt_move_distance / $rt_default_distance;\n"
                u"Rt_eyeLid_Ctrl.translateY = clamp(0, 1, Rt_eyeLid_Loc.translateY / 0.313) + clamp(-1, 0, -$rt_percent);\n"
                u"\n"
                u"Lf_eyeAim_Ctrl.translateX = Lf_eyeAim_Loc.translateX;\n"
                u"Lf_eyeAim_Ctrl.translateY = Lf_eyeAim_Loc.translateY;\n"
                u"Lf_eyeAim_Ctrl.translateZ = Lf_eyeAim_Loc.translateZ;\n"
                u"Rt_eyeAim_Ctrl.translateX = Rt_eyeAim_Loc.translateX;\n"
                u"Rt_eyeAim_Ctrl.translateY = Rt_eyeAim_Loc.translateY;\n"
                u"Rt_eyeAim_Ctrl.translateZ = Rt_eyeAim_Loc.translateZ;\n"
                u"\n"
                u"// 下颌\n"
                u"Mi_Jaw_Ctrl.translateX = clamp(-1, 1, Mi_Jaw_Loc.translateX / 0.982);\n"
                u"Mi_Jaw_Ctrl.translateY = min(clamp(-1, 0, Mi_Jaw_Loc.translateY / 2.745), clamp(-1, 0, Mi_Jaw_Loc.translateZ / 2.54));\n"
                u"Mi_Jaw_Ctrl.translateZ = clamp(0, 1, Mi_Jaw_Loc.translateZ / 1.215);\n"
                u"\n"
                u"// 嘴角\n"
                u"Lf_mouthCorner_Ctrl.translateX = clamp(0, 1, Lf_mouthCorner_Loc.translateX / 1.01) + clamp(-1, 0, clamp(-1, 0, Lf_mouthCorner_Loc.translateX / 0.736) + clamp(0, 1, -Lf_mouthCorner_Loc.translateX / 0.489 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)));\n"
                u"Rt_mouthCorner_Ctrl.translateX = clamp(0, 1, -Rt_mouthCorner_Loc.translateX / 1.01) + clamp(-1, 0, clamp(-1, 0, -Rt_mouthCorner_Loc.translateX / 0.736) + clamp(0, 1, Rt_mouthCorner_Loc.translateX / 0.489 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)));\n"
                u"Lf_mouthCorner_Ctrl.translateY = clamp(0, 1, Lf_mouthCorner_Loc.translateY / 1.221) + clamp(-1, 0, clamp(-1, 0, Lf_mouthCorner_Loc.translateY / 1.221) + clamp(0, 1, -Lf_mouthCorner_Loc.translateY / 1.346 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)));\n"
                u"Rt_mouthCorner_Ctrl.translateY = clamp(0, 1, Rt_mouthCorner_Loc.translateY / 1.221) + clamp(-1, 0, clamp(-1, 0, Rt_mouthCorner_Loc.translateY / 1.221) + clamp(0, 1, -Rt_mouthCorner_Loc.translateY / 1.346 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)));\n"
                u"Lf_mouthCorner_Ctrl.translateZ = clamp(0, 1, Lf_mouthCorner_Loc.translateZ / 1.656) + clamp(-1, 0, clamp(-1, 0, Lf_mouthCorner_Loc.translateZ / 1.656) + clamp(0, 1, -Lf_mouthCorner_Loc.translateZ / 0.534 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)));\n"
                u"Rt_mouthCorner_Ctrl.translateZ = clamp(0, 1, Rt_mouthCorner_Loc.translateZ / 1.656) + clamp(-1, 0, clamp(-1, 0, Lf_mouthCorner_Loc.translateZ / 1.656) + clamp(0, 1, -Lf_mouthCorner_Loc.translateZ / 0.534 * clamp(0, 1, -Mi_Jaw_Ctrl.translateY)));\n"
                u"\n"
                u"// 嘴唇\n"
                u"Up_mouthLip_Ctrl.translateX = clamp(-1, 1, Up_mouthLip_Loc.translateX / 1.449);\n"
                u"Dn_mouthLip_Ctrl.translateX = clamp(-1, 1, Dn_mouthLip_Loc.translateX / 1.328);\n"
                u"Up_mouthLip_Ctrl.translateY = clamp(0, 1, (Up_mouthLip_Loc.translateY - Lf_mouthCorner_Ctrl.translateX * Rt_mouthCorner_Ctrl.translateX * 0.425) / 1.013) + clamp(-1, 0, Up_mouthLip_Loc.translateY / 0.875);\n"
                u"Dn_mouthLip_Ctrl.translateY = clamp(0, 1, (Dn_mouthLip_Loc.translateY - Lf_mouthCorner_Ctrl.translateX * Rt_mouthCorner_Ctrl.translateX * 0.812) / 0.812) + clamp(-1, 0, clamp(-1, 0, Dn_mouthLip_Loc.translateY / 1.195) + clamp(0, 1, -Dn_mouthLip_Loc.translateY / 3.7) * clamp(0, 1, -Mi_Jaw_Ctrl.translateY));\n"
                u"Up_mouthLip_Ctrl.translateZ = clamp(-1, 0, clamp(-1, 0, -Up_mouthLip_Loc.rotateX / 27.225) + clamp(0, 1, Up_mouthLip_Loc.rotateX / 0.329 * Lf_mouthCorner_Ctrl.translateX * Rt_mouthCorner_Ctrl.translateX));\n"
                u"Dn_mouthLip_Ctrl.translateZ = clamp(-1, 0, clamp(-1, 0, Dn_mouthLip_Loc.rotateX / 55.783) + clamp(0, 1, -Dn_mouthLip_Loc.rotateX / 5.247 * Lf_mouthCorner_Ctrl.translateX * Rt_mouthCorner_Ctrl.translateX));\n"
            )
            
            # 清理已存在的表达式
            self.cleanup_existing_expressions()
            
            # 创建新的默认表达式
            cmds.expression(name="Mapping_Expr", string=default_expression)
            print(u"默认表达式 Mapping_Expr 创建成功")
            
            return True
            
        except Exception as e:
            error_msg = u"创建默认表达式失败: " + str(e)
            print(error_msg)
            traceback.print_exc()
            return False
    
    def cleanup_existing_expressions(self):
        """清理已存在的Mapping_Expr表达式"""
        try:
            # 只检查是否存在名为"Mapping_Expr"的表达式
            if cmds.objExists("Mapping_Expr"):
                try:
                    cmds.delete("Mapping_Expr")
                    print(u"已删除表达式: Mapping_Expr")
                except Exception as e:
                    print(u"删除表达式失败: Mapping_Expr")
                    traceback.print_exc()
            else:
                print(u"未发现需要删除的Mapping_Expr表达式")
                
        except Exception as e:
            print(u"清理表达式失败")
            traceback.print_exc()
    
    def get_current_values(self):
        """获取当前所有参数值"""
        return {
            u"嘴角控制系数": self.parameters["mouth_corner_coeff"]["value"],
            u"上嘴唇控制系数": self.parameters["up_lip_coeff"]["value"],
            u"下嘴唇控制系数": self.parameters["dn_lip_coeff"]["value"],
            u"下颌控制系数": self.parameters["jaw_coeff"]["value"],
            u"眉毛内侧控制系数": self.parameters["brow_inner_coeff"]["value"],
            u"眉毛外侧控制系数": self.parameters["brow_outer_coeff"]["value"]
        }
    
    def get_expression_variable(self):
        """获取表达式变量 Mapping_Expr 的值"""
        return self.aa
    
    def close_window(self):
        """关闭窗口"""
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name, window=True)
    
    def on_preset_selection_changed(self, selection):
        """预设选择变化时的回调函数"""
        try:
            print(u"选择了预设: {}".format(selection))
            
            # 如果选择的是默认预设，重置滑条到默认值1.0
            if selection == u"默认":
                print(u"重置到默认预设")
                # 重置所有滑条到默认值1.0
                for param_key, param_info in self.parameters.items():
                    default_value = 1.0  # 所有参数的默认值设为1.0
                    if param_key in self.sliders:
                        slider = self.sliders[param_key]["slider"]
                        value_label = self.sliders[param_key]["value_label"]
                        
                        # 更新滑条值
                        cmds.floatSlider(slider, edit=True, value=default_value)
                        
                        # 更新显示的数值
                        updated_text = u"当前值: " + str(round(default_value, 3))
                        cmds.text(value_label, edit=True, label=updated_text)
                        
                        # 更新参数值
                        self.parameters[param_key]["value"] = default_value
                
                # 执行默认表达式
                print(u"执行默认表达式...")
                if self.create_default_expression():
                    print(u"默认表达式执行成功")
                else:
                    print(u"默认表达式执行失败")
                return
            
            # 加载并应用新选择的预设（不保存当前预设）
            print(u"加载并应用新预设: {}".format(selection))
            self.load_and_apply_preset(selection)
        except Exception as e:
            print(u"预设选择变化时发生错误: {}".format(str(e)))
            traceback.print_exc()
    
    def load_and_apply_preset(self, preset_name):
        """加载并应用预设"""
        try:
            # 加载预设数据
            preset_data = self.load_expression_preset(preset_name)
            if not preset_data:
                print(u"无法加载预设: %s" % preset_name)
                return False
                
            print(u"加载的预设数据: {}".format(preset_name))
            print(u"预设中的参数键: {}".format(list(preset_data.get("parameters", {}).keys())))
            print(u"当前参数键: {}".format(list(self.parameters.keys())))
            print(u"当前滑条键: {}".format(list(self.sliders.keys())))
                
            # 应用参数值到滑条
            if "parameters" in preset_data:
                param_updates = 0
                for param_key, value in preset_data["parameters"].items():
                    print(u"处理参数: {} = {}".format(param_key, value))
                    # 检查参数键是否存在于当前参数和滑条中
                    if param_key in self.parameters:
                        print(u"参数键 {} 存在于 self.parameters 中".format(param_key))
                    else:
                        print(u"参数键 {} 不存在于 self.parameters 中".format(param_key))
                        
                    if param_key in self.sliders:
                        print(u"参数键 {} 存在于 self.sliders 中".format(param_key))
                    else:
                        print(u"参数键 {} 不存在于 self.sliders 中".format(param_key))
                    
                    if param_key in self.parameters and param_key in self.sliders:
                        try:
                            print(u"更新参数和滑条: {}".format(param_key))
                            # 更新参数值
                            self.parameters[param_key]["value"] = float(value)
                            
                            # 更新滑条值
                            slider = self.sliders[param_key]["slider"]
                            value_label = self.sliders[param_key]["value_label"]
                            
                            cmds.floatSlider(slider, edit=True, value=float(value))
                            
                            # 更新显示的数值
                            updated_text = u"当前值: " + str(round(float(value), 3))
                            cmds.text(value_label, edit=True, label=updated_text)
                            
                            param_updates += 1
                            print(u"已更新滑条: {} = {}".format(param_key, value))
                        except Exception as update_error:
                            print(u"更新滑条 {} 时发生错误: {}".format(param_key, str(update_error)))
                    else:
                        print(u"跳过参数(不在当前参数或滑条中): {}".format(param_key))
                
                print(u"已应用预设参数: {}，共更新了 {} 个参数".format(preset_name, param_updates))
                
            # 应用表达式
            if "expression" in preset_data:
                # 删除旧表达式
                if cmds.objExists("Mapping_Expr"):
                    cmds.delete("Mapping_Expr")
                    
                # 创建新表达式并添加错误处理
                try:
                    print(preset_data["expression"])
                    cmds.expression(name="Mapping_Expr", string=preset_data["expression"])
                    print(u"表达式 Mapping_Expr 创建成功")
                except Exception as expr_error:
                    print(u"创建表达式 Mapping_Expr 失败: {}".format(str(expr_error)))
                    # 显示错误信息
                    cmds.confirmDialog(
                        title=u"表达式创建失败",
                        message=u"创建表达式失败，请检查表达式内容是否正确\n错误信息: {}".format(str(expr_error)),
                        button=[u"确定"],
                        defaultButton=u"确定",
                        icon=u"warning"
                    )
                    return False
                # print(u"已应用预设表达式: ",)
                
                
            return True
        except Exception as e:
            print(u"加载并应用预设时发生错误: %s" % str(e))
            traceback.print_exc()
            return False
    
    def update_preset_menu(self):
        """更新预设菜单"""
        try:
            # 清空现有菜单项
            try:
                cmds.optionMenu(self.preset_option_menu, edit=True, deleteAllItems=True)
            except:
                pass
            
            # 添加默认选项
            cmds.menuItem(label=u"默认", parent=self.preset_option_menu)
            
            # 获取并添加所有预设文件
            preset_files = self.get_preset_files()
            for preset_name in preset_files:
                # 确保preset_name是unicode类型
                if isinstance(preset_name, str):
                    try:
                        display_name = preset_name.decode(u'utf-8')
                    except:
                        display_name = preset_name
                else:
                    display_name = preset_name
                cmds.menuItem(label=display_name, parent=self.preset_option_menu)
                
            print(u"预设菜单已更新，共 %d 个预设" % len(preset_files))
            
        except Exception as e:
            # 在Maya Python2环境中正确处理包含非ASCII字符的异常
            try:
                error_msg = unicode(str(e), u'utf-8')
            except:
                try:
                    error_msg = str(e).decode(u'utf-8')
                except:
                    error_msg = repr(e)
            print(u"更新预设菜单时发生错误: %s" % error_msg)
            traceback.print_exc()
    
    def delete_selected_preset(self, *args):
        """删除选中的预设"""
        try:
            # 获取当前选中的预设
            selected_preset = cmds.optionMenu(self.preset_option_menu, query=True, value=True)
            
            # 不能删除默认选项
            if selected_preset == u"默认":
                cmds.confirmDialog(
                    title=u"提示",
                    message=u"无法删除默认预设",
                    button=[u"确定"],
                    defaultButton=u"确定"
                )
                return
            
            # 确认删除
            result = cmds.confirmDialog(
                title=u"确认删除",
                message=u"确定要删除预设 %s 吗？此操作不可恢复！" % selected_preset,
                button=[u"删除", u"取消"],
                defaultButton=u"取消",
                cancelButton=u"取消",
                dismissString=u"取消"
            )
            
            if result == u"删除":
                try:
                    # 获取预设文件路径并删除，简化文件名处理
                    current_path = self.get_script_path()
                    preset_dir = os.path.join(current_path, u"presets")
                    
                    # 确保selected_preset是unicode类型
                    if isinstance(selected_preset, str):
                        try:
                            safe_preset_name = selected_preset.decode(u'utf-8')
                        except UnicodeDecodeError:
                            safe_preset_name = selected_preset
                    else:
                        safe_preset_name = selected_preset
                    
                    # 直接使用文件名，与保存时的逻辑保持一致
                    import re
                    safe_filename = re.sub(r'[<>:"/\\|?*]', '_', safe_preset_name)
                    file_path = os.path.join(preset_dir, u"%s.json" % safe_filename)
                    
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(u"预设 {} 已删除".format(selected_preset))
                        
                        # 更新预设菜单
                        self.update_preset_menu()
                        
                        # 重置所有滑条到默认值1.0
                        for param_key, param_info in self.parameters.items():
                            default_value = 1.0  # 所有参数的默认值设为1.0
                            if param_key in self.sliders:
                                slider = self.sliders[param_key][u"slider"]
                                value_label = self.sliders[param_key][u"value_label"]
                                
                                # 更新滑条值
                                cmds.floatSlider(slider, edit=True, value=default_value)
                                
                                # 更新显示的数值
                                updated_text = u"当前值: " + str(round(default_value, 3))
                                cmds.text(value_label, edit=True, label=updated_text)
                                
                                # 更新参数值
                                self.parameters[param_key][u"value"] = default_value
                        
                        # 删除成功后不再显示提示弹窗，只在控制台打印信息
                        # cmds.confirmDialog(
                        #     title=u"删除成功",
                        #     message=u"预设 %s 已删除成功" % selected_preset,
                        #     button=[u"确定"],
                        #     defaultButton=u"确定"
                        # )
                    else:
                        print(u"预设文件不存在: %s" % selected_preset)
                        
                except Exception as e:
                    # 在Maya Python2环境中正确处理包含非ASCII字符的异常
                    try:
                        error_msg = unicode(str(e), u'utf-8')
                    except:
                        try:
                            error_msg = str(e).decode(u'utf-8')
                        except:
                            error_msg = repr(e)
                    print(u"删除预设时发生错误: %s" % error_msg)
                    traceback.print_exc()
                    
                    # 显示错误信息
                    cmds.confirmDialog(
                        title=u"删除失败",
                        message=u"删除预设失败: %s" % error_msg,
                        button=[u"确定"],
                        defaultButton=u"确定"
                    )
        except Exception as e:
            # 在Maya Python2环境中正确处理包含非ASCII字符的异常
            try:
                error_msg = unicode(str(e), u'utf-8')
            except:
                try:
                    error_msg = str(e).decode(u'utf-8')
                except:
                    error_msg = repr(e)
            print(u"删除选中预设时发生错误: %s" % error_msg)
            traceback.print_exc()
    
    def update_expression_with_preset_save(self, *args):
        """更新表达式并保存为当前预设"""
        print(u"=== 开始执行 update_expression_with_preset_save 函数 ===")
        try:
            # 先执行表达式更新
            print(u"步骤1：更新表达式...")
            self.update_expression()
            
            # 获取当前表达式内容
            expression_content = self.aa
            
            # 获取当前参数值用于保存
            current_parameters = {}
            for key, value in self.parameters.items():
                current_parameters[key] = value[u"value"]
            
            # 检查是否所有滑条值都为默认值1.0
            all_default = True
            for param_key, param_info in self.parameters.items():
                if abs(param_info[u"value"] - 1.0) > 0.001:  # 考虑浮点数精度问题
                    all_default = False
                    break
            
            # 获取当前选中的预设
            print(u"步骤2：获取当前选中的预设...")
            current_selected_preset = self.get_current_selected_preset()
            
            # 参考facial_binding_tool_from_mel.py的逻辑
            if current_selected_preset == u"默认":
                # 如果当前选中的是默认预设
                if all_default:
                    # 如果所有滑条值都为默认值1.0，不创建新的默认预设，只更新表达式
                    print(u"所有滑条值都为默认值1.0，不创建新的默认预设，只更新Maya表达式")
                    # 直接在Maya中创建或更新表达式，不保存预设文件
                    self.cleanup_existing_expressions()
                    if cmds.objExists("Mapping_Expr"):
                        cmds.delete("Mapping_Expr")
                        cmds.expression(name="Mapping_Expr", string=expression_content)
                    print(u"已在Maya中更新表达式: Mapping_Expr")
                    print(u"由于参数都是默认值，未创建新的预设文件")
                else:
                    # 如果滑条值不全为默认值，则显示对话框让用户输入新预设名
                    print(u"当前选中默认预设，但滑条值不全为默认值，显示保存对话框...")
                    self.show_preset_save_dialog(expression_content, current_parameters)
            else:
                # 如果当前选中的预设不是默认预设，直接保存到当前选中的预设，不显示对话框
                # 在打印包含中文的预设名称时，确保正确处理编码
                try:
                    print(u"直接保存到当前预设: " + current_selected_preset.decode(u'utf-8'))
                except:
                    try:
                        print(u"直接保存到当前预设: " + current_selected_preset)
                    except:
                        print(u"直接保存到当前预设")
                if self.save_expression_preset(current_selected_preset, expression_content, current_parameters):
                    print(u"表达式预设 " + current_selected_preset + u" 已直接覆盖保存成功")
                    # 更新预设菜单
                    self.update_preset_menu()
                    # 选中刚刚保存的预设
                    try:
                        cmds.optionMenu(self.preset_option_menu, edit=True, value=current_selected_preset)
                    except:
                        pass
                    # 在打印包含中文的预设名称时，确保正确处理编码
                    try:
                        print(u"已更新预设菜单并选中预设: " + current_selected_preset.decode(u'utf-8'))
                    except:
                        try:
                            print(u"已更新预设菜单并选中预设: " + current_selected_preset)
                        except:
                            print(u"已更新预设菜单并选中预设")
                else:
                    print(u"保存预设失败")
                    # 显示错误信息
                    cmds.confirmDialog(
                        title=u"保存失败",
                        message=u"保存预设时发生错误，请检查文件权限或磁盘空间",
                        button=[u"确定"],
                        defaultButton=u"确定"
                    )
            
            print(u"=== update_expression_with_preset_save 函数执行完成 ===")
            
        except Exception as e:
            # 在Maya Python2环境中正确处理包含非ASCII字符的异常
            try:
                error_msg = unicode(str(e), u'utf-8')
            except:
                try:
                    error_msg = str(e).decode(u'utf-8')
                except:
                    error_msg = repr(e)
            print(u"更新表达式并保存预设时发生错误: %s" % error_msg)
            traceback.print_exc()
            # 显示错误信息
            cmds.confirmDialog(
                title=u"保存失败",
                message=u"更新表达式并保存预设时发生错误: %s" % error_msg,
                button=[u"确定"],
                defaultButton=u"确定"
            )
    
    def get_current_selected_preset(self): 
        """获取当前选中的预设名称"""
        try:
            if not self.preset_option_menu or not cmds.optionMenu(self.preset_option_menu, exists=True):
                print(u"警告: 预设菜单不存在，返回默认")
                return u"默认"
                
            current_preset = cmds.optionMenu(self.preset_option_menu, query=True, value=True)
            print(u"当前选中的预设: " + str(current_preset))
            return current_preset
            
        except Exception as e:
            print(u"获取当前选中预设时发生错误: " + str(e))
            return u"默认"
    
    def are_all_sliders_default(self):
        """检查所有滑条是否都为默认值1.0"""
        try:
            for param_key, param_info in self.parameters.items():
                if abs(param_info["value"] - 1.0) > 0.001:  # 考虑浮点数精度问题
                    return False
            return True
        except Exception as e:
            print(u"检查滑条默认值时发生错误: " + str(e))
            return False
    
    def show_preset_save_dialog(self, expression_string, parameter_values):
        """显示预设保存对话框"""
        try:
            # 检查当前滑条值是否都为默认值1.0，避免重复创建默认预设
            if self.are_all_sliders_default():
                result = cmds.confirmDialog(
                    title=u"提示", 
                    message=u"当前所有参数都是默认值(1.0)，建议直接使用'默认'预设。\n确定要创建新预设吗？", 
                    button=[u"继续创建", u"取消"],
                    defaultButton=u"取消",
                    cancelButton=u"取消",
                    dismissString=u"取消"
                )
                if result == u"取消":
                    return
            
            dialog_name = u"presetSaveDialog"
            if cmds.window(dialog_name, exists=True):
                cmds.deleteUI(dialog_name)
                
            # 获取当前主界面选中的预设
            current_selected_preset = u"默认"
            try:
                if self.preset_option_menu and cmds.optionMenu(self.preset_option_menu, exists=True):
                    selected_value = cmds.optionMenu(self.preset_option_menu, query=True, value=True)
                    # 在处理包含中文的预设名称时，确保正确处理编码
                    try:
                        current_selected_preset = selected_value.decode(u'utf-8')
                    except:
                        current_selected_preset = selected_value
                    print(u"获取当前选中的预设: " + current_selected_preset)
                else:
                    print(u"警告: 主界面预设菜单不存在，使用默认选项")
            except Exception as e:
                # 在Maya Python2环境中正确处理包含非ASCII字符的异常
                try:
                    error_msg = unicode(str(e), u'utf-8')
                except:
                    try:
                        error_msg = str(e).decode(u'utf-8')
                    except:
                        error_msg = repr(e)
                print(u"获取当前选中预设失败: %s" % error_msg + u"，使用默认选项")
                
            # 创建对话框
            cmds.window(dialog_name, title=u"保存表达式预设", width=400, height=150, sizeable=False)
            cmds.columnLayout(adjustableColumn=True, columnOffset=(u"both", 10))
            cmds.separator(height=15)
            cmds.text(label=u"请输入预设名称（新建或覆盖现有）：", align=u"left")
            
            # 预设名称输入框（智能默认值）
            preset_files = self.get_preset_files()
            default_text = u""
            if current_selected_preset != u"默认" and current_selected_preset in preset_files:
                default_text = current_selected_preset
                
            preset_input_field = cmds.textField(
                text=default_text,
                placeholderText=u"请输入预设名称"
            )
            
            cmds.separator(height=15)
            
            # 提示信息
            if default_text:
                # 在显示包含中文的预设名称时，确保正确处理编码
                try:
                    cmds.text(label=u"提示：当前将覆盖预设 '%s'" % default_text.decode(u'utf-8'), align=u"left", font=u"smallPlainLabelFont")
                except:
                    try:
                        cmds.text(label=u"提示：当前将覆盖预设 '%s'" % default_text, align=u"left", font=u"smallPlainLabelFont")
                    except:
                        cmds.text(label=u"提示：当前将覆盖预设", align=u"left", font=u"smallPlainLabelFont")
            else:
                cmds.text(label=u"提示：输入新名称将创建新预设，输入现有名称将覆盖", align=u"left", font=u"smallPlainLabelFont")
                
            cmds.separator(height=15)
            
            # 保存按钮
            cmds.button(label=u"保存", command=lambda x: self.execute_direct_preset_save(
                dialog_name, preset_input_field, expression_string, parameter_values))
            
            cmds.showWindow(dialog_name)
            
        except Exception as e:
            # 在Maya Python2环境中正确处理包含非ASCII字符的异常
            try:
                error_msg = unicode(str(e), u'utf-8')
            except:
                try:
                    error_msg = str(e).decode(u'utf-8')
                except:
                    error_msg = repr(e)
            print(u"显示预设保存对话框时发生错误: %s" % error_msg)
    
    def execute_direct_preset_save(self, dialog_name, input_field, expression_string, parameter_values):
        """执行直接预设保存"""
        try:
            # 获取输入的预设名称
            preset_name = cmds.textField(input_field, query=True, text=True).strip()
            
            if not preset_name:
                cmds.confirmDialog(title=u"错误", message=u"请输入预设名称！", button=[u"确定"])
                return
                
            # 检查预设名称是否为"默认"，避免创建重名预设
            if preset_name == u"默认":
                cmds.confirmDialog(title=u"错误", message=u"不能创建名为'默认'的预设，请使用其他名称！", button=[u"确定"])
                return
            
            # 检查当前滑条值是否都为默认值1.0，避免重复创建默认预设
            if self.are_all_sliders_default():
                result = cmds.confirmDialog(
                    title=u"提示", 
                    message=u"当前所有参数都是默认值(1.0)，建议直接使用'默认'预设。\n确定要创建新预设吗？", 
                    button=[u"继续创建", u"取消"],
                    defaultButton=u"取消",
                    cancelButton=u"取消",
                    dismissString=u"取消"
                )
                if result == u"取消":
                    return
                
            # 检查是否为现有预设（在保存前检查）
            current_presets = self.get_preset_files()
            is_overwrite = preset_name in current_presets
                
            # 直接保存预设，不需要任何确认
            if self.save_expression_preset(preset_name, expression_string, parameter_values):
                cmds.deleteUI(dialog_name)
                
                # 更新预设菜单并自动切换到刚保存的预设
                self.update_preset_menu()
                # 更新下拉菜单选中项
                try:
                    cmds.optionMenu(self.preset_option_menu, edit=True, value=preset_name)
                except:
                    pass
                    
                # 根据是否为新预设或覆盖现有预设显示不同的消息
                if is_overwrite:
                    # 在打印包含中文的预设名称时，确保正确处理编码
                    try:
                        print(u"表达式预设 " + preset_name.decode(u'utf-8') + u" 已覆盖成功并已自动选中")
                    except:
                        try:
                            print(u"表达式预设 " + preset_name + u" 已覆盖成功并已自动选中")
                        except:
                            print(u"表达式预设已覆盖成功并已自动选中")
                else:
                    # 在打印包含中文的预设名称时，确保正确处理编码
                    try:
                        print(u"表达式预设 " + preset_name.decode(u'utf-8') + u" 已新建成功并已自动选中")
                    except:
                        try:
                            print(u"表达式预设 " + preset_name + u" 已新建成功并已自动选中")
                        except:
                            print(u"表达式预设已新建成功并已自动选中")
            else:
                cmds.confirmDialog(title=u"错误", message=u"保存预设失败！", button=[u"确定"])
                
        except Exception as e:
            # 在Maya Python2环境中正确处理包含非ASCII字符的异常
            try:
                error_msg = unicode(str(e), u'utf-8')
            except:
                try:
                    error_msg = str(e).decode(u'utf-8')
                except:
                    error_msg = repr(e)
            print(u"执行直接预设保存时发生错误: %s" % error_msg)
            # 显示错误信息
            cmds.confirmDialog(
                title=u"保存失败",
                message=u"保存预设时发生错误: %s" % error_msg,
                button=[u"确定"],
                defaultButton=u"确定"
            )
    def get_script_path(self):
        """获取脚本文件自身的路径"""
        try:
            # 获取当前脚本文件的绝对路径
            script_path = os.path.dirname(os.path.abspath(__file__))
            return script_path
        except:
            # 如果无法获取脚本路径，则使用当前工作目录
            return os.getcwd()
    
    def get_current_mel_path(self):
        """获取当前MEL文件路径"""
        try:
            # 方法1：尝试从Maya工作空间目录获取
            workspace_dir = cmds.workspace(query=True, directory=True)
            if workspace_dir:
                return workspace_dir
            else:
                # 方法2：使用当前工作目录
                return os.getcwd()
        except:
            return os.getcwd()
    
    def update_expression_and_save_default(self):
        """更新表达式并保存默认预设"""
        try:
            print(u"更新表达式并保存默认预设")
            # 更新表达式（使用已重置的滑条值）
            self.update_expression()
            
            # 获取当前表达式内容
            expression_content = self.aa
            
            # 获取当前参数值用于保存（使用已重置的值）
            current_parameters = {}
            for key, value in self.parameters.items():
                current_parameters[key] = value["value"]
            
            # 检查是否所有滑条值都为默认值1.0
            all_default = True
            for param_key, param_info in self.parameters.items():
                if abs(param_info["value"] - 1.0) > 0.001:  # 考虑浮点数精度问题
                    all_default = False
                    break
            
            # 只有当滑条值不全为默认值1.0时才保存默认预设
            if not all_default:
                # 直接保存为"默认"预设
                if self.save_expression_preset("默认", expression_content, current_parameters):
                    print(u"表达式预设 '默认' 已保存成功！")
                    # 更新预设菜单
                    self.update_preset_menu()
                    # 选中"默认"预设
                    try:
                        cmds.optionMenu(self.preset_option_menu, edit=True, value=u"默认")
                    except:
                        pass
                else:
                    print(u"保存默认预设失败")
            else:
                print(u"所有滑条值都为默认值1.0，不创建新的默认预设")
            
            # 在Maya中创建或更新表达式
            self.cleanup_existing_expressions()
            if cmds.objExists("Mapping_Expr"):
                cmds.delete("Mapping_Expr")
                cmds.expression(name="Mapping_Expr", string=expression_content)
            print(u"已在Maya中创建/更新表达式: Mapping_Expr")
                
            print(u"默认预设更新完成")
        except Exception as e:
            print(u"更新表达式并保存默认预设时发生错误: %s" % str(e))
            traceback.print_exc()

# 创建全局变量存储控制器实例
mouth_corner_controller = None

def create_mouth_corner_controller():
    """创建嘴角控制器界面"""
    global mouth_corner_controller
    
    # 关闭已存在的控制器
    if mouth_corner_controller:
        mouth_corner_controller.close_window()
    
    # 创建新的控制器
    mouth_corner_controller = MouthCornerController()
    return mouth_corner_controller

def get_current_values():
    """获取当前参数值"""
    if mouth_corner_controller:
        return mouth_corner_controller.get_current_values()
    else:
        print(u"请先创建控制器界面")
        return None

def get_aa_variable():
    """获取表达式变量 Mapping_Expr 的值"""
    if mouth_corner_controller:
        return mouth_corner_controller.get_expression_variable()
    else:
        print(u"请先创建控制器界面")
        return None

# 主程序执行
if __name__ == "__main__":
    # 在Maya中直接执行
    create_mouth_corner_controller()
else:
    # 通过exec()执行时
    if MAYA_MODE:
        print(u"正在在Maya中创建嘴角控制器...")
        create_mouth_corner_controller()
        print(u"界面创建完成")
        print(u"使用方法:")
        print(u"  - 直接调节滑条参数")
        print(u"  - 调用 get_current_values() 获取参数值")
        print(u"  - 调用 get_aa_variable() 获取表达式变量")
        print(u"  - 调用 create_mouth_corner_controller() 重新创建界面")