#!/bin/bash
# Mac/Linux一键打包上传脚本
echo "清理旧打包文件..."
rm -rf dist/ build/ tjw.egg-info/

echo "开始打包..."
python setup.py sdist bdist_wheel

echo "开始上传..."
twine upload dist/*

echo "完成！"