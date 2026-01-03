# coding:utf-8
import sys


def readHierarchyNameDict(readRowList=[1,2]):
    # 使用 ExcelFile ，通过将 xls 或者 xlsx 路径传入，生成一个实例
    xlsx =u'A:/TD/Template/Model/Outline/资产分组命名规范索引表.xls'
    # 导入 xlrd 库
    import xlrd
    # 打开刚才我们写入的 test_w.xls 文件
    wb = xlrd.open_workbook(xlsx)
    sh1 = wb.sheet_by_index(0)
    col1 = sh1.col_values(readRowList[0])[2:] # 获取第一行内容
    col2 = sh1.col_values(readRowList[1])[2:] # 获取第二列内容
    # 打印获取的行列值
    #print( u"第一行的值为:", col2)
    #print( u"第二列的值为:", col2)
    return col1,col2

if __name__=='__main__':
    pass
    #print (readHierarchyNameDict())