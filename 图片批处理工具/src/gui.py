import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from image_processor import ImageProcessor

class ImageProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("图片批处理工具")
        self.root.geometry("600x700")
        self.root.resizable(True, True)
        
        self.processor = ImageProcessor()
        
        # 设置标题
        self.title_label = tk.Label(root, text="图片批处理工具", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        # 创建选项卡
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建各个功能页面
        self.create_resize_tab()
        self.create_convert_tab()
        self.create_watermark_tab()
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("准备就绪")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_resize_tab(self):
        """创建调整大小选项卡"""
        resize_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(resize_frame, text="调整大小")
        
        # 处理模式选择
        mode_frame = ttk.LabelFrame(resize_frame, text="处理模式", padding=10)
        mode_frame.grid(row=0, column=0, columnspan=3, sticky="we", pady=10)
        
        self.resize_mode_var = tk.StringVar(value="batch")
        tk.Radiobutton(mode_frame, text="批量处理目录", variable=self.resize_mode_var, value="batch", 
                      command=self.toggle_resize_mode).grid(row=0, column=0, padx=10)
        tk.Radiobutton(mode_frame, text="处理单张图片", variable=self.resize_mode_var, value="single", 
                      command=self.toggle_resize_mode).grid(row=0, column=1, padx=10)
        
        # 批量处理 - 输入目录
        self.resize_batch_frame = ttk.Frame(resize_frame)
        self.resize_batch_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=5)
        
        tk.Label(self.resize_batch_frame, text="输入目录:").grid(row=0, column=0, sticky="w", pady=5)
        self.resize_input_var = tk.StringVar()
        tk.Entry(self.resize_batch_frame, textvariable=self.resize_input_var, width=50).grid(row=0, column=1, pady=5)
        tk.Button(self.resize_batch_frame, text="浏览...", command=lambda: self.browse_directory(self.resize_input_var)).grid(row=0, column=2, padx=5, pady=5)
        
        # 单张处理 - 输入文件
        self.resize_single_frame = ttk.Frame(resize_frame)
        self.resize_single_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=5)
        self.resize_single_frame.grid_remove()  # 默认隐藏
        
        tk.Label(self.resize_single_frame, text="输入图片:").grid(row=0, column=0, sticky="w", pady=5)
        self.resize_input_file_var = tk.StringVar()
        tk.Entry(self.resize_single_frame, textvariable=self.resize_input_file_var, width=50).grid(row=0, column=1, pady=5)
        tk.Button(self.resize_single_frame, text="浏览...", command=self.browse_resize_input_file).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出目录
        tk.Label(resize_frame, text="输出目录:").grid(row=2, column=0, sticky="w", pady=5)
        self.resize_output_var = tk.StringVar()
        tk.Entry(resize_frame, textvariable=self.resize_output_var, width=50).grid(row=2, column=1, pady=5)
        tk.Button(resize_frame, text="浏览...", command=lambda: self.browse_directory(self.resize_output_var)).grid(row=2, column=2, padx=5, pady=5)
        
        # 尺寸设置
        size_frame = ttk.LabelFrame(resize_frame, text="尺寸设置", padding=10)
        size_frame.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)
        
        tk.Label(size_frame, text="宽度:").grid(row=0, column=0, sticky="w", pady=5)
        self.width_var = tk.IntVar(value=800)
        tk.Entry(size_frame, textvariable=self.width_var, width=10).grid(row=0, column=1, pady=5)
        
        tk.Label(size_frame, text="高度:").grid(row=1, column=0, sticky="w", pady=5)
        self.height_var = tk.IntVar(value=600)
        tk.Entry(size_frame, textvariable=self.height_var, width=10).grid(row=1, column=1, pady=5)
        
        # 执行按钮
        tk.Button(resize_frame, text="开始处理", command=self.resize_images, width=20).grid(row=4, column=0, columnspan=3, pady=20)
        
        # 结果显示
        result_frame = ttk.LabelFrame(resize_frame, text="处理结果", padding=10)
        result_frame.grid(row=5, column=0, columnspan=3, sticky="we", pady=10)
        
        self.resize_result_text = tk.Text(result_frame, height=10, width=60)
        self.resize_result_text.pack(fill="both", expand=True)
    
    def create_convert_tab(self):
        """创建格式转换选项卡"""
        convert_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(convert_frame, text="格式转换")
        
        # 处理模式选择
        mode_frame = ttk.LabelFrame(convert_frame, text="处理模式", padding=10)
        mode_frame.grid(row=0, column=0, columnspan=3, sticky="we", pady=10)
        
        self.convert_mode_var = tk.StringVar(value="batch")
        tk.Radiobutton(mode_frame, text="批量处理目录", variable=self.convert_mode_var, value="batch", 
                      command=self.toggle_convert_mode).grid(row=0, column=0, padx=10)
        tk.Radiobutton(mode_frame, text="处理单张图片", variable=self.convert_mode_var, value="single", 
                      command=self.toggle_convert_mode).grid(row=0, column=1, padx=10)
        
        # 批量处理 - 输入目录
        self.convert_batch_frame = ttk.Frame(convert_frame)
        self.convert_batch_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=5)
        
        tk.Label(self.convert_batch_frame, text="输入目录:").grid(row=0, column=0, sticky="w", pady=5)
        self.convert_input_var = tk.StringVar()
        tk.Entry(self.convert_batch_frame, textvariable=self.convert_input_var, width=50).grid(row=0, column=1, pady=5)
        tk.Button(self.convert_batch_frame, text="浏览...", command=lambda: self.browse_directory(self.convert_input_var)).grid(row=0, column=2, padx=5, pady=5)
        
        # 单张处理 - 输入文件
        self.convert_single_frame = ttk.Frame(convert_frame)
        self.convert_single_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=5)
        self.convert_single_frame.grid_remove()  # 默认隐藏
        
        tk.Label(self.convert_single_frame, text="输入图片:").grid(row=0, column=0, sticky="w", pady=5)
        self.convert_input_file_var = tk.StringVar()
        tk.Entry(self.convert_single_frame, textvariable=self.convert_input_file_var, width=50).grid(row=0, column=1, pady=5)
        tk.Button(self.convert_single_frame, text="浏览...", command=self.browse_convert_input_file).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出目录
        tk.Label(convert_frame, text="输出目录:").grid(row=2, column=0, sticky="w", pady=5)
        self.convert_output_var = tk.StringVar()
        tk.Entry(convert_frame, textvariable=self.convert_output_var, width=50).grid(row=2, column=1, pady=5)
        tk.Button(convert_frame, text="浏览...", command=lambda: self.browse_directory(self.convert_output_var)).grid(row=2, column=2, padx=5, pady=5)
        
        # 格式选择
        format_frame = ttk.LabelFrame(convert_frame, text="目标格式", padding=10)
        format_frame.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)
        
        self.format_var = tk.StringVar(value="jpeg")
        formats = [("JPEG", "jpeg"), ("PNG", "png"), ("BMP", "bmp"), ("GIF", "gif"), ("WEBP", "webp")]
        
        for i, (text, value) in enumerate(formats):
            tk.Radiobutton(format_frame, text=text, variable=self.format_var, value=value).grid(row=0, column=i, padx=10)
        
        # 执行按钮
        tk.Button(convert_frame, text="开始处理", command=self.convert_images, width=20).grid(row=4, column=0, columnspan=3, pady=20)
        
        # 结果显示
        result_frame = ttk.LabelFrame(convert_frame, text="处理结果", padding=10)
        result_frame.grid(row=5, column=0, columnspan=3, sticky="we", pady=10)
        
        self.convert_result_text = tk.Text(result_frame, height=10, width=60)
        self.convert_result_text.pack(fill="both", expand=True)
    
    def create_watermark_tab(self):
        """创建水印选项卡"""
        watermark_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(watermark_frame, text="添加水印")
        
        # 处理模式选择
        mode_frame = ttk.LabelFrame(watermark_frame, text="处理模式", padding=10)
        mode_frame.grid(row=0, column=0, columnspan=3, sticky="we", pady=10)
        
        self.watermark_mode_var = tk.StringVar(value="batch")
        tk.Radiobutton(mode_frame, text="批量处理目录", variable=self.watermark_mode_var, value="batch", 
                      command=self.toggle_watermark_mode).grid(row=0, column=0, padx=10)
        tk.Radiobutton(mode_frame, text="处理单张图片", variable=self.watermark_mode_var, value="single", 
                      command=self.toggle_watermark_mode).grid(row=0, column=1, padx=10)
        
        # 批量处理 - 输入目录
        self.watermark_batch_frame = ttk.Frame(watermark_frame)
        self.watermark_batch_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=5)
        
        tk.Label(self.watermark_batch_frame, text="输入目录:").grid(row=0, column=0, sticky="w", pady=5)
        self.watermark_input_var = tk.StringVar()
        tk.Entry(self.watermark_batch_frame, textvariable=self.watermark_input_var, width=50).grid(row=0, column=1, pady=5)
        tk.Button(self.watermark_batch_frame, text="浏览...", command=lambda: self.browse_directory(self.watermark_input_var)).grid(row=0, column=2, padx=5, pady=5)
        
        # 单张处理 - 输入文件
        self.watermark_single_frame = ttk.Frame(watermark_frame)
        self.watermark_single_frame.grid(row=1, column=0, columnspan=3, sticky="we", pady=5)
        self.watermark_single_frame.grid_remove()  # 默认隐藏
        
        tk.Label(self.watermark_single_frame, text="输入图片:").grid(row=0, column=0, sticky="w", pady=5)
        self.watermark_input_file_var = tk.StringVar()
        tk.Entry(self.watermark_single_frame, textvariable=self.watermark_input_file_var, width=50).grid(row=0, column=1, pady=5)
        tk.Button(self.watermark_single_frame, text="浏览...", command=self.browse_watermark_input_file).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出目录
        tk.Label(watermark_frame, text="输出目录:").grid(row=2, column=0, sticky="w", pady=5)
        self.watermark_output_var = tk.StringVar()
        tk.Entry(watermark_frame, textvariable=self.watermark_output_var, width=50).grid(row=2, column=1, pady=5)
        tk.Button(watermark_frame, text="浏览...", command=lambda: self.browse_directory(self.watermark_output_var)).grid(row=2, column=2, padx=5, pady=5)
        
        # 水印类型选择
        self.watermark_type_var = tk.StringVar(value="text")
        watermark_type_frame = ttk.LabelFrame(watermark_frame, text="水印类型", padding=10)
        watermark_type_frame.grid(row=3, column=0, columnspan=3, sticky="we", pady=10)
        
        tk.Radiobutton(watermark_type_frame, text="文本水印", variable=self.watermark_type_var, value="text", 
                      command=self.toggle_watermark_type).grid(row=0, column=0, padx=10)
        tk.Radiobutton(watermark_type_frame, text="图片水印", variable=self.watermark_type_var, value="image", 
                      command=self.toggle_watermark_type).grid(row=0, column=1, padx=10)
        
        # 水印设置
        watermark_settings_frame = ttk.LabelFrame(watermark_frame, text="水印设置", padding=10)
        watermark_settings_frame.grid(row=4, column=0, columnspan=3, sticky="we", pady=10)
        
        # 文本水印
        self.text_frame = ttk.Frame(watermark_settings_frame)
        self.text_frame.grid(row=0, column=0, sticky="w", pady=5)
        
        tk.Label(self.text_frame, text="水印文本:").grid(row=0, column=0, sticky="w", pady=5)
        self.watermark_text_var = tk.StringVar(value="水印")
        tk.Entry(self.text_frame, textvariable=self.watermark_text_var, width=30).grid(row=0, column=1, pady=5)
        
        # 图片水印
        self.image_frame = ttk.Frame(watermark_settings_frame)
        self.image_frame.grid(row=1, column=0, sticky="w", pady=5)
        self.image_frame.grid_remove()  # 默认隐藏
        
        tk.Label(self.image_frame, text="水印图片:").grid(row=0, column=0, sticky="w", pady=5)
        self.watermark_image_var = tk.StringVar()
        tk.Entry(self.image_frame, textvariable=self.watermark_image_var, width=50).grid(row=0, column=1, pady=5)
        tk.Button(self.image_frame, text="浏览...", command=self.browse_watermark_image).grid(row=0, column=2, padx=5, pady=5)
        
        # 位置和透明度
        tk.Label(watermark_settings_frame, text="位置:").grid(row=2, column=0, sticky="w", pady=5)
        self.position_var = tk.StringVar(value="center")
        position_frame = ttk.Frame(watermark_settings_frame)
        position_frame.grid(row=2, column=1, sticky="w", pady=5)
        
        tk.Radiobutton(position_frame, text="居中", variable=self.position_var, value="center").grid(row=0, column=0, padx=5)
        tk.Radiobutton(position_frame, text="自定义", variable=self.position_var, value="custom").grid(row=0, column=1, padx=5)
        
        self.position_custom_frame = ttk.Frame(watermark_settings_frame)
        self.position_custom_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)
        self.position_custom_frame.grid_remove()  # 默认隐藏
        
        tk.Label(self.position_custom_frame, text="X:").grid(row=0, column=0, padx=5)
        self.position_x_var = tk.IntVar(value=10)
        tk.Entry(self.position_custom_frame, textvariable=self.position_x_var, width=5).grid(row=0, column=1, padx=5)
        
        tk.Label(self.position_custom_frame, text="Y:").grid(row=0, column=2, padx=5)
        self.position_y_var = tk.IntVar(value=10)
        tk.Entry(self.position_custom_frame, textvariable=self.position_y_var, width=5).grid(row=0, column=3, padx=5)
        
        # 监听position_var变化
        self.position_var.trace_add("write", self.toggle_position_custom)
        
        tk.Label(watermark_settings_frame, text="透明度:").grid(row=4, column=0, sticky="w", pady=5)
        self.opacity_var = tk.DoubleVar(value=0.5)
        tk.Scale(watermark_settings_frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, 
                variable=self.opacity_var, length=200).grid(row=4, column=1, sticky="w", pady=5)
        
        # 执行按钮
        tk.Button(watermark_frame, text="开始处理", command=self.add_watermark, width=20).grid(row=5, column=0, columnspan=3, pady=20)
        
        # 结果显示
        result_frame = ttk.LabelFrame(watermark_frame, text="处理结果", padding=10)
        result_frame.grid(row=6, column=0, columnspan=3, sticky="we", pady=10)
        
        self.watermark_result_text = tk.Text(result_frame, height=10, width=60)
        self.watermark_result_text.pack(fill="both", expand=True)
    
    def toggle_resize_mode(self):
        """切换调整大小处理模式"""
        if self.resize_mode_var.get() == "batch":
            self.resize_batch_frame.grid()
            self.resize_single_frame.grid_remove()
        else:
            self.resize_batch_frame.grid_remove()
            self.resize_single_frame.grid()
    
    def toggle_convert_mode(self):
        """切换格式转换处理模式"""
        if self.convert_mode_var.get() == "batch":
            self.convert_batch_frame.grid()
            self.convert_single_frame.grid_remove()
        else:
            self.convert_batch_frame.grid_remove()
            self.convert_single_frame.grid()
    
    def toggle_watermark_mode(self):
        """切换水印处理模式"""
        if self.watermark_mode_var.get() == "batch":
            self.watermark_batch_frame.grid()
            self.watermark_single_frame.grid_remove()
        else:
            self.watermark_batch_frame.grid_remove()
            self.watermark_single_frame.grid()
    
    def toggle_watermark_type(self):
        """切换水印类型"""
        if self.watermark_type_var.get() == "text":
            self.text_frame.grid()
            self.image_frame.grid_remove()
        else:
            self.text_frame.grid_remove()
            self.image_frame.grid()
    
    def toggle_position_custom(self, *args):
        """切换位置选项"""
        if self.position_var.get() == "custom":
            self.position_custom_frame.grid()
        else:
            self.position_custom_frame.grid_remove()
    
    def browse_directory(self, var):
        """浏览并选择目录"""
        directory = filedialog.askdirectory()
        if directory:
            var.set(directory)
    
    def browse_resize_input_file(self):
        """浏览并选择调整大小的输入图片"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.resize_input_file_var.set(file_path)
    
    def browse_convert_input_file(self):
        """浏览并选择格式转换的输入图片"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.convert_input_file_var.set(file_path)
    
    def browse_watermark_input_file(self):
        """浏览并选择添加水印的输入图片"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.watermark_input_file_var.set(file_path)
    
    def browse_watermark_image(self):
        """浏览并选择水印图片"""
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.watermark_image_var.set(file_path)
    
    def process_single_image(self, operation, input_file, output_dir, **kwargs):
        """处理单张图片"""
        try:
            if not os.path.exists(input_file):
                messagebox.showerror("错误", "输入图片不存在")
                return False
            
            if not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir)
                except Exception as e:
                    messagebox.showerror("错误", f"无法创建输出目录: {e}")
                    return False
            
            # 获取文件名和扩展名
            filename = os.path.basename(input_file)
            file_base, file_ext = os.path.splitext(filename)
            
            # 根据操作类型确定输出文件名
            if operation == 'convert' and 'format_name' in kwargs:
                output_filename = file_base + '.' + kwargs['format_name'].lower()
            else:
                output_filename = filename
            
            output_path = os.path.join(output_dir, output_filename)
            
            # 根据操作类型执行相应的处理
            success = False
            if operation == 'resize' and 'size' in kwargs:
                success = self.processor.resize_image(input_file, output_path, kwargs['size'])
            elif operation == 'convert' and 'format_name' in kwargs:
                success = self.processor.convert_format(input_file, output_path, kwargs['format_name'])
            elif operation == 'watermark':
                success = self.processor.add_watermark(input_file, output_path, **kwargs)
            
            return success
        except Exception as e:
            messagebox.showerror("错误", f"处理图片时出错: {e}")
            return False
    
    def resize_images(self):
        """调整图片大小"""
        width = self.width_var.get()
        height = self.height_var.get()
        output_dir = self.resize_output_var.get()
        
        if not output_dir:
            messagebox.showerror("错误", "请选择输出目录")
            return
        
        mode = self.resize_mode_var.get()
        
        try:
            self.status_var.set("正在处理中...")
            self.root.update()
            
            if mode == "batch":
                input_dir = self.resize_input_var.get()
                if not input_dir:
                    messagebox.showerror("错误", "请选择输入目录")
                    return
                
                if not os.path.exists(input_dir):
                    messagebox.showerror("错误", "输入目录不存在")
                    return
                
                results = self.processor.batch_process(
                    input_dir, 
                    output_dir, 
                    'resize', 
                    size=(width, height)
                )
                
                self.display_results(self.resize_result_text, results)
            else:
                input_file = self.resize_input_file_var.get()
                if not input_file:
                    messagebox.showerror("错误", "请选择输入图片")
                    return
                
                success = self.process_single_image(
                    'resize',
                    input_file,
                    output_dir,
                    size=(width, height)
                )
                
                if success:
                    self.resize_result_text.delete(1.0, tk.END)
                    self.resize_result_text.insert(tk.END, "处理完成!\n\n")
                    self.resize_result_text.insert(tk.END, f"成功处理图片: {os.path.basename(input_file)}\n")
                    self.resize_result_text.insert(tk.END, f"\n处理完成的图片已保存到: {os.path.abspath(output_dir)}")
                else:
                    self.resize_result_text.delete(1.0, tk.END)
                    self.resize_result_text.insert(tk.END, "处理失败!\n")
            
            self.status_var.set("处理完成")
        except Exception as e:
            messagebox.showerror("错误", f"处理时出错: {e}")
            self.status_var.set("处理失败")
    
    def convert_images(self):
        """转换图片格式"""
        format_name = self.format_var.get()
        output_dir = self.convert_output_var.get()
        
        if not output_dir:
            messagebox.showerror("错误", "请选择输出目录")
            return
        
        mode = self.convert_mode_var.get()
        
        try:
            self.status_var.set("正在处理中...")
            self.root.update()
            
            if mode == "batch":
                input_dir = self.convert_input_var.get()
                if not input_dir:
                    messagebox.showerror("错误", "请选择输入目录")
                    return
                
                if not os.path.exists(input_dir):
                    messagebox.showerror("错误", "输入目录不存在")
                    return
                
                results = self.processor.batch_process(
                    input_dir, 
                    output_dir, 
                    'convert', 
                    format_name=format_name
                )
                
                self.display_results(self.convert_result_text, results)
            else:
                input_file = self.convert_input_file_var.get()
                if not input_file:
                    messagebox.showerror("错误", "请选择输入图片")
                    return
                
                success = self.process_single_image(
                    'convert',
                    input_file,
                    output_dir,
                    format_name=format_name
                )
                
                if success:
                    self.convert_result_text.delete(1.0, tk.END)
                    self.convert_result_text.insert(tk.END, "处理完成!\n\n")
                    self.convert_result_text.insert(tk.END, f"成功处理图片: {os.path.basename(input_file)}\n")
                    self.convert_result_text.insert(tk.END, f"\n处理完成的图片已保存到: {os.path.abspath(output_dir)}")
                else:
                    self.convert_result_text.delete(1.0, tk.END)
                    self.convert_result_text.insert(tk.END, "处理失败!\n")
            
            self.status_var.set("处理完成")
        except Exception as e:
            messagebox.showerror("错误", f"处理时出错: {e}")
            self.status_var.set("处理失败")
    
    def add_watermark(self):
        """添加水印"""
        output_dir = self.watermark_output_var.get()
        
        if not output_dir:
            messagebox.showerror("错误", "请选择输出目录")
            return
        
        # 获取水印设置
        watermark_text = None
        watermark_image = None
        
        if self.watermark_type_var.get() == "text":
            watermark_text = self.watermark_text_var.get()
            if not watermark_text:
                messagebox.showerror("错误", "请输入水印文本")
                return
        else:
            watermark_image = self.watermark_image_var.get()
            if not watermark_image:
                messagebox.showerror("错误", "请选择水印图片")
                return
            if not os.path.exists(watermark_image):
                messagebox.showerror("错误", "水印图片不存在")
                return
        
        # 获取位置
        position = "center"
        if self.position_var.get() == "custom":
            position = (self.position_x_var.get(), self.position_y_var.get())
        
        opacity = self.opacity_var.get()
        
        mode = self.watermark_mode_var.get()
        
        try:
            self.status_var.set("正在处理中...")
            self.root.update()
            
            if mode == "batch":
                input_dir = self.watermark_input_var.get()
                if not input_dir:
                    messagebox.showerror("错误", "请选择输入目录")
                    return
                
                if not os.path.exists(input_dir):
                    messagebox.showerror("错误", "输入目录不存在")
                    return
                
                results = self.processor.batch_process(
                    input_dir, 
                    output_dir, 
                    'watermark', 
                    watermark_text=watermark_text,
                    watermark_image=watermark_image,
                    position=position,
                    opacity=opacity
                )
                
                self.display_results(self.watermark_result_text, results)
            else:
                input_file = self.watermark_input_file_var.get()
                if not input_file:
                    messagebox.showerror("错误", "请选择输入图片")
                    return
                
                success = self.process_single_image(
                    'watermark',
                    input_file,
                    output_dir,
                    watermark_text=watermark_text,
                    watermark_image=watermark_image,
                    position=position,
                    opacity=opacity
                )
                
                if success:
                    self.watermark_result_text.delete(1.0, tk.END)
                    self.watermark_result_text.insert(tk.END, "处理完成!\n\n")
                    self.watermark_result_text.insert(tk.END, f"成功处理图片: {os.path.basename(input_file)}\n")
                    self.watermark_result_text.insert(tk.END, f"\n处理完成的图片已保存到: {os.path.abspath(output_dir)}")
                else:
                    self.watermark_result_text.delete(1.0, tk.END)
                    self.watermark_result_text.insert(tk.END, "处理失败!\n")
            
            self.status_var.set("处理完成")
        except Exception as e:
            messagebox.showerror("错误", f"处理时出错: {e}")
            self.status_var.set("处理失败")
    
    def validate_directories(self, input_dir, output_dir):
        """验证输入和输出目录"""
        if not input_dir:
            messagebox.showerror("错误", "请选择输入目录")
            return False
        
        if not output_dir:
            messagebox.showerror("错误", "请选择输出目录")
            return False
        
        if not os.path.exists(input_dir):
            messagebox.showerror("错误", "输入目录不存在")
            return False
        
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                messagebox.showerror("错误", f"无法创建输出目录: {e}")
                return False
        
        return True
    
    def display_results(self, text_widget, results):
        """显示处理结果"""
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, f"处理完成!\n\n")
        text_widget.insert(tk.END, f"成功: {results['success']} 张图片\n")
        text_widget.insert(tk.END, f"失败: {results['fail']} 张图片\n")
        text_widget.insert(tk.END, f"跳过: {results['skipped']} 个文件 (非支持的图片格式)\n")
        
        # 根据当前活动的选项卡获取正确的输出目录
        current_tab = self.notebook.select()
        tab_index = self.notebook.index(current_tab)
        
        output_path = ""
        if tab_index == 0:  # 调整大小选项卡
            output_path = self.resize_output_var.get()
        elif tab_index == 1:  # 格式转换选项卡
            output_path = self.convert_output_var.get()
        elif tab_index == 2:  # 添加水印选项卡
            output_path = self.watermark_output_var.get()
        
        if results['success'] > 0:
            text_widget.insert(tk.END, f"\n处理完成的图片已保存到: {os.path.abspath(output_path)}")

def main():
    root = tk.Tk()
    app = ImageProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 