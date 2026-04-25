# TJW

一个最简单的PYPI 发布包的样例，PIP安装后，即可使用，提供基础的命令行功能和数值操作。

## 功能特性

- **命令行工具**：提供 `helloworld` 和 `hello` 两个命令
- **数值操作**：支持简单的数值加1操作
- **易于扩展**：模块化设计，便于添加新功能

## 安装

使用 pip 安装：

```bash
pip install --upgrade tjw
```

查看安装信息：

```bash
pip show tjw
```

## 使用方法
### 终端PYTHON直接使用

```bash
python -c "from tjw import hello; print(hello(number=43))"
# 输出：43
```

### 作为库在项目中使用

```python
from tjw.core import tjw_class, hello

# 使用 tjw_class
tjw = tjw_class()
print(tjw.helloworld(name="张三"))  # 输出：helloworld,[张三]!

# 使用 hello 函数
result = hello(number=42)
print(f"结果: {result}")  # 输出：结果: 43
```

### 命令行使用

查看帮助信息：

```bash
tjw --help
```

输出问候信息：

```bash
tjw helloworld --name 张三
# 输出：helloworld,[张三]!
```

执行数值加1操作：

```bash
tjw hello --number 42
# 输出：结果: 43
```

## 项目结构

```
tjwpip/
├── tjw/
│   ├── __init__.py
│   ├── cli.py        # 命令行接口
│   └── core.py       # 核心功能
├── setup.py          # 包配置
├── publish.py        # 发布脚本
├── README.md         # 项目文档
└── requirements.txt  # 依赖配置
```

## 发布指南

1. **注册 PyPI 账号**：
    - 访问 https://pypi.org/account/register/ 注册账号

2. **创建 API Token**：
    - 登录 PyPI 后，访问 https://pypi.org/manage/account/
    - 点击 "Add API token" 创建新的 API token
    - 复制生成的 token

3. **配置环境变量**：
    - 在项目根目录创建 `.env` 文件
    - 添加以下内容：
      ```
      PYPI_API_TOKEN=你的API token
      ```

4. **运行发布脚本**：
   ```bash
   python publish.py
   ```

   发布脚本会自动：
    - 检查 PyPI 上的最新版本
    - 自动版本号加1
    - 打包项目
    - 上传到 PyPI
    - 清理临时文件

## 版本信息

- 当前版本：1.0.4
- 发布地址：https://pypi.org/project/tjw/

## 许可证

MIT License