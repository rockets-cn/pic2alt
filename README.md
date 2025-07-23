# Pic2Alt - 图片Alt文本提取工具

一个使用Ollama AI模型自动为图片生成中文alt文本描述的工具。支持批量处理图片并生成CSV格式的结果文件。

## 功能特点

- 🖼️ 支持多种图片格式（JPG、PNG、GIF、BMP、WebP、TIFF等）
- 🤖 使用Ollama minicpm-v模型进行智能图片描述
- 📝 生成适合作为alt属性的简洁中文描述
- 📊 批量处理并输出CSV格式结果
- 🔍 自动检测Ollama服务状态
- 📁 自动扫描指定目录下的图片文件

## 安装要求

### 系统要求
- Python 3.6+
- Ollama服务（本地运行）
- minicpm-v模型

### Python依赖
```bash
pip install -r requirements.txt
```

### Ollama安装与配置
1. 安装Ollama：访问 [ollama.ai](https://ollama.ai) 下载并安装
2. 启动Ollama服务：
   ```bash
   ollama serve
   ```
3. 下载minicpm-v模型：
   ```bash
   ollama pull minicpm-v
   ```

## 使用方法

### 基本使用
1. 将需要处理的图片放入 `picture/` 目录
2. 运行主程序：
   ```bash
   python extract_alt.py
   ```
3. 查看生成的 `alt_texts.csv` 文件

### 测试模式
如果Ollama未运行或没有图片，可以使用测试模式：
```bash
# 创建测试CSV文件
python test_simple.py

# 或运行轻量级测试版本
python test_extract.py
```

## 文件结构

```
pic2alt/
├── extract_alt.py      # 主程序 - 完整功能版本
├── test_extract.py     # 测试版本 - 轻量级
├── test_simple.py      # 简单测试 - 创建示例CSV
├── requirements.txt    # Python依赖
├── alt_texts.csv       # 输出结果文件
└── picture/            # 图片存储目录
    ├── IMG_8718.jpeg
    ├── pose.jpg
    ├── sen0486.jpg
    ├── unihiker.jpg
    ├── 显微镜.jpg
    └── 行空板扩展板.jpg
```

## 配置选项

### 自定义参数
在 `extract_alt.py` 中可以修改以下参数：

- `model_name`: 使用的Ollama模型名称（默认：minicpm-v）
- `picture_dir`: 图片目录路径（默认：picture）
- `output_file`: 输出CSV文件名（默认：alt_texts.csv）
- `ollama_base_url`: Ollama服务地址（默认：http://localhost:11434）

### 示例
```python
extractor = AltTextExtractor(
    model_name="minicpm-v",
    picture_dir="my_images",
    output_file="results.csv"
)
```

## 输出格式

生成的CSV文件包含两列：
- `filename`: 图片文件名
- `alt_text`: 生成的中文alt文本描述

### 示例输出
```csv
filename,alt_text
pose.jpg,人物姿势演示图片
显微镜.jpg,实验室显微镜设备
unihiker.jpg,Unihiker开发板
```

## 故障排除

### 常见问题

#### Ollama连接失败
- 确保Ollama服务正在运行：`ollama serve`
- 检查防火墙设置
- 确认minicpm-v模型已下载：`ollama pull minicpm-v`

#### 没有找到图片文件
- 检查 `picture/` 目录是否存在
- 确认图片格式是否受支持
- 检查文件扩展名是否正确

#### 中文描述乱码
- 确保系统支持UTF-8编码
- CSV文件使用UTF-8编码保存

### 错误处理
程序会捕获并显示以下错误：
- Ollama服务连接错误
- 图片文件读取错误
- 模型响应错误
- 文件写入错误

## 技术实现

### 工作原理
1. 扫描指定目录下的所有图片文件
2. 将图片编码为base64格式
3. 通过Ollama API发送图片和提示词
4. 接收并解析AI生成的描述文本
5. 将结果保存为CSV格式

### API调用示例
```python
payload = {
    "model": "minicpm-v",
    "prompt": "请描述这张图片的内容，用简洁的中文描述，适合作为alt属性文本。",
    "images": [base64_image],
    "stream": False,
    "options": {
        "temperature": 0.3,
        "top_p": 0.8
    }
}
```

## 开发说明

### 扩展功能
- 支持更多图片格式
- 添加多语言描述支持
- 集成其他AI模型
- 添加Web界面
- 支持批量目录处理

### 性能优化
- 支持并发处理
- 添加缓存机制
- 优化大图片处理
- 添加进度显示

## 许可证

本项目采用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 联系方式

如有问题或建议，请通过GitHub Issues联系。