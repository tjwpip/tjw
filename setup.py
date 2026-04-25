import os
from setuptools import setup, find_packages

# ===================== 核心：版本号会被 publish.sh 自动更新 =====================
# 重要
PIP包名 = "tjw"
版本号 = "1.0.11"
一句话描述 = "一个简单的命令行工具，用于输出问候信息和数值加1"

# 一般重要
作者 = "tjw"
作者邮箱 = "saogegood@163.com"
关键词 = ["tjw", "tjw类库"]
网站 = "https://github.com/tjwpip/tjw"


# ==============================================================================

def 获得详细描述():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content if content else f"{一句话描述}"
    return f"{一句话描述}"


# ===================== ✅ 关键：动态读取 requirements.txt =====================
def 获取依赖列表():
    """自动读取同目录下 requirements.txt 并返回依赖列表"""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")

    if not os.path.exists(requirements_path):
        return []

    with open(requirements_path, "r", encoding="utf-8") as f:
        依赖列表 = [
            line.strip()
            for line in f.readlines()
            if line.strip() and not line.startswith("#")
        ]
    return 依赖列表


# ==============================================================================

setup(
    name=PIP包名,
    version=版本号,
    description=一句话描述,
    author=作者,
    author_email=作者邮箱,
    long_description=获得详细描述(),
    long_description_content_type="text/markdown",
    license="MIT",

    url=网站,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",

    # ===================== ✅ 这里变成动态读取 =====================
    install_requires=获取依赖列表(),

    keywords=关键词,
    include_package_data=True,
    zip_safe=False,

    # 添加命令行入口点
    entry_points={
        'console_scripts': [
            'tjw=tjw.cli:main',
        ],
    },
)
