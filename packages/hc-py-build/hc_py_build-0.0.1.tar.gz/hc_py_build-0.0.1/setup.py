from setuptools import setup, find_packages


def read_version():
    with open('VERSION', 'r') as version_file:
        return version_file.read().strip()


setup(
    name='hc_py_build',  # 包名
    version=read_version(),  # 版本号
    packages=find_packages(),  # 自动查找所有的包和子包
    install_requires=[  # 依赖的其他包
        'cython'  # 示例依赖
    ],
    author='chouhong',  # 作者名
    author_email='ithongchou@163.com',  # 作者邮箱
    description='把python源码编译成pyd（Windows平台）或so（Linux平台）',  # 包描述
    long_description=open('README.md', encoding='utf-8').read(),  # 包的详细描述，通常从 README 文件中读取
    long_description_content_type='text/markdown',  # README 文件的格式
    # url='https://github.com/yourusername/yourrepository', # 项目的主页 URL
    classifiers=[  # 包的分类
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
