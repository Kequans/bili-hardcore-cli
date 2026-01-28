
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
B站答题助手命令行版本
直接在代码中配置API，无需GUI交互
"""

import sys
import os

# 添加bilibili-AIHardcore目录到模块搜索路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'bilibili-AIHardcore'))

# ==================== 配置区域 ====================
# DeepSeek API配置
# 获取API密钥: https://platform.deepseek.com/api_keys
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 请替换为你的实际API Key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# 如果你使用的是其他兼容OpenAI API的服务，可以修改以下配置：
# 例如使用火山引擎:
# DEEPSEEK_API_KEY = "your-volcengine-api-key"
# DEEPSEEK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
# DEEPSEEK_MODEL = "your-model-endpoint-id"

# 例如使用硅基流动:
# DEEPSEEK_API_KEY = "your-siliconflow-api-key"
# DEEPSEEK_BASE_URL = "https://api.siliconflow.cn/v1"
# DEEPSEEK_MODEL = "deepseek-ai/DeepSeek-V2.5"
# =================================================

def main():
    """主函数"""
    # 设置环境变量
    os.environ['DEEPSEEK_API_KEY'] = DEEPSEEK_API_KEY

    # 导入必要的模块
    from scripts.login import auth, logout, is_login
    from scripts.start_senior import quiz_session
    from tools.logger import logger
    from config import config
    from config.config import AUTH_FILE

    # 强制设置为使用DeepSeek模型
    config.model_choice = '1'
    config.API_KEY_DEEPSEEK = DEEPSEEK_API_KEY

    # 更新DeepSeek配置
    config.MODEL_CONFIGS['deepseek']['base_url'] = DEEPSEEK_BASE_URL
    config.MODEL_CONFIGS['deepseek']['model'] = DEEPSEEK_MODEL

    logger.info("=" * 50)
    logger.info("B站硬核会员答题助手 - 命令行版本")
    logger.info("=" * 50)
    logger.info(f"使用模型: DeepSeek ({DEEPSEEK_MODEL})")
    logger.info(f"API地址: {DEEPSEEK_BASE_URL}")
    logger.info("=" * 50)

    # 检查API Key是否已配置
    if DEEPSEEK_API_KEY == "your-deepseek-api-key-here" or DEEPSEEK_API_KEY.startswith("your-"):
        logger.error("=" * 50)
        logger.error("错误: 请先在 cli_main.py 文件中配置你的 DEEPSEEK_API_KEY")
        logger.error("=" * 50)
        logger.error("配置步骤:")
        logger.error("1. 编辑 cli_main.py 文件")
        logger.error("2. 找到 DEEPSEEK_API_KEY 配置项")
        logger.error("3. 将其值替换为你的实际API密钥")
        logger.error("")
        logger.error("获取API密钥: https://platform.deepseek.com/api_keys")
        logger.error("=" * 50)
        sys.exit(1)

    # 检查是否有已保存的登录信息
    if os.path.exists(AUTH_FILE):
        logger.info("")
        logger.info("检测到已保存的登录信息")
        logger.info("=" * 50)

        # 显示登录信息的时间
        try:
            import time
            file_mtime = os.path.getmtime(AUTH_FILE)
            login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_mtime))
            logger.info(f"登录时间: {login_time}")

            # 计算剩余有效期
            current_time = time.time()
            days_left = 7 - (current_time - file_mtime) / (24 * 3600)
            if days_left > 0:
                logger.info(f"剩余有效期: {days_left:.1f} 天")
            else:
                logger.info("登录信息已过期")
        except:
            pass

        logger.info("=" * 50)
        logger.info("")

        # 询问是否清除登录信息
        while True:
            choice = input("是否使用已保存的登录信息？(y/n，输入n将清除并重新登录): ").strip().lower()
            if choice in ['y', 'yes', 'n', 'no']:
                break
            logger.warning("无效的输入，请输入 y 或 n")

        if choice in ['n', 'no']:
            logger.info("正在清除登录信息...")
            if logout():
                logger.info("登录信息已清除，将进行新的登录")
            else:
                logger.error("清除登录信息失败")
                sys.exit(1)
        else:
            logger.info("将使用已保存的登录信息")

        logger.info("")

    # 执行登录流程
    logger.info("开始登录流程...")
    if not auth(gui_mode=False):
        logger.error("登录失败，程序退出")
        sys.exit(1)

    logger.info("登录成功，开始答题...")
    logger.info("=" * 50)

    # 开始答题
    try:
        quiz_session.start()
        logger.info("=" * 50)
        logger.info("答题流程结束")
    except KeyboardInterrupt:
        logger.info("\n用户中断程序")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
