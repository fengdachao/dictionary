#!/bin/bash

# 中英翻译和英文字典系统启动脚本

echo "=== 中英翻译和英文字典系统 ==="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查pip是否安装
if ! command -v pip3 &> /dev/null; then
    echo "错误: 未找到pip3，请先安装pip3"
    exit 1
fi

echo "检查依赖包..."
# 安装依赖
pip3 install -r requirements.txt

echo ""
echo "请选择运行模式:"
echo "1. 命令行界面"
echo "2. Web界面"
echo "3. 退出"
echo ""

read -p "请输入选择 (1-3): " choice

case $choice in
    1)
        echo "启动命令行界面..."
        python3 translator.py
        ;;
    2)
        echo "启动Web界面..."
        echo "启动后请在浏览器中访问: http://localhost:5000"
        python3 web_app.py
        ;;
    3)
        echo "退出"
        exit 0
        ;;
    *)
        echo "无效选择"
        exit 1
        ;;
esac