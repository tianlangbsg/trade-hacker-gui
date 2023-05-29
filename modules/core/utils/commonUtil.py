import os


# 获取根路径
def get_root_path():
    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    # 获取当前文件的父目录
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    # 获取根目录
    root_path = os.path.abspath(os.path.dirname(father_path) + os.path.sep + ".")
    return root_path

# 获取工程主路径
def get_home_path():
    # 获取当前文件路径
    current_path = os.path.abspath(__file__)
    # 获取当前文件的父目录
    father_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
    # 获取根目录
    home_path = os.path.abspath(os.path.dirname(father_path) + os.path.sep + ".")
    home_path = os.path.abspath(os.path.dirname(home_path) + os.path.sep + ".")
    home_path = os.path.abspath(os.path.dirname(home_path) + os.path.sep + ".")
    return home_path
