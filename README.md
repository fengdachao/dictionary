# 中英翻译和英文字典系统

基于开源翻译模型的中英翻译和英文字典系统，支持翻译和英文例句查询功能。

## 功能特性

- 🌐 **中英互译**: 支持中文到英文和英文到中文的翻译
- 📚 **英文字典**: 内置英文字典，提供单词释义、发音和例句
- 💡 **智能例句**: 翻译时自动提供相关英文例句
- 🖥️ **多种界面**: 支持命令行界面和Web界面
- 🚀 **开源模型**: 使用Helsinki-NLP的OPUS-MT开源翻译模型

## 系统要求

- Python 3.7+
- 至少4GB内存（推荐8GB+）
- 网络连接（首次运行需要下载模型）

## 安装步骤

1. **克隆或下载项目文件**
   ```bash
   # 确保所有文件都在同一目录下
   ls -la
   # 应该看到: translator.py, web_app.py, requirements.txt, templates/, README.md
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **首次运行（下载模型）**
   ```bash
   python translator.py
   ```
   首次运行会自动下载翻译模型，可能需要几分钟时间。

## 使用方法

### 方法一：命令行界面

```bash
python translator.py
```

启动后会显示菜单：
- 1. 中英翻译
- 2. 英中翻译  
- 3. 英文字典查询
- 4. 翻译并显示例句
- 5. 退出

### 方法二：Web界面

```bash
python web_app.py
```

然后在浏览器中访问：http://localhost:5000

Web界面提供：
- **翻译功能**: 支持中英互译
- **字典查询**: 输入英文单词查询释义和例句
- **翻译+例句**: 翻译文本并自动显示相关例句

## 内置字典词汇

系统内置了常用英文单词的字典，包括：
- hello, world, beautiful, computer
- learn, love, time, good
- friend, home

每个单词包含：
- 发音音标
- 中文释义
- 英文定义
- 实用例句

## 技术架构

### 翻译模型
- **主要模型**: Helsinki-NLP/opus-mt-zh-en (中英)
- **备用模型**: Helsinki-NLP/opus-mt-en-zh (英中)
- **框架**: Transformers + PyTorch

### 系统组件
- `translator.py`: 核心翻译和字典功能
- `web_app.py`: Flask Web服务
- `templates/index.html`: Web界面
- `requirements.txt`: 依赖包列表

## API接口

### 翻译接口
```http
POST /api/translate
Content-Type: application/json

{
    "text": "你好世界",
    "source_lang": "zh"
}
```

### 字典查询接口
```http
GET /api/dictionary/hello
```

### 翻译+例句接口
```http
POST /api/translate_with_examples
Content-Type: application/json

{
    "text": "你好世界",
    "source_lang": "zh"
}
```

## 故障排除

### 常见问题

1. **模型下载失败**
   - 检查网络连接
   - 尝试使用VPN或代理
   - 手动下载模型到本地

2. **内存不足**
   - 关闭其他程序释放内存
   - 使用CPU模式（自动检测）

3. **翻译质量不佳**
   - 输入文本要清晰完整
   - 避免过长的句子
   - 可以尝试分段翻译

### 性能优化

- **GPU加速**: 系统会自动检测并使用GPU（如果可用）
- **模型缓存**: 模型会缓存在本地，避免重复下载
- **批处理**: 支持批量翻译（在代码中实现）

## 扩展功能

### 添加更多字典词汇
编辑 `translator.py` 中的 `_init_dictionary()` 方法，添加更多单词：

```python
"new_word": {
    "pronunciation": "/pronunciation/",
    "definitions": ["definition1", "definition2"],
    "examples": ["example1", "example2"],
    "chinese": "中文释义"
}
```

### 集成在线字典API
可以集成有道、百度等在线字典API获取更多词汇和例句。

### 支持更多语言
可以添加其他语言对的翻译模型，如日英、韩英等。

## 许可证

本项目使用MIT许可证，详见LICENSE文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 更新日志

### v1.0.0
- 实现基础中英翻译功能
- 添加英文字典和例句功能
- 提供命令行和Web两种界面
- 使用Helsinki-NLP开源翻译模型