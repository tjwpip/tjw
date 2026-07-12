from tjw.core.shengfenzheng.sfz import CShengFenZheng

PACKAGE_NAME = "tjw"
LOCAL_VERSION = "1.0.0"


class tjw_class:
    def helloworld(self, name: str = "TJW"):
        return f"helloworld,[{name}]!"


def hello(number: int = 0):
    return number + 1


if __name__ == '__main__':
    result = hello()
    print(f"结果：{result}")
