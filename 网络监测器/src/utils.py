import os
import sys
import platform
import time
import datetime

def get_system_info():
    """获取系统信息"""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor()
    }

def format_time_duration(seconds):
    """
    将秒数格式化为人类可读的时间持续格式
    
    参数:
        seconds (float): 秒数
        
    返回:
        str: 格式化后的时间字符串
    """
    if seconds < 60:
        return f"{seconds:.1f}秒"
    
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return f"{int(minutes)}分{int(seconds)}秒"
    
    hours, minutes = divmod(minutes, 60)
    if hours < 24:
        return f"{int(hours)}小时{int(minutes)}分{int(seconds)}秒"
    
    days, hours = divmod(hours, 24)
    return f"{int(days)}天{int(hours)}小时{int(minutes)}分{int(seconds)}秒"

def format_datetime(dt=None, format_str="%Y-%m-%d %H:%M:%S"):
    """
    格式化日期时间
    
    参数:
        dt (datetime, optional): 要格式化的datetime对象，默认为当前时间
        format_str (str, optional): 格式化字符串
        
    返回:
        str: 格式化后的日期时间字符串
    """
    if dt is None:
        dt = datetime.datetime.now()
    return dt.strftime(format_str)

def play_alert_sound():
    """
    播放提醒声音
    
    在Windows、Linux和MacOS上使用不同的方式播放声音
    """
    system = platform.system().lower()
    
    if system == 'windows':
        # Windows
        import winsound
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    elif system == 'darwin':
        # MacOS
        os.system('afplay /System/Library/Sounds/Sosumi.aiff')
    else:
        # Linux
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load("/usr/share/sounds/freedesktop/stereo/dialog-warning.oga")
            pygame.mixer.music.play()
            # 等待音频播放完毕
            time.sleep(1)
        except (ImportError, FileNotFoundError):
            try:
                os.system('aplay -q /usr/share/sounds/freedesktop/stereo/dialog-warning.oga')
            except:
                # 如果以上方法都失败，尝试使用print作为最后的备选
                print('\a')  # 发出系统提示音

def get_resource_path(relative_path):
    """
    获取资源文件的绝对路径
    
    参数:
        relative_path (str): 相对于resources目录的路径
        
    返回:
        str: 资源文件的绝对路径
    """
    # 如果是通过PyInstaller打包的应用
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.executable)))
    else:
        # 获取当前脚本所在目录
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 拼接资源目录
    resources_path = os.path.join(base_path, 'resources')
    
    # 最后拼接相对路径
    return os.path.join(resources_path, relative_path)

def show_desktop_notification(title, message):
    """
    显示桌面通知
    
    参数:
        title (str): 通知标题
        message (str): 通知内容
    """
    system = platform.system().lower()
    
    try:
        if system == 'windows':
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=5, threaded=True)
        elif system == 'darwin':  # MacOS
            os.system(f"""osascript -e 'display notification "{message}" with title "{title}"'""")
        else:  # Linux
            os.system(f"""notify-send "{title}" "{message}" """)
    except Exception as e:
        print(f"无法显示桌面通知: {e}")
        # 回退到简单的终端消息
        print(f"\n{title}: {message}\n") 