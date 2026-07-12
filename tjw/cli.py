__version__ = "1.0.14"

import argparse
import subprocess
import sys

from tjw.core import tjw_class, hello

tjw = tjw_class()


def main():
    parser = argparse.ArgumentParser(
        prog="tjw",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='TJW 命令行工具',
        epilog='示例: tjw helloworld --name 张三 或 tjw web --port 8000'
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # helloworld 命令
    helloworld_parser = subparsers.add_parser('helloworld', help='输出问候信息')
    helloworld_parser.add_argument('--name', default='TJW', help='问候对象的名称，默认为 TJW')

    # hello 命令
    hello_parser = subparsers.add_parser('hello', help='执行数值加1操作')
    hello_parser.add_argument('--number', type=int, default=0, help='要加1的数值，默认为0')

    # web 命令 - 启动Web服务
    web_parser = subparsers.add_parser('web', help='启动 TJW Web 服务')
    web_parser.add_argument('--port', type=int, default=8000, help='服务端口，默认为 8000')
    web_parser.add_argument('--host', default='0.0.0.0', help='绑定地址，默认为 0.0.0.0')
    web_parser.add_argument('--reload', action='store_true', help='启用自动重载（开发模式）')

    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    if args.command == 'helloworld':
        print(tjw.helloworld(name=args.name))
    elif args.command == 'hello':
        result = hello(number=args.number)
        print(f"结果: {result}")
    elif args.command == 'web':
        start_server(args.port, args.host, args.reload)
    else:
        parser.print_help()


def print_banner(port):
    banner = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                        🚀 TJW FastAPI Service                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐  ║
║  │  🏠 首页          │  http://localhost:{port}/                         │  ║
║  │  📖 API文档       │  http://localhost:{port}/docs                    │  ║
║  │  📘 Redoc文档     │  http://localhost:{port}/redoc                   │  ║
║  │  🏥 健康检查      │  http://localhost:{port}/health                  │  ║
║  │  🔌 API基础路径    │  http://localhost:{port}/api/sfz                │  ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
║  ┌──────────────────────── 快捷访问 ─────────────────────────┐              ║
║  │  🆔 身份证工具    │  /id/1002 或 /?id=1002              │              ║
║  │  📊 仪表盘        │  /id/1001 或 /?id=1001              │              ║
║  │  🔧 实用工具      │  /id/1003 或 /?id=1003              │              ║
║  │  ⚙️ 系统设置      │  /id/1004 或 /?id=1004              │              ║
║  └────────────────────────────────────────────────────────────────────────┘  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def start_server(port, host, reload):
    try:
        import uvicorn
        from web.app import app
    except ImportError:
        print("⚠️  检测到依赖未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "pydantic"], check=True)
        print("✅ 依赖安装完成")
        import uvicorn

    print("\n" + "="*70)
    print(f"          📦 正在启动 TJW FastAPI 服务 (端口: {port})...")
    print("="*70)

    print_banner(port)
    print("💡 提示: 按 Ctrl+C 停止服务")
    print("="*70 + "\n")

    try:
        uvicorn.run(
            "web.app:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n✅ 服务已停止")
    except Exception as e:
        print(f"\n❌ 服务启动失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()