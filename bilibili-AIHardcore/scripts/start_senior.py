from client.senior import captcha_get, captcha_submit, category_get, question_get, question_submit
from tools.logger import logger
from tools.LLM.gemini import GeminiAPI
from tools.LLM.deepseek import DeepSeekAPI
from tools.LLM.custom import CustomAPI
from config.config import model_choice
from time import sleep
import os
import requests
from tools.request_b import session, headers as bili_headers

class QuizSession:
    def __init__(self):
        self.question_id = None
        self.answers = None
        self.question_num = 0
        self.question = None
        self.stopped = False
        # 从配置中获取当前选择的模型
        self.current_model = model_choice

    def start(self):
        """开始答题会话"""
        try:
            while self.question_num < 100 and not self.stopped:
                if not self.get_question():
                    logger.error("获取题目失败")
                    return
                
                # 检查是否停止
                if self.stopped:
                    logger.info("答题已停止")
                    return
                
                # 显示题目信息
                self.display_question()

                # 根据用户选择初始化对应的LLM模型
                # 使用类中缓存的当前模型选择，这样可以随时更新
                logger.info("=" * 50)
                logger.info("正在调用AI模型进行答题...")
                if self.current_model == '1':
                    logger.info("使用模型: DeepSeek")
                    llm = DeepSeekAPI()
                elif self.current_model == '2':
                    logger.info("使用模型: Gemini")
                    llm = GeminiAPI()
                elif self.current_model == '3':
                    logger.info("使用模型: Custom")
                    llm = CustomAPI()
                else:
                    logger.info("使用模型: DeepSeek (默认)")
                    llm = DeepSeekAPI()

                # 检查是否停止
                if self.stopped:
                    logger.info("答题已停止")
                    return

                logger.info("正在向AI发送问题...")
                answer = llm.ask(self.get_question_prompt())
                logger.info("=" * 50)
                logger.info('✓ AI给出的答案: {}'.format(answer))
                logger.info("=" * 50)
                
                # 检查是否停止
                if self.stopped:
                    logger.info("答题已停止")
                    return
                
                try:
                    answer = int(answer)
                    if not (1 <= answer <= len(self.answers)):
                        logger.warning(f"无效的答案序号: {answer}")
                        continue
                except ValueError:
                    logger.warning("AI回复其他内容,正在重试")
                    continue

                result = self.answers[answer-1]
                
                # 检查是否停止
                if self.stopped:
                    logger.info("答题已停止")
                    return
                
                if not self.submit_answer(result):
                    logger.error("提交答案失败")
                    return
        except KeyboardInterrupt:
            logger.info("答题会话已终止")
        except Exception as e:
            logger.error(f"答题过程发生错误: {str(e)}")
    
    # 允许外部更新当前使用的模型
    def update_model_choice(self, new_model_choice):
        """更新当前使用的模型
        
        Args:
            new_model_choice (str): 新的模型选择 ('1', '2' 或 '3')
        """
        self.current_model = new_model_choice
        logger.info(f"已更新模型选择为: {self.current_model}")

    def get_question(self):
        """获取题目
        
        Returns:
            bool: 是否成功获取题目
        """
        try:
            question = question_get()
            if not question:
                return False

            if question.get('code') != 0:
                logger.info("需要验证码验证")
                return self.handle_verification()

            data = question.get('data', {})
            self.question = data.get('question')
            self.answers = data.get('answers', [])
            self.question_id = data.get('id')
            self.question_num = data.get('question_num', 0)
            return True

        except Exception as e:
            logger.error(f"获取题目失败: {str(e)}")
            return False

    def handle_verification(self):
        """处理验证码验证
        
        Returns:
            bool: 验证是否成功
        """
        try:
            # 检查是否停止
            if self.stopped:
                logger.info("答题已停止")
                return False
                
            logger.info("获取分类信息...")
            category = category_get()
            if not category:
                return False
            
            # 检查是否停止
            if self.stopped:
                logger.info("答题已停止")
                return False
                
            logger.info("分类信息:")
            for cat in category.get('categories', []):
                logger.info(f"ID: {cat.get('id')} - {cat.get('name')}")
            logger.info("tips: 输入多个分类ID请用 *英文逗号* 隔开,例如:1,2,3")
            ids = input('请输入分类ID: ')

            # 检查是否停止
            if self.stopped:
                logger.info("答题已停止")
                return False
                
            logger.info("获取验证码...")
            captcha_res = captcha_get()
            if not captcha_res:
                return False

            captcha_url = captcha_res.get('url')
            captcha_token = captcha_res.get('token')

            # 尝试下载验证码图片到本地
            try:
                logger.info("正在下载验证码图片...")

                # 使用与B站API相同的session和headers
                request_headers = bili_headers.copy()
                request_headers.update({
                    'Referer': 'https://www.bilibili.com/',
                    'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                })

                response = session.get(captcha_url, headers=request_headers, timeout=10)

                # 检查是否是图片
                content_type = response.headers.get('Content-Type', '')
                if response.status_code == 200 and 'image' in content_type:
                    # 保存到临时文件
                    captcha_file = os.path.join(os.getcwd(), 'captcha.jpg')
                    with open(captcha_file, 'wb') as f:
                        f.write(response.content)
                    logger.info("=" * 50)
                    logger.info(f"✓ 验证码图片已保存到: {captcha_file}")
                    logger.info("=" * 50)

                    # 尝试自动打开图片
                    try:
                        import platform
                        system = platform.system()
                        if system == 'Darwin':  # macOS
                            os.system(f'open "{captcha_file}"')
                            logger.info("✓ 已自动打开验证码图片")
                        elif system == 'Windows':
                            os.system(f'start "" "{captcha_file}"')
                            logger.info("✓ 已自动打开验证码图片")
                        elif system == 'Linux':
                            os.system(f'xdg-open "{captcha_file}"')
                            logger.info("✓ 已自动打开验证码图片")
                        else:
                            logger.info(f"请手动打开图片: {captcha_file}")
                    except Exception as e:
                        logger.info(f"无法自动打开图片，请手动打开: {captcha_file}")

                    logger.info("=" * 50)
                else:
                    # 如果不是图片，显示错误信息
                    logger.warning(f"无法直接获取验证码图片 (状态码: {response.status_code})")
                    logger.warning("=" * 50)
                    logger.warning("⚠️  验证码获取失败")
                    logger.warning("可能的原因:")
                    logger.warning("1. B站API需要特殊的认证")
                    logger.warning("2. 验证码URL已过期")
                    logger.warning("3. 网络问题")
                    logger.warning("=" * 50)
                    logger.info("备用方案: 请在浏览器中打开以下链接")
                    logger.info("注意: 打开后不要刷新页面！")
                    logger.info("=" * 50)
                    logger.info(captcha_url)
                    logger.info("=" * 50)

            except Exception as e:
                logger.warning(f"下载验证码图片出错: {e}")
                logger.info("=" * 50)
                logger.info("请在浏览器中打开以下链接查看验证码:")
                logger.info("注意: 打开后不要刷新页面！")
                logger.info("=" * 50)
                logger.info(captcha_url)
                logger.info("=" * 50)
                
            # 检查是否停止
            if self.stopped:
                logger.info("答题已停止")
                return False
                
            captcha = input('请输入验证码: ')

            if captcha_submit(code=captcha, captcha_token=captcha_token, ids=ids):
                logger.info("验证通过✅")
                # 删除临时验证码文件
                try:
                    captcha_file = os.path.join(os.getcwd(), 'captcha.jpg')
                    if os.path.exists(captcha_file):
                        os.remove(captcha_file)
                except:
                    pass
                return self.get_question()
            else:
                logger.error("验证失败")
                return False

        except Exception as e:
            logger.error(f"验证过程发生错误: {str(e)}")
            return False

    def display_question(self):
        """显示当前题目和选项"""
        if not self.answers:
            logger.warning("没有可用的题目")
            return

        logger.info(f"第{self.question_num}题:{self.question}")
        for i, answer in enumerate(self.answers, 1):
            logger.info(f"{i}. {answer.get('ans_text')}")
    
    def get_question_prompt(self):
        return '''
        题目:{}
        答案:{}
        '''.format(self.question, self.answers)

    def submit_answer(self, answer):
        """提交答案
        
        Args:
            answer (dict): 答案信息
        
        Returns:
            bool: 是否成功提交答案
        """
        try:
            result = question_submit(
                self.question_id,
                answer.get('ans_hash'),
                answer.get('ans_text')
            )
            if result and result.get('code') == 0:
                logger.info("答案提交成功")
                sleep(1)
                return True
            else:
                logger.error(f"答案提交失败: {result}")
                return False
        except Exception as e:
            logger.error(f"提交答案时发生错误: {str(e)}")
            return False

# 创建答题会话实例
quiz_session = QuizSession()

def start():
    """启动答题程序"""
    quiz_session.start()
    logger.info('答题结束')