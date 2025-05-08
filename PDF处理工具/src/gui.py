import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdf_utils import merge_pdfs, split_pdf, extract_text

class PDFProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF文档处理工具")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # 创建选项卡
        self.tab_control = ttk.Notebook(root)
        
        # 合并PDF选项卡
        self.merge_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.merge_tab, text="合并PDF")
        self.setup_merge_tab()
        
        # 分割PDF选项卡
        self.split_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.split_tab, text="分割PDF")
        self.setup_split_tab()
        
        # 提取文本选项卡
        self.extract_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.extract_tab, text="提取文本")
        self.setup_extract_tab()
        
        self.tab_control.pack(expand=1, fill="both")
    
    def setup_merge_tab(self):
        # 文件列表框架
        list_frame = ttk.LabelFrame(self.merge_tab, text="选择要合并的PDF文件")
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # 文件列表
        self.files_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED, height=10)
        self.files_listbox.pack(padx=10, pady=10, fill="both", expand=True)
        
        # 按钮框架
        btn_frame = ttk.Frame(self.merge_tab)
        btn_frame.pack(padx=10, pady=10, fill="x")
        
        # 添加文件按钮
        add_btn = ttk.Button(btn_frame, text="添加文件", command=self.add_files)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # 删除选中文件按钮
        remove_btn = ttk.Button(btn_frame, text="删除选中", command=self.remove_files)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # 清空列表按钮
        clear_btn = ttk.Button(btn_frame, text="清空列表", command=self.clear_files)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 合并按钮
        merge_btn = ttk.Button(self.merge_tab, text="合并PDF", command=self.merge_pdfs_action)
        merge_btn.pack(pady=10)
        
        # 存储文件路径
        self.merge_files = []
    
    def setup_split_tab(self):
        # 文件选择框架
        file_frame = ttk.LabelFrame(self.split_tab, text="选择要分割的PDF文件")
        file_frame.pack(padx=10, pady=10, fill="x")
        
        # 文件路径输入
        self.split_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.split_file_var, width=50)
        file_entry.pack(side=tk.LEFT, padx=5, pady=10, fill="x", expand=True)
        
        # 浏览按钮
        browse_btn = ttk.Button(file_frame, text="浏览", command=self.browse_split_file)
        browse_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # 选项框架
        options_frame = ttk.LabelFrame(self.split_tab, text="分割选项")
        options_frame.pack(padx=10, pady=10, fill="x")
        
        # 页数选择
        ttk.Label(options_frame, text="每个文件的页数:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.pages_var = tk.IntVar(value=1)
        pages_spinbox = ttk.Spinbox(options_frame, from_=1, to=100, textvariable=self.pages_var, width=5)
        pages_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        # 输出目录选择
        ttk.Label(options_frame, text="输出目录:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.output_dir_var = tk.StringVar(value="output")
        output_dir_entry = ttk.Entry(options_frame, textvariable=self.output_dir_var, width=40)
        output_dir_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        
        browse_dir_btn = ttk.Button(options_frame, text="选择", command=self.browse_output_dir)
        browse_dir_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # 分割按钮
        split_btn = ttk.Button(self.split_tab, text="分割PDF", command=self.split_pdf_action)
        split_btn.pack(pady=10)
    
    def setup_extract_tab(self):
        # 文件选择框架
        file_frame = ttk.LabelFrame(self.extract_tab, text="选择要提取文本的PDF文件")
        file_frame.pack(padx=10, pady=10, fill="x")
        
        # 文件路径输入
        self.extract_file_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.extract_file_var, width=50)
        file_entry.pack(side=tk.LEFT, padx=5, pady=10, fill="x", expand=True)
        
        # 浏览按钮
        browse_btn = ttk.Button(file_frame, text="浏览", command=self.browse_extract_file)
        browse_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # 输出选项框架
        output_frame = ttk.LabelFrame(self.extract_tab, text="输出选项")
        output_frame.pack(padx=10, pady=10, fill="x")
        
        # 保存到文件选项
        self.save_to_file_var = tk.BooleanVar(value=True)
        save_check = ttk.Checkbutton(output_frame, text="保存到文件", variable=self.save_to_file_var, 
                                     command=self.toggle_output_file)
        save_check.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        # 输出文件路径
        ttk.Label(output_frame, text="输出文件:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.output_file_var = tk.StringVar()
        self.output_file_entry = ttk.Entry(output_frame, textvariable=self.output_file_var, width=40)
        self.output_file_entry.grid(row=1, column=1, padx=5, pady=5, sticky="we")
        
        self.browse_output_btn = ttk.Button(output_frame, text="选择", command=self.browse_output_file)
        self.browse_output_btn.grid(row=1, column=2, padx=5, pady=5)
        
        # 文本预览区域
        preview_frame = ttk.LabelFrame(self.extract_tab, text="文本预览")
        preview_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.text_preview = tk.Text(preview_frame, wrap=tk.WORD, height=10)
        self.text_preview.pack(padx=5, pady=5, fill="both", expand=True)
        
        # 提取按钮
        extract_btn = ttk.Button(self.extract_tab, text="提取文本", command=self.extract_text_action)
        extract_btn.pack(pady=10)
    
    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF文件", "*.pdf")])
        if files:
            for file in files:
                if file not in self.merge_files:
                    self.merge_files.append(file)
                    self.files_listbox.insert(tk.END, os.path.basename(file))
    
    def remove_files(self):
        selected = self.files_listbox.curselection()
        if selected:
            # 从后向前删除，避免索引变化
            for index in sorted(selected, reverse=True):
                del self.merge_files[index]
                self.files_listbox.delete(index)
    
    def clear_files(self):
        self.merge_files.clear()
        self.files_listbox.delete(0, tk.END)
    
    def browse_split_file(self):
        file = filedialog.askopenfilename(filetypes=[("PDF文件", "*.pdf")])
        if file:
            self.split_file_var.set(file)
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
    
    def browse_extract_file(self):
        file = filedialog.askopenfilename(filetypes=[("PDF文件", "*.pdf")])
        if file:
            self.extract_file_var.set(file)
            # 设置默认输出文件名
            base_name = os.path.splitext(os.path.basename(file))[0]
            self.output_file_var.set(f"{base_name}.txt")
    
    def browse_output_file(self):
        file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("文本文件", "*.txt")])
        if file:
            self.output_file_var.set(file)
    
    def toggle_output_file(self):
        if self.save_to_file_var.get():
            self.output_file_entry.config(state="normal")
            self.browse_output_btn.config(state="normal")
        else:
            self.output_file_entry.config(state="disabled")
            self.browse_output_btn.config(state="disabled")
    
    def merge_pdfs_action(self):
        if not self.merge_files:
            messagebox.showwarning("警告", "请先添加PDF文件")
            return
        
        output_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF文件", "*.pdf")])
        if not output_file:
            return
        
        if merge_pdfs(self.merge_files, output_file):
            messagebox.showinfo("成功", f"PDF文件已成功合并为:\n{output_file}")
        else:
            messagebox.showerror("错误", "合并PDF文件失败")
    
    def split_pdf_action(self):
        input_file = self.split_file_var.get()
        if not input_file:
            messagebox.showwarning("警告", "请选择要分割的PDF文件")
            return
        
        output_dir = self.output_dir_var.get()
        pages_per_file = self.pages_var.get()
        
        try:
            output_files = split_pdf(input_file, output_dir, pages_per_file)
            if output_files:
                messagebox.showinfo("成功", f"PDF文件已成功分割为{len(output_files)}个文件\n保存在: {output_dir}")
            else:
                messagebox.showerror("错误", "分割PDF文件失败")
        except Exception as e:
            messagebox.showerror("错误", f"分割PDF时出错: {str(e)}")
    
    def extract_text_action(self):
        input_file = self.extract_file_var.get()
        if not input_file:
            messagebox.showwarning("警告", "请选择要提取文本的PDF文件")
            return
        
        output_file = None
        if self.save_to_file_var.get():
            output_file = self.output_file_var.get()
            if not output_file:
                messagebox.showwarning("警告", "请指定输出文件")
                return
        
        try:
            text = extract_text(input_file, output_file)
            
            # 显示预览
            self.text_preview.delete(1.0, tk.END)
            self.text_preview.insert(tk.END, text[:5000] + "..." if len(text) > 5000 else text)
            
            if output_file:
                messagebox.showinfo("成功", f"文本已成功提取并保存到:\n{output_file}")
        except Exception as e:
            messagebox.showerror("错误", f"提取文本时出错: {str(e)}")

def main():
    root = tk.Tk()
    app = PDFProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 