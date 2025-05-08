#!/usr/bin/env python3
import os
import sys

def main():
    """启动程序的主函数"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(script_dir, "src"))
    
    print("启动图片批处理工具...")
    
    # 询问用户使用GUI还是命令行
    print("请选择启动模式:")
    print("1. 图形界面模式")
    print("2. 命令行模式")
    
    choice = input("请输入选择 (默认为1): ").strip()
    
    if choice == "2":
        # 导入命令行模块并启动
        from src.main import main as cli_main
        cli_main()
    else:
        # 默认启动图形界面
        try:
            from src.gui import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"启动图形界面失败: {e}")
            print("可能缺少必要的依赖，请确保已安装tkinter。")
            print("尝试使用命令行模式...")
            
            try:
                from src.main import main as cli_main
                cli_main()
            except ImportError as e2:
                print(f"启动命令行模式也失败: {e2}")
                print("请确保已安装所有必要的依赖。")
                return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 