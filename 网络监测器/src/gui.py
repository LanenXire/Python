import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import queue

from network_monitor import NetworkMonitor
from utils import format_datetime, format_time_duration, play_alert_sound, show_desktop_notification

class NetworkMonitorGUI:
    def __init__(self, root, log_dir):
        self.root = root
        self.log_dir = log_dir
        self.root.title("网络监测器")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 配置变量
        self.test_ip_var = tk.StringVar(value="8.8.8.8")
        self.test_interval_var = tk.IntVar(value=5)
        self.alert_sound_var = tk.BooleanVar(value=True)
        self.desktop_notification_var = tk.BooleanVar(value=True)
        
        # 创建网络监测器实例
        self.monitor = NetworkMonitor(
            log_dir=log_dir, 
            test_ip=self.test_ip_var.get(),
            test_interval=self.test_interval_var.get()
        )
        
        # 设置监测器回调函数
        self.monitor.set_connection_status_changed_callback(self.on_connection_status_changed)
        
        # 创建UI
        self.create_ui()
        
        # 状态历史记录
        self.status_history = []
        self.status_queue = queue.Queue()
        
        # 启动更新UI的计时器
        self.update_status_ui()
        self.root.after(1000, self.process_status_queue)
    
    def create_ui(self):
        """创建用户界面"""
        # 创建菜单栏
        self.create_menu()
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 上部分 - 状态和控制
        control_frame = ttk.LabelFrame(main_frame, text="网络状态监控", padding=10)
        control_frame.pack(fill=tk.X, pady=5)
        
        # 状态指示器
        status_frame = ttk.Frame(control_frame)
        status_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(status_frame, text="当前状态:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.status_indicator = ttk.Label(status_frame, text="检测中...", font=("Arial", 10, "bold"))
        self.status_indicator.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(status_frame, text="测试IP:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(status_frame, textvariable=self.test_ip_var, width=15).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(status_frame, text="检测间隔(秒):").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(status_frame, from_=1, to=60, textvariable=self.test_interval_var, width=5).grid(row=0, column=5, padx=5, pady=5, sticky=tk.W)
        
        # 按钮区域
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.start_button = ttk.Button(button_frame, text="开始监控", command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(button_frame, text="停止监控", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="应用设置", command=self.apply_settings).pack(side=tk.LEFT, padx=5)
        
        # 通知设置
        notification_frame = ttk.Frame(control_frame)
        notification_frame.pack(fill=tk.X, pady=5)
        
        ttk.Checkbutton(notification_frame, text="断网时播放声音提醒", variable=self.alert_sound_var).pack(side=tk.LEFT, padx=5)
        ttk.Checkbutton(notification_frame, text="显示桌面通知", variable=self.desktop_notification_var).pack(side=tk.LEFT, padx=5)
        
        # 中部 - 历史记录和图表
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 历史记录选项卡
        history_frame = ttk.Frame(notebook, padding=10)
        notebook.add(history_frame, text="连接历史")
        
        # 创建历史记录列表
        columns = ("时间", "事件", "持续时间")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings")
        
        # 设置列标题
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=100)
        
        # 设置列宽度
        self.history_tree.column("时间", width=150)
        self.history_tree.column("事件", width=100)
        self.history_tree.column("持续时间", width=150)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscroll=scrollbar.set)
        
        # 放置组件
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 图表选项卡
        chart_frame = ttk.Frame(notebook, padding=10)
        notebook.add(chart_frame, text="连接图表")
        
        # 创建图表
        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 底部 - 状态栏
        status_bar_frame = ttk.Frame(main_frame)
        status_bar_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=5)
        
        self.status_bar = ttk.Label(status_bar_frame, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X)
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="开始监控", command=self.start_monitoring)
        file_menu.add_command(label="停止监控", command=self.stop_monitoring)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.on_close)
        menubar.add_cascade(label="文件", menu=file_menu)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="清除历史记录", command=self.clear_history)
        tools_menu.add_command(label="立即测试连接", command=self.test_connection_now)
        menubar.add_cascade(label="工具", menu=tools_menu)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="帮助", command=self.show_help)
        help_menu.add_command(label="关于", command=self.show_about)
        menubar.add_cascade(label="帮助", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def start_monitoring(self):
        """开始监控网络连接"""
        self.monitor.start_monitoring()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_bar.config(text="正在监控网络连接...")
    
    def stop_monitoring(self):
        """停止监控网络连接"""
        self.monitor.stop_monitoring()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_bar.config(text="监控已停止")
    
    def apply_settings(self):
        """应用设置"""
        try:
            test_ip = self.test_ip_var.get()
            test_interval = self.test_interval_var.get()
            
            # 更新监测器设置
            self.monitor.set_test_ip(test_ip)
            self.monitor.set_test_interval(test_interval)
            
            messagebox.showinfo("设置", "设置已应用")
        except Exception as e:
            messagebox.showerror("错误", f"应用设置时出错: {e}")
    
    def on_connection_status_changed(self, is_connected):
        """
        网络连接状态变化回调函数
        
        参数:
            is_connected (bool): 新的连接状态
        """
        # 使用队列，避免在不同线程中更新UI
        self.status_queue.put(is_connected)
    
    def process_status_queue(self):
        """处理状态变更队列"""
        try:
            # 尝试获取队列中的状态更新，不阻塞
            while True:
                is_connected = self.status_queue.get_nowait()
                self.update_connection_status(is_connected)
                self.status_queue.task_done()
        except queue.Empty:
            pass
        
        # 继续定期检查队列
        self.root.after(1000, self.process_status_queue)
    
    def update_connection_status(self, is_connected):
        """
        更新连接状态UI
        
        参数:
            is_connected (bool): 新的连接状态
        """
        current_time = datetime.now()
        
        # 更新状态指示器
        if is_connected:
            self.status_indicator.config(text="已连接", foreground="green")
            status_text = "网络连接已恢复"
            
            # 添加到历史记录
            if self.status_history and not self.status_history[-1]["is_connected"]:
                # 计算断网持续时间
                last_status = self.status_history[-1]
                duration = current_time - last_status["time"]
                duration_str = format_time_duration(duration.total_seconds())
                
                # 更新上一条断网记录的持续时间
                item_id = self.history_tree.get_children()[-1]
                self.history_tree.item(item_id, values=(
                    format_datetime(last_status["time"]),
                    "网络断开",
                    duration_str
                ))
        else:
            self.status_indicator.config(text="未连接", foreground="red")
            status_text = "网络连接已断开"
            
            # 播放提醒声音
            if self.alert_sound_var.get():
                thread = threading.Thread(target=play_alert_sound)
                thread.daemon = True
                thread.start()
            
            # 显示桌面通知
            if self.desktop_notification_var.get():
                show_desktop_notification("网络监测器", "网络连接已断开!")
        
        # 添加到状态历史
        status_entry = {
            "time": current_time,
            "is_connected": is_connected,
            "duration": None  # 将在下一次状态变化时更新
        }
        self.status_history.append(status_entry)
        
        # 更新历史记录视图
        self.history_tree.insert("", "end", values=(
            format_datetime(current_time),
            "网络连接" if is_connected else "网络断开",
            "计算中..."
        ))
        
        # 更新图表
        self.update_chart()
        
        # 更新状态栏
        self.status_bar.config(text=f"{status_text} - {format_datetime(current_time)}")
    
    def update_status_ui(self):
        """更新状态UI"""
        is_connected = self.monitor.get_connection_status()
        
        if is_connected:
            self.status_indicator.config(text="已连接", foreground="green")
        else:
            self.status_indicator.config(text="未连接", foreground="red")
    
    def update_chart(self):
        """更新连接状态图表"""
        if not self.status_history:
            return
        
        # 清除图表
        self.ax.clear()
        
        # 准备数据
        times = []
        statuses = []
        
        # 确保至少有24小时的数据范围
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        
        # 如果有历史数据，确保从第一条记录开始
        if self.status_history:
            start_time = min(start_time, self.status_history[0]["time"])
        
        # 添加起始点
        times.append(start_time)
        # 如果第一条记录是连接状态，使用相反的状态作为起始点
        if self.status_history and self.status_history[0]["is_connected"]:
            statuses.append(0)  # 断开
        else:
            statuses.append(1)  # 连接
        
        # 添加所有状态变化点
        for entry in self.status_history:
            times.append(entry["time"])
            statuses.append(1 if entry["is_connected"] else 0)
        
        # 添加结束点（当前时间）
        times.append(end_time)
        if self.status_history:
            # 使用最后一条记录的状态
            statuses.append(1 if self.status_history[-1]["is_connected"] else 0)
        else:
            statuses.append(1)  # 默认为连接状态
        
        # 绘制图表
        self.ax.step(times, statuses, where='post')
        
        # 设置Y轴范围和标签
        self.ax.set_ylim(-0.1, 1.1)
        self.ax.set_yticks([0, 1])
        self.ax.set_yticklabels(["断开", "连接"])
        
        # 设置X轴为时间轴
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        self.ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        
        # 添加网格线
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # 设置标题和标签
        self.ax.set_title("网络连接状态历史")
        self.ax.set_xlabel("时间")
        self.ax.set_ylabel("连接状态")
        
        # 调整布局
        self.fig.tight_layout()
        
        # 刷新画布
        self.canvas.draw()
    
    def clear_history(self):
        """清除历史记录"""
        if messagebox.askyesno("清除历史", "确定要清除所有历史记录吗？"):
            self.status_history = []
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            self.update_chart()
    
    def test_connection_now(self):
        """立即测试连接"""
        is_connected = self.monitor.check_connection()
        
        if is_connected:
            messagebox.showinfo("连接测试", "网络连接正常")
        else:
            messagebox.showwarning("连接测试", "网络连接已断开")
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
网络监测器使用帮助:

1. 开始/停止监控: 点击相应按钮开始或停止监控网络连接。
2. 测试IP: 设置用于测试连接的IP地址。默认为8.8.8.8 (谷歌DNS服务器)。
3. 检测间隔: 设置检测网络连接的时间间隔，单位为秒。
4. 提醒设置: 选择是否在网络断开时播放声音提醒和显示桌面通知。
5. 连接历史: 显示网络连接状态变化的历史记录。
6. 连接图表: 图形化显示网络连接状态变化。

注意: 请确保应用设置后再开始监控，以便应用新的设置。
        """
        messagebox.showinfo("帮助", help_text)
    
    def show_about(self):
        """显示关于信息"""
        about_text = """
网络监测器 v1.0

一个简单的工具，用于监控网络连接状态并在断网时发出提醒。

功能:
- 实时监控网络连接
- 断网时发出声音和桌面提醒
- 记录连接状态变化历史
- 图形化显示连接状态

使用Python开发
        """
        messagebox.showinfo("关于", about_text)
    
    def on_close(self):
        """关闭应用"""
        if self.monitor.is_monitoring:
            if messagebox.askyesno("退出", "监控正在运行，确定要退出吗？"):
                self.monitor.stop_monitoring()
                self.root.destroy()
        else:
            self.root.destroy()

def main():
    # 创建日志目录
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(script_dir, "logs")
    
    # 创建主窗口
    root = tk.Tk()
    app = NetworkMonitorGUI(root, log_dir)
    
    # 设置关闭事件处理
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    
    # 启动应用
    root.mainloop()

if __name__ == "__main__":
    main() 