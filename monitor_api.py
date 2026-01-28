#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
实时监控API调用
显示每次API请求的详细信息
"""

import sys
import os

# 添加bilibili-AIHardcore目录到模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'bilibili-AIHardcore'))

# 从cli_main导入配置
import cli_main

# 设置环境变量
os.environ['DEEPSEEK_API_KEY'] = cli_main.DEEPSEEK_API_KEY

import requests
from datetime import datetime

# 保存原始的requests.post方法
original_post = requests.post

# 创建一个包装函数来监控所有POST请求
def monitored_post(*args, **kwargs):
    url = args[0] if args else kwargs.get('url', 'Unknown')

    # 只监控DeepSeek API调用
    if 'deepseek.com' in url or 'chat/completions' in url:
        print("\n" + "=" * 70)
        print(f"🔔 检测到API调用！")
        print(f"⏰ 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 URL: {url}")

        # 显示请求数据
        if 'json' in kwargs:
            data = kwargs['json']
            print(f"📤 请求数据:")
            print(f"   - 模型: {data.get('model', 'N/A')}")
            if 'messages' in data and len(data['messages']) > 0:
                content = data['messages'][0].get('content', '')
                # 只显示前200个字符
                if len(content) > 200:
                    content = content[:200] + "..."
                print(f"   - 问题: {content}")

        # 显示请求头（隐藏完整的API Key）
        if 'headers' in kwargs:
            headers = kwargs['headers']
            if 'Authorization' in headers:
                auth = headers['Authorization']
                if 'Bearer' in auth:
                    key = auth.replace('Bearer ', '')
                    print(f"   - API Key: {key[:10]}...{key[-4:]}")

    # 调用原始的post方法
    response = original_post(*args, **kwargs)

    # 如果是DeepSeek API，显示响应
    if 'deepseek.com' in url or 'chat/completions' in url:
        try:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                answer = result['choices'][0]['message']['content']
                print(f"📥 AI回答: {answer}")
                print(f"✅ API调用成功！")
        except:
            print(f"⚠️  响应状态: {response.status_code}")
        print("=" * 70 + "\n")

    return response

# 替换requests.post方法
requests.post = monitored_post

print("=" * 70)
print("🔍 API调用监控器已启动")
print("=" * 70)
print("现在运行的任何代码中的DeepSeek API调用都会被监控和显示")
print("=" * 70)
print()

# 导入并测试
from tools.LLM.deepseek import DeepSeekAPI
from config import config

# 更新配置
config.model_choice = '1'
config.API_KEY_DEEPSEEK = cli_main.DEEPSEEK_API_KEY
config.MODEL_CONFIGS['deepseek']['base_url'] = cli_main.DEEPSEEK_BASE_URL
config.MODEL_CONFIGS['deepseek']['model'] = cli_main.DEEPSEEK_MODEL

print("📝 测试问题: 1+1等于几？")
print()

# 创建DeepSeek API实例并测试
llm = DeepSeekAPI()

test_question = """
题目: 1+1等于几？
答案: [{'ans_text': '1'}, {'ans_text': '2'}, {'ans_text': '3'}, {'ans_text': '4'}]
"""

try:
    answer = llm.ask(test_question)
    print(f"\n✅ 最终答案: {answer}")
    print("\n" + "=" * 70)
    print("✅ 监控测试完成！")
    print("=" * 70)
    print("\n如果你看到了上面的API调用信息，说明AI确实在工作！")
    print("在实际答题时，每道题都会产生类似的API调用。")
except Exception as e:
    print(f"\n❌ 错误: {str(e)}")
    import traceback
    traceback.print_exc()
