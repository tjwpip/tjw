@echo off
chcp 65001 >nul 2>&1
:: 启用延迟变量扩展（解决!变量!解析问题）
setlocal enabledelayedexpansion
:: Windows一键打包上传脚本（带工具自动检测与安装）
title Python包打包上传工具

echo ========================================
echo 正在检测打包/上传工具是否已安装...
echo ========================================
echo.

:: 定义需要检测的包列表
set "required_packages=setuptools wheel twine"
set "missing_packages="

:: 循环检测每个包是否安装
for %%p in (%required_packages%) do (
    echo 检测 %%p...
    python -c "import %%p" >nul 2>&1
    if errorlevel 1 (
        echo   %%p 未安装
        set "missing_packages=!missing_packages! %%p"
    ) else (
        echo   %%p 已安装
    )
)

echo.
:: 如果有缺失的包，自动安装
if not "!missing_packages!"=="" (
    echo ========================================
    echo 开始安装缺失的工具：!missing_packages!
    echo ========================================
    :: 移除开头的空格，避免pip识别错误
    set "missing_packages=!missing_packages:~1!"
    :: 使用python -m pip 安装，避免pip命令找不到
    python -m pip install !missing_packages!
    if errorlevel 1 (
        echo 错误：工具安装失败，请检查网络或pip配置
        pause
        exit /b 1
    )
    echo.
    echo 工具安装完成！
    echo.
) else (
    echo 所有必要工具均已安装，无需额外操作
    echo.
)

echo ========================================
echo 清理旧打包文件...
echo ========================================
rmdir /s /q dist build tjw.egg-info 2>nul
echo 旧文件清理完成
echo.

echo ========================================
echo 开始打包...
echo ========================================
python setup.py sdist bdist_wheel
if errorlevel 1 (
    echo 错误：打包失败，请检查setup.py文件
    pause
    exit /b 1
)
echo 打包完成
echo.

echo ========================================
echo 开始上传...
echo ========================================
:: 改用python -m twine执行，不依赖PATH环境变量
python -m twine upload dist/*
if errorlevel 1 (
    echo 错误：上传失败，请检查twine配置（如pypi账号）或网络
    echo 常见原因：1. 未配置pypi账号 2. 网络问题 3. 包名已存在
    pause
    exit /b 1
)

echo.
echo ========================================
echo 上传成功！开始清理打包生成的临时文件...
echo ========================================
:: 清理打包生成的临时文件
rmdir /s /q dist build tjw.egg-info 2>nul
if errorlevel 0 (
    echo 临时文件（dist/build/egg-info）已成功清理
) else (
    echo 提示：部分临时文件清理失败（可能文件被占用）
)
echo.

echo ========================================
echo 全部操作完成！
echo ========================================
pause
:: 关闭延迟变量扩展
endlocal