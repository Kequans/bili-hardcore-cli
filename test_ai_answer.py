#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试AI答题功能
验证DeepSeek API是否真的被调用
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

# 导入必要的模块
from tools.LLM.deepseek import DeepSeekAPI
from config import config

# 更新配置
config.model_choice = '1'
config.API_KEY_DEEPSEEK = cli_main.DEEPSEEK_API_KEY
config.MODEL_CONFIGS['deepseek']['base_url'] = cli_main.DEEPSEEK_BASE_URL
config.MODEL_CONFIGS['deepseek']['model'] = cli_main.DEEPSEEK_MODEL

print("=" * 60)
print("测试AI答题功能")
print("=" * 60)
print(f"API Key: {cli_main.DEEPSEEK_API_KEY[:10]}...{cli_main.DEEPSEEK_API_KEY[-4:]}")
print(f"Base URL: {cli_main.DEEPSEEK_BASE_URL}")
print(f"Model: {cli_main.DEEPSEEK_MODEL}")
print("=" * 60)

# 创建DeepSeek API实例
llm = DeepSeekAPI()

# 模拟一个答题场景
test_question = """
题目:大的反义词是什么？
答案:[{'ans_text': '长', 'ans_hash': 'xxx'}, {'ans_text': '宽', 'ans_hash': 'yyy'}, {'ans_text': '小', 'ans_hash': 'zzz'}, {'ans_text': '热', 'ans_hash': 'www'}]
"""

print("\n测试问题:")
print(test_question)
print("\n正在调用AI...")
print("-" * 60)

try:
    answer = llm.ask(test_question)
    print("-" * 60)
    print(f"\n✓ AI返回的答案: {answer}")

    # 尝试解析答案
    try:
        answer_num = int(answer.strip())
        print(f"✓ 解析后的答案序号: {answer_num}")

        if 1 <= answer_num <= 4:
            print(f"✓ 答案有效（1-4之间）")
            print("\n" + "=" * 60)
            print("✓ AI答题功能测试通过！")
            print("=" * 60)
        else:
            print(f"⚠ 答案超出范围: {answer_num}")
    except ValueError:
        print(f"⚠ AI返回的不是纯数字: {answer}")
        print("这可能需要在代码中添加更好的答案解析逻辑")

except Exception as e:
    print("-" * 60)
    print(f"\n✗ 测试失败: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
