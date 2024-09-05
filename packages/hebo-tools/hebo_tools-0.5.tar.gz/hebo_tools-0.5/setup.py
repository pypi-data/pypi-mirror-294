from setuptools import setup, find_packages

import re


def get_version(filepath):
    # 读取当前文件内容
    with open(filepath, 'r') as file:
        content = file.read()

    # 使用正则表达式查找当前版本号
    match = re.search(r"__version__ = '(\d+\.\d+)'", content)
    if match:
        current_version = float(match.group(1))
        print(f"Version updated to {current_version}")
        return current_version
    else:
        print("Version number not found in the file.")


# 替换为你的文件路径
version = get_version('hebo_tools/version.py')

print("1111111111", version)
setup(
    name='hebo_tools',               # 包名称
    version=version,                   # 版本号
    packages=find_packages(),        # 自动查找包
    description='用于离床判断',
    author='hy',
    author_email='yue.huang@slaaplekker.cn',
    url='https://github.com/yourname/my_package',  # 代码仓库URL
)
