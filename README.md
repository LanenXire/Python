# Python练习项目集

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

个人进行Python练习的项目，用于学习和实践Python编程技能。
每个子目录都是一个独立的项目，有各自的功能和用途。

## 项目结构

```
Python/
├── PDF处理工具/         # PDF文档处理工具，支持合并、分割和文本提取
├── 图片批处理工具/      # 图片批处理工具，支持调整大小、格式转换和添加水印
├── 网络监测器/          # 网络监测工具，监控网络连接状态并在断网时发出提醒
├── [未来项目目录]/      # 更多练习项目将被添加到这里
└── README.md           # 本文档
```

## 已有项目

### 1. PDF处理工具

一个简单的PDF处理工具，可以执行以下操作：
- 合并多个PDF文件
- 按页数分割PDF文件
- 从PDF中提取文本

提供命令行和图形界面两种使用方式。详情请参阅 [PDF处理工具/README.md](PDF处理工具/README.md)。

### 2. 图片批处理工具

一个功能强大的图片批处理工具，可以执行以下操作：
- 批量或单张调整图片大小
- 批量或单张转换图片格式（支持JPEG、PNG、BMP、GIF和WEBP）
- 批量或单张添加水印（支持文本和图片水印）

提供用户友好的图形界面和命令行两种使用方式。详情请参阅 [图片批处理工具/README.md](图片批处理工具/README.md)。

### 3. 网络监测器

一个实用的网络连接监测工具，可以执行以下操作：
- 实时监控网络连接状态
- 断网时通过声音和桌面通知提醒
- 记录并可视化网络连接历史
- 提供图形界面和控制台两种使用模式

适用于需要稳定网络连接的场景，如远程办公、在线会议等。详情请参阅 [网络监测器/README.md](网络监测器/README.md)。

## 如何使用

1. 克隆此仓库
   ```bash
   git clone https://github.com/LanenXire/Python.git
   git clone https://gitee.com/lanenDCku/python.git
   cd Python
   ```

2. 进入感兴趣的项目目录
   ```bash
   cd 网络监测器
   ```

3. 按照项目README中的说明安装依赖并运行

## 环境要求

- Python 3.6+
- 各项目可能有特定的依赖项，请参阅各自的README文件

## 贡献指南

欢迎贡献新的项目或改进现有项目！请遵循以下步骤：

1. Fork本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m '添加了一些很棒的功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个Pull Request

## 许可证

本项目采用MIT许可证 - 详情请参阅 [LICENSE](LICENSE) 文件 