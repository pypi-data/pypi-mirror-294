import os

# 获取terminal当前路径
def get_terminal_directory():
    return os.getcwd()

# 获取程序（主目录）的路径
def get_program_directory():
    # 首先获取当前脚本的绝对路径
    current_directory = os.path.abspath(__file__)
    # 然后获取这个路径的目录部分，即当前脚本所在目录
    program_directory = os.path.dirname(current_directory)
    # 再使用 dirname 获取上一级目录，即包含模块的目录
    parent_directory = os.path.dirname(program_directory)
    # 再使用 dirname 获取上一级目录，即项目的根目录
    root_directory = os.path.dirname(parent_directory)
    return root_directory
