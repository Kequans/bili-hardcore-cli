#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
清除登录信息工具
用于清除已保存的B站登录cookie和认证信息
"""

import sys
import os

# 添加bilibili-AIHardcore目录到模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'bilibili-AIHardcore'))

from scripts.login import logout, is_login
from config.config import AUTH_FILE
from tools.logger import logger
import time

def main():
    """主函数"""
    print("=" * 60)
    print("B站答题助手 - 清除登录信息工具")
    print("=" * 60)
    print()

    # 检查是否有登录信息
    if not os.path.exists(AUTH_FILE):
        print("✓ 没有找到已保存的登录信息")
        print("  文件路径:", AUTH_FILE)
        print()
        print("无需清除，可以直接运行 cli_main.py 进行新的登录")
        return

    # 显示登录信息详情
    print("找到已保存的登录信息:")
    print("-" * 60)
    try:
        file_mtime = os.path.getmtime(AUTH_FILE)
        login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_mtime))
        print(f"  登录时间: {login_time}")

        # 计算剩余有效期
        current_time = time.time()
        days_passed = (current_time - file_mtime) / (24 * 3600)
        days_left = 7 - days_passed

        if days_left > 0:
            print(f"  已使用: {days_passed:.1f} 天")
            print(f"  剩余有效期: {days_left:.1f} 天")
        else:
            print(f"  状态: 已过期 (超过7天)")

        # 显示文件大小
        file_size = os.path.getsize(AUTH_FILE)
        print(f"  文件大小: {file_size} 字节")
        print(f"  文件路径: {AUTH_FILE}")

    except Exception as e:
        print(f"  无法读取详细信息: {str(e)}")

    print("-" * 60)
    print()

    # 询问是否确认清除
    while True:
        choice = input("是否确认清除登录信息？(y/n): ").strip().lower()
        if choice in ['y', 'yes', 'n', 'no']:
            break
        print("无效的输入，请输入 y 或 n")

    if choice in ['n', 'no']:
        print()
        print("✓ 已取消清除操作")
        print("  登录信息保持不变")
        return

    # 执行清除操作
    print()
    print("正在清除登录信息...")

    if logout():
        print()
        print("=" * 60)
        print("✓ 登录信息已成功清除！")
        print("=" * 60)
        print()
        print("下次运行 cli_main.py 时将需要重新登录")
        print()
    else:
        print()
        print("=" * 60)
        print("✗ 清除登录信息失败")
        print("=" * 60)
        print()
        print("可能的原因:")
        print("  1. 文件权限问题")
        print("  2. 文件被其他程序占用")
        print()
        print("你可以尝试手动删除文件:")
        print(f"  rm -rf {AUTH_FILE}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
