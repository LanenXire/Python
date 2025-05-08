import os
from PIL import Image, ImageDraw, ImageFont

class ImageProcessor:
    """图片处理类，提供调整大小、格式转换和添加水印功能"""
    
    def __init__(self):
        """初始化图片处理器"""
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']
    
    def resize_image(self, image_path, output_path, size):
        """
        调整图片大小
        
        参数:
            image_path (str): 原图片路径
            output_path (str): 输出图片路径
            size (tuple): 目标尺寸 (宽, 高)
        """
        try:
            with Image.open(image_path) as img:
                resized_img = img.resize(size, Image.LANCZOS)
                resized_img.save(output_path)
                return True
        except Exception as e:
            print(f"调整图片大小时出错: {e}")
            return False
    
    def convert_format(self, image_path, output_path, format_name):
        """
        转换图片格式
        
        参数:
            image_path (str): 原图片路径
            output_path (str): 输出图片路径
            format_name (str): 目标格式 ('JPEG', 'PNG', 'BMP', 'GIF', 'WEBP')
        """
        try:
            with Image.open(image_path) as img:
                # 如果转换为JPEG, 确保图片是RGB模式
                if format_name.upper() == 'JPEG' and img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.save(output_path, format_name.upper())
                return True
        except Exception as e:
            print(f"转换图片格式时出错: {e}")
            return False
    
    def add_watermark(self, image_path, output_path, watermark_text=None, watermark_image=None, position=(0, 0), opacity=0.5):
        """
        添加水印
        
        参数:
            image_path (str): 原图片路径
            output_path (str): 输出图片路径
            watermark_text (str, optional): 水印文字
            watermark_image (str, optional): 水印图片路径
            position (tuple): 水印位置 (x, y) 或 'center'
            opacity (float): 水印透明度 (0.0-1.0)
        """
        try:
            with Image.open(image_path) as img:
                # 确保图片是RGB或RGBA
                if img.mode != 'RGBA' and img.mode != 'RGB':
                    img = img.convert('RGBA')
                
                # 创建一个透明的图层用于添加水印
                watermark_layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(watermark_layer)
                
                if watermark_text:
                    # 尝试加载字体，如果失败则使用默认字体
                    try:
                        font = ImageFont.truetype("arial.ttf", 36)
                    except IOError:
                        font = ImageFont.load_default()
                    
                    # 计算文本大小
                    text_size = draw.textbbox((0, 0), watermark_text, font=font)[2:]
                    
                    # 确定水印位置
                    if position == 'center':
                        position = ((img.width - text_size[0]) // 2, (img.height - text_size[1]) // 2)
                    
                    # 绘制文本水印
                    draw.text(position, watermark_text, font=font, fill=(255, 255, 255, int(255 * opacity)))
                
                elif watermark_image:
                    # 添加图片水印
                    with Image.open(watermark_image) as mark_img:
                        # 调整水印图片大小
                        mark_width, mark_height = mark_img.size
                        if mark_width > img.width // 3:
                            ratio = (img.width // 3) / mark_width
                            mark_width = int(mark_width * ratio)
                            mark_height = int(mark_height * ratio)
                            mark_img = mark_img.resize((mark_width, mark_height), Image.LANCZOS)
                        
                        # 确定水印位置
                        if position == 'center':
                            position = ((img.width - mark_width) // 2, (img.height - mark_height) // 2)
                        
                        # 将水印图片粘贴到透明层
                        if mark_img.mode != 'RGBA':
                            mark_img = mark_img.convert('RGBA')
                        
                        # 调整水印图片透明度
                        mark_data = mark_img.getdata()
                        new_data = []
                        for item in mark_data:
                            # 修改alpha通道的值
                            new_data.append((item[0], item[1], item[2], int(item[3] * opacity) if len(item) > 3 else int(255 * opacity)))
                        
                        mark_img.putdata(new_data)
                        watermark_layer.paste(mark_img, position, mark_img)
                
                # 将水印层与原图合并
                result = Image.alpha_composite(img.convert('RGBA'), watermark_layer)
                
                # 保存结果
                if os.path.splitext(output_path)[1].lower() == '.jpg' or os.path.splitext(output_path)[1].lower() == '.jpeg':
                    result = result.convert('RGB')
                
                result.save(output_path)
                return True
        except Exception as e:
            print(f"添加水印时出错: {e}")
            return False
    
    def batch_process(self, input_dir, output_dir, operation, **kwargs):
        """
        批量处理图片
        
        参数:
            input_dir (str): 输入目录
            output_dir (str): 输出目录
            operation (str): 操作类型 ('resize', 'convert', 'watermark')
            **kwargs: 操作特定的参数
        
        返回:
            dict: 处理结果统计
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        result = {'success': 0, 'fail': 0, 'skipped': 0}
        
        for filename in os.listdir(input_dir):
            input_path = os.path.join(input_dir, filename)
            
            # 检查是否为图片文件
            ext = os.path.splitext(filename)[1].lower()
            if ext not in self.supported_formats:
                result['skipped'] += 1
                continue
            
            # 根据操作类型确定输出文件名
            if operation == 'convert' and 'format_name' in kwargs:
                output_filename = os.path.splitext(filename)[0] + '.' + kwargs['format_name'].lower()
            else:
                output_filename = filename
                
            output_path = os.path.join(output_dir, output_filename)
            
            # 根据操作类型执行相应的处理
            success = False
            if operation == 'resize' and 'size' in kwargs:
                success = self.resize_image(input_path, output_path, kwargs['size'])
            elif operation == 'convert' and 'format_name' in kwargs:
                success = self.convert_format(input_path, output_path, kwargs['format_name'])
            elif operation == 'watermark':
                watermark_args = {
                    'watermark_text': kwargs.get('watermark_text'),
                    'watermark_image': kwargs.get('watermark_image'),
                    'position': kwargs.get('position', 'center'),
                    'opacity': kwargs.get('opacity', 0.5)
                }
                success = self.add_watermark(input_path, output_path, **watermark_args)
            
            if success:
                result['success'] += 1
            else:
                result['fail'] += 1
        
        return result 