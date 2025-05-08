import os
import argparse
import sys
from image_processor import ImageProcessor

def main():
    """主函数，处理命令行参数并执行相应的操作"""
    parser = argparse.ArgumentParser(description='批量图片处理工具')
    subparsers = parser.add_subparsers(dest='command', help='操作命令')
    
    # 调整大小命令
    resize_parser = subparsers.add_parser('resize', help='批量调整图片大小')
    resize_parser.add_argument('-i', '--input', required=True, help='输入目录')
    resize_parser.add_argument('-o', '--output', required=True, help='输出目录')
    resize_parser.add_argument('-w', '--width', type=int, required=True, help='目标宽度')
    resize_parser.add_argument('-h', '--height', type=int, required=True, help='目标高度')
    
    # 格式转换命令
    convert_parser = subparsers.add_parser('convert', help='批量转换图片格式')
    convert_parser.add_argument('-i', '--input', required=True, help='输入目录')
    convert_parser.add_argument('-o', '--output', required=True, help='输出目录')
    convert_parser.add_argument('-f', '--format', required=True, choices=['jpeg', 'png', 'bmp', 'gif', 'webp'], help='目标格式')
    
    # 添加水印命令
    watermark_parser = subparsers.add_parser('watermark', help='批量添加水印')
    watermark_parser.add_argument('-i', '--input', required=True, help='输入目录')
    watermark_parser.add_argument('-o', '--output', required=True, help='输出目录')
    # 水印文本和水印图片至少需要一个
    watermark_group = watermark_parser.add_mutually_exclusive_group(required=True)
    watermark_group.add_argument('-t', '--text', help='水印文本')
    watermark_group.add_argument('-m', '--image', help='水印图片路径')
    watermark_parser.add_argument('-p', '--position', default='center', help='水印位置 (x,y 或 center)')
    watermark_parser.add_argument('-a', '--opacity', type=float, default=0.5, help='水印透明度 (0.0-1.0)')
    
    args = parser.parse_args()
    
    # 如果没有指定命令，显示帮助信息
    if not args.command:
        parser.print_help()
        return
    
    processor = ImageProcessor()
    
    try:
        # 执行相应的命令
        if args.command == 'resize':
            print(f"正在批量调整图片大小为 {args.width}x{args.height}...")
            results = processor.batch_process(
                args.input, 
                args.output, 
                'resize', 
                size=(args.width, args.height)
            )
        
        elif args.command == 'convert':
            print(f"正在批量转换图片格式为 {args.format}...")
            results = processor.batch_process(
                args.input, 
                args.output, 
                'convert', 
                format_name=args.format
            )
        
        elif args.command == 'watermark':
            # 处理位置参数
            position = args.position
            if position != 'center' and ',' in position:
                try:
                    x, y = map(int, position.split(','))
                    position = (x, y)
                except ValueError:
                    print("位置格式错误，应为 'x,y' 或 'center'")
                    return
            
            watermark_type = "文本" if args.text else "图片"
            print(f"正在批量添加{watermark_type}水印...")
            
            results = processor.batch_process(
                args.input, 
                args.output, 
                'watermark', 
                watermark_text=args.text,
                watermark_image=args.image,
                position=position,
                opacity=args.opacity
            )
        
        # 打印处理结果
        print(f"处理完成!")
        print(f"成功: {results['success']} 张图片")
        print(f"失败: {results['fail']} 张图片")
        print(f"跳过: {results['skipped']} 个文件 (非支持的图片格式)")
        
    except Exception as e:
        print(f"处理过程中出错: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 