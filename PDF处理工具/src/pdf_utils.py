import os
from PyPDF2 import PdfReader, PdfWriter, PdfMerger

def merge_pdfs(input_paths, output_path):
    """
    合并多个PDF文件
    :param input_paths: PDF文件路径列表
    :param output_path: 输出的PDF文件路径
    :return: 成功返回True，失败返回False
    """
    try:
        merger = PdfMerger()
        
        for path in input_paths:
            merger.append(path)
            
        merger.write(output_path)
        merger.close()
        return True
    except Exception as e:
        print(f"合并PDF时出错: {str(e)}")
        return False

def split_pdf(input_path, output_dir, pages_per_file=1):
    """
    分割PDF文件
    :param input_path: 输入的PDF文件路径
    :param output_dir: 输出目录
    :param pages_per_file: 每个文件的页数，默认为1
    :return: 成功返回分割后的文件路径列表，失败返回空列表
    """
    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        output_files = []
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        base_filename = os.path.splitext(os.path.basename(input_path))[0]
        
        for i in range(0, total_pages, pages_per_file):
            writer = PdfWriter()
            
            # 添加页面到新的PDF
            for page_num in range(i, min(i + pages_per_file, total_pages)):
                writer.add_page(reader.pages[page_num])
            
            # 保存分割后的PDF
            output_file = os.path.join(output_dir, f"{base_filename}_页{i+1}-{min(i+pages_per_file, total_pages)}.pdf")
            with open(output_file, "wb") as f:
                writer.write(f)
            
            output_files.append(output_file)
        
        return output_files
    except Exception as e:
        print(f"分割PDF时出错: {str(e)}")
        return []

def extract_text(input_path, output_path=None):
    """
    从PDF中提取文本
    :param input_path: 输入的PDF文件路径
    :param output_path: 输出的文本文件路径，如果为None则仅返回文本内容
    :return: 提取的文本内容
    """
    try:
        reader = PdfReader(input_path)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
        
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
        
        return text
    except Exception as e:
        print(f"提取文本时出错: {str(e)}")
        return "" 