import os
import time
import socket
import platform
import subprocess
import threading
import datetime
import logging
from logging.handlers import RotatingFileHandler

class NetworkMonitor:
    """网络监测器类，用于监控网络连接状态"""
    
    def __init__(self, log_dir, test_ip="8.8.8.8", test_interval=5, ping_timeout=2):
        """
        初始化网络监测器
        
        参数:
            log_dir (str): 日志保存目录
            test_ip (str): 用于测试连接的IP地址，默认为谷歌DNS服务器
            test_interval (int): 检测间隔时间（秒）
            ping_timeout (int): ping超时时间（秒）
        """
        self.test_ip = test_ip
        self.test_interval = test_interval
        self.ping_timeout = ping_timeout
        self.is_connected = False
        self.is_monitoring = False
        self.monitoring_thread = None
        self.connection_status_changed_callback = None
        self.last_status_change_time = None
        
        # 设置日志
        self.setup_logging(log_dir)
        
        # 初始检测当前网络状态
        self.is_connected = self.check_connection()
        self.logger.info(f"初始网络状态: {'已连接' if self.is_connected else '未连接'}")
    
    def setup_logging(self, log_dir):
        """设置日志记录"""
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        log_file = os.path.join(log_dir, 'network_monitor.log')
        
        self.logger = logging.getLogger('NetworkMonitor')
        self.logger.setLevel(logging.INFO)
        
        # 创建一个轮转文件处理器，最大2MB，保留5个备份
        file_handler = RotatingFileHandler(log_file, maxBytes=2*1024*1024, backupCount=5)
        file_handler.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 创建格式器并添加到处理器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def check_connection(self):
        """
        检查网络连接状态
        
        返回:
            bool: 如果网络连接正常返回True，否则返回False
        """
        # 方法1: 使用socket尝试连接
        try:
            # 设置超时时间以避免长时间等待
            socket.setdefaulttimeout(self.ping_timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.test_ip, 53))
            return True
        except socket.error:
            pass
        
        # 方法2: 尝试Ping命令
        try:
            system = platform.system().lower()
            
            if system == 'windows':
                # Windows系统使用-n参数指定发送次数
                ping_cmd = ['ping', '-n', '1', '-w', str(int(self.ping_timeout * 1000)), self.test_ip]
            else:
                # Linux和MacOS使用-c参数指定发送次数
                ping_cmd = ['ping', '-c', '1', '-W', str(int(self.ping_timeout)), self.test_ip]
                
            return subprocess.call(ping_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
        except:
            return False
    
    def start_monitoring(self):
        """开始监控网络连接"""
        if self.is_monitoring:
            self.logger.warning("监控已经在运行")
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop)
        self.monitoring_thread.daemon = True
        self.monitoring_thread.start()
        self.logger.info("开始监控网络连接")
    
    def stop_monitoring(self):
        """停止监控网络连接"""
        if not self.is_monitoring:
            self.logger.warning("监控未在运行")
            return
        
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=self.test_interval+1)
        self.logger.info("停止监控网络连接")
    
    def _monitoring_loop(self):
        """监控循环，定期检查网络连接状态"""
        while self.is_monitoring:
            current_status = self.check_connection()
            
            # 如果状态发生变化
            if current_status != self.is_connected:
                self._handle_status_change(current_status)
            
            # 等待指定的间隔时间
            time.sleep(self.test_interval)
    
    def _handle_status_change(self, new_status):
        """
        处理网络状态变化
        
        参数:
            new_status (bool): 新的网络状态
        """
        self.is_connected = new_status
        current_time = datetime.datetime.now()
        
        # 记录断开或连接时间
        if self.last_status_change_time:
            duration = current_time - self.last_status_change_time
            if new_status:
                self.logger.info(f"网络已恢复连接，断网持续时间: {duration}")
            else:
                self.logger.warning(f"网络已断开连接，持续连接时间: {duration}")
        else:
            if new_status:
                self.logger.info("网络已连接")
            else:
                self.logger.warning("网络已断开")
        
        self.last_status_change_time = current_time
        
        # 调用回调函数（如果已设置）
        if self.connection_status_changed_callback:
            self.connection_status_changed_callback(new_status)
    
    def set_connection_status_changed_callback(self, callback):
        """
        设置网络状态变化的回调函数
        
        参数:
            callback (callable): 当网络状态变化时调用的函数，接受一个布尔参数表示新的连接状态
        """
        self.connection_status_changed_callback = callback
    
    def get_connection_status(self):
        """
        获取当前网络连接状态
        
        返回:
            bool: 如果网络连接正常返回True，否则返回False
        """
        return self.is_connected
    
    def set_test_interval(self, interval):
        """
        设置检测间隔时间
        
        参数:
            interval (int): 新的检测间隔时间（秒）
        """
        self.test_interval = interval
        self.logger.info(f"检测间隔已更新为 {interval} 秒")
    
    def set_test_ip(self, ip):
        """
        设置测试IP地址
        
        参数:
            ip (str): 新的测试IP地址
        """
        self.test_ip = ip
        self.logger.info(f"测试IP已更新为 {ip}")
    
    def get_network_stats(self):
        """
        获取网络状态统计信息
        
        返回:
            dict: 包含网络状态统计信息的字典
        """
        # TODO: 实现网络状态统计，如平均延迟、丢包率等
        return {
            "is_connected": self.is_connected,
            "test_ip": self.test_ip,
            "test_interval": self.test_interval,
            "last_status_change": self.last_status_change_time
        } 