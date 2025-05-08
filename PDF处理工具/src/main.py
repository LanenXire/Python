import os
import argparse
from pdf_utils import merge_pdfs, split_pdf, extract_text

def main():
    parser = argparse.ArgumentParser(description='PDF文档处理工具 - 合并、分割和提取文本')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 合并PDF命令
    merge_parser = subparsers.add_parser('merge', help='合并多个PDF文件')
    merge_parser.add_argument('inputs', nargs='+', help='输入PDF文件路径列表')
    merge_parser.add_argument('-o', '--output', required=True, help='输出PDF文件路径')
    
    # 分割PDF命令
    split_parser = subparsers.add_parser('split', help='分割PDF文件')
    split_parser.add_argument('input', help='输入PDF文件路径')
    split_parser.add_argument('-o', '--output-dir', default='output', help='输出目录')
    split_parser.add_argument('-p', '--pages-per-file', type=int, default=1, help='每个文件的页数')
    
    # 提取文本命令
    text_parser = subparsers.add_parser('extract', help='从PDF中提取文本')
    text_parser.add_argument('input', help='输入PDF文件路径')
    text_parser.add_argument('-o', '--output', help='输出文本文件路径')
    
    args = parser.parse_args()
    
    if args.command == 'merge':
        print(f"正在合并 {len(args.inputs)} 个PDF文件...")
        if merge_pdfs(args.inputs, args.output):
            print(f"已成功合并为: {args.output}")
        else:
            print("合并失败")
    
    elif args.command == 'split':
        print(f"正在分割PDF文件: {args.input}")
        output_files = split_pdf(args.input, args.output_dir, args.pages_per_file)
        if output_files:
            print(f"已成功分割为 {len(output_files)} 个文件:")
            for file in output_files:
                print(f"  - {file}")
        else:
            print("分割失败")
    
    elif args.command == 'extract':
        print(f"正在从PDF提取文本: {args.input}")
        text = extract_text(args.input, args.output)
        if args.output:
            print(f"文本已保存到: {args.output}")
        else:
            print("提取的文本:")
            print("-" * 80)
            print(text[:1000] + "..." if len(text) > 1000 else text)
            print("-" * 80)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 