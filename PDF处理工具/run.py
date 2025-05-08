import os
import sys

# 将src目录添加到模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.append(src_dir)

# 导入GUI模块
from gui import main

if __name__ == "__main__":
    main() 