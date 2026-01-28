#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
查看登录状态工具
显示当前的登录信息和状态
"""

import sys
import os
import json

# 添加bilibili-AIHardcore目录到模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'bilibili-AIHardcore'))

from config.config import AUTH_FILE
import time

def main():
    """主函数"""
    print("=" * 60)
    print("B站答题助手 - 登录状态查看")
    print("=" * 60)
    print()

    # 检查是否有登录信息
    if not os.path.exists(AUTH_FILE):
        print("❌ 未登录")
        print()
        print("没有找到已保存的登录信息")
        print(f"文件路径: {AUTH_FILE}")
        print()
        print("请运行 cli_main.py 进行登录")
        return

    print("✓ 已登录")
    print()

    # 读取并显示登录信息
    try:
        with open(AUTH_FILE, 'r') as f:
            auth_data = json.load(f)

        print("登录信息详情:")
        print("-" * 60)

        # 显示用户ID
        if 'mid' in auth_data:
            print(f"  用户ID (MID): {auth_data['mid']}")

        # 显示access_token（部分隐藏）
        if 'access_token' in auth_data:
            token = auth_data['access_token']
            if len(token) > 20:
                print(f"  Access Token: {token[:10]}...{token[-10:]}")
            else:
                print(f"  Access Token: {token}")

        # 显示csrf（部分隐藏）
        if 'csrf' in auth_data:
            csrf = auth_data['csrf']
            if len(csrf) > 10:
                print(f"  CSRF Token: {csrf[:5]}...{csrf[-5:]}")
            else:
                print(f"  CSRF Token: {csrf}")

        # 显示cookie数量
        if 'cookie' in auth_data:
            cookie_str = auth_data['cookie']
            cookie_count = len(cookie_str.split(';'))
            print(f"  Cookie数量: {cookie_count} 个")

        print()

        # 显示文件信息
        file_mtime = os.path.getmtime(AUTH_FILE)
        login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_mtime))
        print(f"  登录时间: {login_time}")

        # 计算有效期
        current_time = time.time()
        days_passed = (current_time - file_mtime) / (24 * 3600)
        days_left = 7 - days_passed

        print(f"  已使用: {days_passed:.1f} 天")

        if days_left > 0:
            print(f"  剩余有效期: {days_left:.1f} 天")
            print(f"  状态: ✓ 有效")
        else:
            print(f"  状态: ✗ 已过期 (超过7天)")
            print()
            print("  建议: 运行 clear_login.py 清除过期信息并重新登录")

        # 显示文件信息
        file_size = os.path.getsize(AUTH_FILE)
        print()
        print(f"  文件大小: {file_size} 字节")
        print(f"  文件路径: {AUTH_FILE}")

        print("-" * 60)

    except json.JSONDecodeError:
        print("✗ 登录信息文件损坏")
        print()
        print("建议: 运行 clear_login.py 清除损坏的文件并重新登录")
    except Exception as e:
        print(f"✗ 读取登录信息失败: {str(e)}")

    print()
    print("可用操作:")
    print("  - 运行 cli_main.py 开始答题")
    print("  - 运行 clear_login.py 清除登录信息")
    print()

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
