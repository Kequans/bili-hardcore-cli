#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API配置测试脚本
用于验证DeepSeek API是否配置正确
"""

import os
import sys

# 添加bilibili-AIHardcore目录到模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'bilibili-AIHardcore'))

def test_api():
    """测试API配置"""
    print("=" * 50)
    print("DeepSeek API 配置测试")
    print("=" * 50)

    # 从cli_main.py导入配置
    try:
        import cli_main
        api_key = cli_main.DEEPSEEK_API_KEY
        base_url = cli_main.DEEPSEEK_BASE_URL
        model = cli_main.DEEPSEEK_MODEL
    except ImportError:
        print("错误: 无法导入 cli_main.py")
        print("请确保 cli_main.py 文件存在")
        return False

    # 检查API Key是否配置
    if api_key == "your-deepseek-api-key-here" or api_key.startswith("your-"):
        print("❌ API Key 未配置")
        print("请编辑 cli_main.py 文件，设置你的 DEEPSEEK_API_KEY")
        return False

    print(f"✓ API Key: {api_key[:10]}...{api_key[-4:]}")
    print(f"✓ Base URL: {base_url}")
    print(f"✓ Model: {model}")
    print("")

    # 测试API连接
    print("正在测试API连接...")
    try:
        import requests

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        data = {
            "model": model,
            "messages": [
                {"role": "user", "content": "你好"}
            ],
            "max_tokens": 10
        }

        response = requests.post(
            f"{base_url}/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            print(f"✓ API连接成功")
            print(f"✓ 测试响应: {content}")
            print("")
            print("=" * 50)
            print("✓ 配置测试通过！可以运行 cli_main.py 开始答题")
            print("=" * 50)
            return True
        else:
            print(f"❌ API请求失败")
            print(f"状态码: {response.status_code}")
            print(f"响应: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ API请求超时")
        print("请检查网络连接")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API请求失败: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
