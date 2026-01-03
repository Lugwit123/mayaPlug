@echo off

chcp 65001
:: 设置 pyside2-uic.exe 的路径
set "UIC=D:\TD_Depot\plug_in\Python\Python37\Scripts\pyside2-uic.exe"

:: 切换到批处理文件所在的目录
cd /d "%~dp0"

:: 转换当前目录下的所有 .ui 文件为 .py 文件
for %%f in (*.ui) do (
    
    echo Converting "%%f" to "%%~nf.py"...
    "%UIC%" "%%f" -o "%%~nf.py"
    )


echo Conversion complete.
pause

