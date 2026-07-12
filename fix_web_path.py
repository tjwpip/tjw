import os

# 修复 web/app.py 中的静态文件路径
web_app_path = os.path.join(os.path.dirname(__file__), "web/app.py")

with open(web_app_path, "r", encoding="utf-8") as f:
    content = f.read()

# 添加 os 导入
if "import os" not in content:
    content = "import os\n" + content

# 修复静态文件路径
content = content.replace(
    'app.mount("/static", StaticFiles(directory="web/static"), name="static")',
    'app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")'
)

# 修复 root 函数中的文件路径
content = content.replace(
    'return FileResponse("web/static/index.html")',
    'return FileResponse(os.path.join(os.path.dirname(__file__), "static/index.html"))'
)

with open(web_app_path, "w", encoding="utf-8") as f:
    f.write(content)

print("修复 web/app.py 完成")

# 修复 tjw/cli.py 添加版本参数
cli_path = os.path.join(os.path.dirname(__file__), "tjw/cli.py")

with open(cli_path, "r", encoding="utf-8") as f:
    content = f.read()

# 添加版本常量
if "__version__" not in content:
    version_line = '__version__ = "1.0.14"\n\n'
    content = version_line + content

# 添加版本参数到 argparse
old_parser = '''parser = argparse.ArgumentParser(
        description='TJW 鍛戒护琛屽伐鍏?,
        epilog='''
new_parser = '''parser = argparse.ArgumentParser(
        description='TJW 鍛戒护琛屽伐鍏?,
        epilog='''

# 添加 --version 参数
if "--version" not in content:
    content = content.replace(
        'parser = argparse.ArgumentParser(',
        'parser = argparse.ArgumentParser(\n        prog="tjw",\n        formatter_class=argparse.ArgumentDefaultsHelpFormatter,'
    )
    content = content.replace(
        'args = parser.parse_args()',
        'parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")\n\n    args = parser.parse_args()'
    )

with open(cli_path, "w", encoding="utf-8") as f:
    f.write(content)

print("修复 tjw/cli.py 完成")