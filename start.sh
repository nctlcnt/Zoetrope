#!/bin/bash

# Zoetrope Quick Start Script

echo "🎬 Zoetrope 启动脚本"
echo "===================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装，请先安装 Python 3"
    exit 1
fi

echo "✅ Python 已安装"

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 激活虚拟环境..."
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo "📥 安装依赖..."
pip install -r requirements.txt --quiet

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env 文件不存在，从 .env.example 创建..."
    cp .env.example .env
    echo "📝 请编辑 .env 文件并填入你的 API keys"
fi

echo ""
echo "✅ 设置完成！"
echo ""
echo "🚀 启动后端服务器..."
python run.py
