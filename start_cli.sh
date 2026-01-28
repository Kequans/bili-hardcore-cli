#!/bin/bash

# B站答题助手 - 命令行版本快速启动脚本

echo "=================================="
echo "B站硬核会员答题助手 - 命令行版本"
echo "=================================="
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查是否已安装依赖
if ! python3 -c "import requests" &> /dev/null; then
    echo "检测到未安装依赖，正在安装..."
    pip3 install -r requirements-cli.txt
    echo ""
fi

# 检查API密钥是否配置
if grep -q "your-deepseek-api-key-here\|your-volcengine-api-key\|your-siliconflow-api-key" cli_main.py | grep -v "^#"; then
    echo "警告: 检测到API密钥未配置！"
    echo "请编辑 cli_main.py 文件，设置你的 DEEPSEEK_API_KEY"
    echo ""
    read -p "是否现在编辑配置文件？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} cli_main.py
    else
        echo "请手动编辑 cli_main.py 文件后再运行"
        exit 1
    fi
fi

# 运行程序
echo "启动程序..."
echo ""
python3 cli_main.py
