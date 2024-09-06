from setuptools import setup, find_packages

# 读取README文件作为项目的long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='htctools',  # 项目名称
    version='0.2.0',  # 项目版本
    author='Tianchang Huang',  # 作者姓名
    author_email='tianchang.huang@monash.edu',  # 作者邮箱
    description='A self-use DFT toolbox',  # 项目简介
    long_description=long_description,  # 项目详细描述
    long_description_content_type="text/markdown",  # 描述文件类型
    url='https://github.com/yourusername/htctools',  # 项目主页
    packages=find_packages(),  # 自动查找所有包含`__init__.py`的包
    classifiers=[  # 项目分类信息
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # 选择合适的开源许可证
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python版本要求
    install_requires=[  # 项目依赖包列表
        'numpy>=1.19.2'
    ],
    entry_points={
        'console_scripts': [
            'htctools=htctools.main:main',
        ],
    },
    include_package_data=True,  # 包含数据文件
    package_data={  # 打包时包含的其他文件
        '': ['rcs\\potpaw_PBE_52\\**\\*'],
        '': ['*.md'],  # 包含所有.md文件
    },
)
