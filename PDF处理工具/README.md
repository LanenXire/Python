# PDF文档处理工具

这是一个简单的PDF处理工具，可以执行以下操作：
- 合并多个PDF文件
- 按页数分割PDF文件
- 从PDF中提取文本

## 功能特点

- 简单易用的图形用户界面
- 支持拖放文件
- 实时文本预览
- 批量处理能力

## 安装和运行

### 前提条件

- Python 3.6 或更高版本
- 安装所需依赖项

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行程序

```bash
python run.py
```

## 使用方法

### 合并PDF

1. 切换到"合并PDF"选项卡
2. 点击"添加文件"选择多个PDF文件
3. 调整文件顺序（通过上下移动）
4. 点击"合并PDF"选择输出文件
5. 确认合并操作

### 分割PDF

1. 切换到"分割PDF"选项卡
2. 选择要分割的PDF文件
3. 设置每个新文件包含的页数
4. 选择输出目录
5. 点击"分割PDF"执行操作

### 提取文本

1. 切换到"提取文本"选项卡
2. 选择要提取文本的PDF文件
3. 选择是否保存到文件
4. 点击"提取文本"
5. 在预览区域查看提取的文本

## 命令行使用

除了图形界面，也可以通过命令行使用：

```bash
python src/main.py merge input1.pdf input2.pdf -o output.pdf
python src/main.py split input.pdf -o output_dir -p 5
python src/main.py extract input.pdf -o output.txt
```

## 注意事项

- 对于大型PDF文件，处理可能需要更长时间
- 某些加密的PDF可能无法处理
- 文本提取功能可能对于扫描PDF效果不佳 