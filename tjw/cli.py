import argparse

from tjw.core import tjw_class, hello

tjw = tjw_class()


def main():
    parser = argparse.ArgumentParser(
        description='TJW 命令行工具',
        epilog='示例: tjw helloworld --name 张三 或 tjw hello --number 42'
    )
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # helloworld 命令
    helloworld_parser = subparsers.add_parser('helloworld', help='输出问候信息')
    helloworld_parser.add_argument('--name', default='TJW', help='问候对象的名称，默认为 TJW')

    # hello 命令
    hello_parser = subparsers.add_parser('hello', help='执行数值加1操作')
    hello_parser.add_argument('--number', type=int, default=0, help='要加1的数值，默认为0')

    args = parser.parse_args()

    if args.command == 'helloworld':
        print(tjw.helloworld(name=args.name))
    elif args.command == 'hello':
        result = hello(number=args.number)
        print(f"结果: {result}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()