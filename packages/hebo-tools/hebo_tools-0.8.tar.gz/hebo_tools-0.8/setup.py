from setuptools import setup, find_packages

import re


def update_version(filepath):
    # 读取当前文件内容
    with open(filepath, 'r') as file:
        content = file.read()

    # 使用正则表达式查找当前版本号
    match = re.search(r"__version__ = '(\d+\.\d+)'", content)
    if match:
        current_version = float(match.group(1))
        new_version = round(current_version + 0.1, 1)  # 保持一位小数

        # 替换旧的版本号为新的版本号
        new_content = re.sub(r"__version__ = '\d+\.\d+'", f"__version__ = '{new_version}'", content)

        # 将更新后的内容写回文件
        with open(filepath, 'w') as file:
            file.write(new_content)

        print(f"Version updated to {new_version}")
        return new_version
    else:
        print("Version number not found in the file.")


# 替换为你的文件路径
version = update_version('hebo_tools/version.py')

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
