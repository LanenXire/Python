#!/usr/bin/env python3
import os
import sys
import argparse

def main():
    """主函数，处理命令行参数并启动应用"""
    # 添加src目录到Python路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(script_dir, "src"))
    
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='网络监测器 - 监控网络连接状态')
    parser.add_argument('--console', action='store_true', help='在控制台模式下运行，无图形界面')
    parser.add_argument('--ip', default='8.8.8.8', help='测试连接的IP地址 (默认: 8.8.8.8)')
    parser.add_argument('--interval', type=int, default=5, help='检测间隔时间(秒) (默认: 5)')
    
    args = parser.parse_args()
    
    # 创建日志目录
    log_dir = os.path.join(script_dir, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    if args.console:
        # 控制台模式
        run_console_mode(log_dir, args.ip, args.interval)
    else:
        # 图形界面模式
        run_gui_mode(log_dir)

def run_console_mode(log_dir, test_ip, test_interval):
    """运行控制台模式"""
    import time
    from src.network_monitor import NetworkMonitor
    from src.utils import play_alert_sound
    
    print("网络监测器 - 控制台模式")
    print(f"测试IP: {test_ip}, 检测间隔: {test_interval}秒")
    print("按Ctrl+C退出")
    
    # 创建网络监测器
    monitor = NetworkMonitor(
        log_dir=log_dir,
        test_ip=test_ip,
        test_interval=test_interval
    )
    
    # 设置状态变化回调
    def on_status_change(is_connected):
        if is_connected:
            print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 网络已连接")
        else:
            print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] 网络已断开")
            play_alert_sound()
    
    monitor.set_connection_status_changed_callback(on_status_change)
    
    try:
        # 开始监控
        monitor.start_monitoring()
        
        # 输出初始状态
        status = "已连接" if monitor.get_connection_status() else "未连接"
        print(f"初始状态: {status}")
        
        # 保持程序运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在停止监控...")
        monitor.stop_monitoring()
        print("已退出")

def run_gui_mode(log_dir):
    """运行图形界面模式"""
    try:
        import tkinter as tk
        from src.gui import NetworkMonitorGUI
        
        # 创建主窗口
        root = tk.Tk()
        app = NetworkMonitorGUI(root, log_dir)
        
        # 设置关闭事件处理
        root.protocol("WM_DELETE_WINDOW", app.on_close)
        
        # 启动应用
        root.mainloop()
    except ImportError as e:
        print(f"启动图形界面失败: {e}")
        print("请确保已安装所有必要的依赖库")
        print("尝试以控制台模式运行: python run.py --console")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 