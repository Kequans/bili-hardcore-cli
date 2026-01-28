import requests
import os
from typing import Dict, Any, Optional
from config.config import PROMPT, API_KEY_DEEPSEEK, load_model_config
from time import time

class DeepSeekAPI:
    def __init__(self):
        # 加载DeepSeek模型配置
        config = load_model_config('deepseek')
        self.base_url = config['base_url']
        self.model = config['model']
        # 优先使用环境变量中的API Key，其次使用配置文件中的
        self.api_key = os.environ.get('DEEPSEEK_API_KEY', API_KEY_DEEPSEEK)

    def ask(self, question: str, timeout: Optional[int] = 30) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": PROMPT.format(time(), question)
                }
            ]
        }

        try:
            print(f"[DEBUG] 正在调用DeepSeek API...")
            print(f"[DEBUG] API地址: {url}")
            print(f"[DEBUG] 模型: {self.model}")
            print(f"[DEBUG] API Key: {self.api_key[:10]}...{self.api_key[-4:]}")

            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=timeout
            )
            response.raise_for_status()

            result = response.json()["choices"][0]["message"]["content"]
            print(f"[DEBUG] API返回结果: {result}")

            return result
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] DeepSeek API调用失败: {str(e)}")
            raise Exception(f"DeepSeek API request failed: {str(e)}")