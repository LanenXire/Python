# 图片批处理工具

这是一个用Python编写的图片批处理工具，可以批量调整图片大小、转换格式和添加水印。

## 功能特点

- **批量调整图片大小**：将一个目录下的所有图片调整为指定尺寸
- **批量转换图片格式**：支持JPEG、PNG、BMP、GIF和WEBP格式之间的转换
- **批量添加水印**：支持文本水印和图片水印，可自定义位置和透明度
- **单张图片处理**：支持选择单张图片进行处理，更加灵活
- **图形用户界面**：简洁易用的图形界面，方便操作
- **命令行界面**：支持命令行操作，方便脚本集成和自动化

## 系统要求

- Python 3.6 或更高版本
- 依赖库: Pillow (PIL), tkinter (图形界面)

## 安装依赖

```bash
pip install Pillow
```

注意：tkinter通常随Python一起安装，如果没有，请根据您的操作系统安装：

- Windows: 通常随Python一起安装
- macOS: `brew install python-tk`
- Linux: `apt-get install python3-tk` (Debian/Ubuntu) 或 `dnf install python3-tkinter` (Fedora)

## 使用方法

### 启动程序

在项目目录下运行：

```bash
python run.py
```

程序会询问您是使用图形界面模式还是命令行模式。

### 图形界面模式

选择图形界面模式后，您可以通过以下步骤操作：

1. 选择功能选项卡（调整大小、格式转换或添加水印）
2. 选择处理模式（批量处理目录或处理单张图片）
3. 设置输入和输出目录（或单张图片）
4. 配置相应的参数
5. 点击"开始处理"按钮

#### 批量处理目录

选择"批量处理目录"模式后：
- 设置包含待处理图片的输入目录
- 设置保存处理结果的输出目录
- 配置相应的参数（尺寸、格式或水印设置）

#### 处理单张图片

选择"处理单张图片"模式后：
- 选择要处理的单张图片
- 设置保存处理结果的输出目录
- 配置相应的参数（尺寸、格式或水印设置）

### 命令行模式

命令行模式支持以下命令：

#### 调整图片大小

```bash
python src/main.py resize -i 输入目录 -o 输出目录 -w 宽度 -h 高度
```

#### 转换图片格式

```bash
python src/main.py convert -i 输入目录 -o 输出目录 -f 格式
```

格式选项：jpeg, png, bmp, gif, webp

#### 添加水印

```bash
# 添加文本水印
python src/main.py watermark -i 输入目录 -o 输出目录 -t "水印文本" [-p "center" 或 "x,y"] [-a 不透明度]

# 添加图片水印
python src/main.py watermark -i 输入目录 -o 输出目录 -m 水印图片路径 [-p "center" 或 "x,y"] [-a 不透明度]
```

## 目录结构

- `src/`: 源代码目录
  - `image_processor.py`: 图片处理核心类
  - `main.py`: 命令行界面
  - `gui.py`: 图形用户界面
- `input/`: 存放待处理的图片
- `output/`: 存放处理后的图片
- `watermarks/`: 存放水印图片
- `run.py`: 启动脚本

## 示例

### 调整大小示例

```bash
python src/main.py resize -i input -o output -w 800 -h 600
```

这将把input目录下的所有图片调整为800x600的尺寸，并保存到output目录。

### 格式转换示例

```bash
python src/main.py convert -i input -o output -f png
```

这将把input目录下的所有图片转换为PNG格式，并保存到output目录。

### 添加水印示例

```bash
python src/main.py watermark -i input -o output -t "© 2025" -p center -a 0.5
```

这将在input目录下的所有图片中央添加半透明的"© 2025"文本水印，并保存到output目录。

## 许可证

MIT许可证 