# -*- coding: utf-8 -*-
"""
PyPI 全自动发布脚本（全平台通用 Windows/Mac/Linux）
功能：自动版本+1、打包、上传、 清理
"""
import os
import re
import sys
import shutil
import subprocess
import requests
from dotenv import load_dotenv

# ===================== 加载环境变量 =====================
load_dotenv()


# ===================== 从 tjw/__init__.py 读取版本号 =====================
def get_tjw_version() -> str:
    """从 tjw/__init__.py 读取版本号"""
    init_path = os.path.join(os.path.dirname(__file__), "tjw", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    return match.group(1) if match else "1.0.0"


def update_tjw_version(new_version: str):
    """更新 tjw/__init__.py 中的版本号"""
    init_path = os.path.join(os.path.dirname(__file__), "tjw", "__init__.py")
    with open(init_path, "r", encoding="utf-8") as f:
        content = f.read()
    new_content = re.sub(
        r'__version__\s*=\s*["\']([^"\']+)["\']',
        f'__version__ = "{new_version}"',
        content,
        count=1
    )
    with open(init_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"📝 tjw/__init__.py 版本已更新为 {new_version}")


PACKAGE_NAME = "tjw"  # 直接指定包名
LOCAL_VERSION = get_tjw_version()  # 从 tjw/__init__.py 读取版本号

# ===================== 配置 =====================
PYPI_TOKEN = os.getenv("PYPI_API_TOKEN")
DEBUG_MODE = "--debug" in sys.argv or "-d" in sys.argv

# ===================== 校验 =====================
if not PYPI_TOKEN:
    print("❌ 错误：PYPI_API_TOKEN 未配置，请检查 .env")
    sys.exit(1)

if not os.path.exists("setup.py"):
    print("❌ 错误：未找到 setup.py")
    sys.exit(1)

print(f"📦 动态读取包名：{PACKAGE_NAME}")
print(f"🏷️  本地当前版本：{LOCAL_VERSION}")

# ===================== 获取 PyPI 最新版本 =====================
print("🔍 获取 PyPI 最新版本...")
LATEST_VERSION = "1.0.0"

try:
    url = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        releases = list(data["releases"].keys())
        releases.sort(key=lambda x: tuple(map(int, x.split("."))))
        LATEST_VERSION = releases[-1] if releases else "1.0.0"
except:
    LATEST_VERSION = LOCAL_VERSION

print(f"📌 PyPI 最新版本：{LATEST_VERSION}")

# ===================== 自动版本 +1 =====================
major, minor, patch = LATEST_VERSION.split(".")
new_patch = int(patch) + 1
NEW_VERSION = f"{major}.{minor}.{new_patch}"
print(f"✅ 即将发布新版本：{NEW_VERSION}")

# ===================== 更新 tjw/__init__.py（在打包前更新，确保 setup.py 能读取到新版本） =====================
update_tjw_version(NEW_VERSION)

# ===================== 安装依赖（自动修复） =====================
print("📦 安装/升级打包依赖...")
try:
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "twine", "wheel", "build"], check=True,
                   capture_output=not DEBUG_MODE)
    print("✅ 依赖安装完成")
except Exception as e:
    print("❌ 依赖安装/升级失败")
    sys.exit(1)


# ===================== 清理 =====================
def clean():
    for folder in ["dist", "build", f"{PACKAGE_NAME}.egg-info"]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    print("🗑️ 清理完成")


print("🔴 清理历史文件...")
clean()

# ===================== 打包 =====================
print(f"🟡 开始打包 {PACKAGE_NAME} {NEW_VERSION}...")
cmd = [sys.executable, "-m", "build"]
try:
    result = subprocess.run(cmd, capture_output=not DEBUG_MODE, check=True, text=True)
    if DEBUG_MODE and result.stdout:
        print(result.stdout)
except subprocess.CalledProcessError as e:
    print("❌ 打包失败")
    if e.stderr:
        print(f"错误信息: {e.stderr}")
    clean()
    sys.exit(1)

# 校验打包结果
if not os.path.exists("dist") or len(os.listdir("dist")) == 0:
    print("❌ 打包失败：dist 目录为空")
    clean()
    sys.exit(1)

print(f"✅ 打包成功！")

# ===================== 上传（修复 Windows 找不到 twine 问题） =====================
print("🟢 上传到 PyPI...")
upload_cmd = [
    sys.executable, "-m", "twine", "upload",
    "--username", "__token__",
    "--password", PYPI_TOKEN,
    "dist/*"
]
if DEBUG_MODE:
    upload_cmd.append("--verbose")

subprocess.run(upload_cmd, check=True)

# ===================== 收尾 =====================
if not DEBUG_MODE:
    clean()

print(f"\n🎉 发布成功！")
print(f"📦 新版本：{NEW_VERSION}")
print(f"🔧 安装：pip install {PACKAGE_NAME}")
print(f"🔧 升级：pip install --upgrade {PACKAGE_NAME}")
print(f"🔍 查看: pip show {PACKAGE_NAME}")
print(f"🔧 使用: python -c \"from tjw import tjw; tjw.hello('hello,world!')\"")
print(f"🔧 查看文档: https://pypi.org/project/{PACKAGE_NAME}/")