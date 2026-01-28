# 快速开始指南

## 5分钟快速上手

### 第一步：安装依赖

```bash
cd /Users/kequan/Desktop/Test/bilibili-AIHardcore
pip install -r requirements-cli.txt
```

### 第二步：配置API密钥

1. 访问 https://platform.deepseek.com/api_keys 获取API密钥
2. 编辑 `cli_main.py` 文件
3. 找到这一行：
   ```python
   DEEPSEEK_API_KEY = "your-deepseek-api-key-here"
   ```
4. 替换为你的实际API密钥：
   ```python
   DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```
5. 保存文件

### 第三步：测试配置

```bash
python test_api.py
```

看到 `✓ 配置测试通过！` 就可以继续了。

### 第四步：运行程序

```bash
python cli_main.py
```

### 第五步：登录和答题

1. **扫码登录**
   - 程序会显示二维码
   - 使用哔哩哔哩APP扫码登录
   - 如果二维码显示不正常，使用程序提供的链接手动生成

2. **输入分类和验证码**
   - 程序会显示可用的答题分类
   - 输入分类ID（推荐选择历史分区）
   - 打开验证码链接，输入验证码

3. **自动答题**
   - 验证通过后，程序会自动开始答题
   - 所有过程都在命令行中显示
   - 等待答题完成即可

## 示例输出

```
==================================================
B站硬核会员答题助手 - 命令行版本
==================================================
使用模型: DeepSeek (deepseek-chat)
API地址: https://api.deepseek.com
==================================================
开始登录流程...
请使用哔哩哔哩APP扫描二维码登录
[二维码显示]
登录成功，开始答题...
==================================================
第1题:大的反义词是什么？
1. 长
2. 宽
3. 小
4. 热
AI给出的答案:3
答案提交成功
...
```

## 常见问题快速解决

### 切换账号
```bash
# 方法1：使用主程序
python cli_main.py
# 选择 n 清除旧登录信息，然后扫码登录新账号

# 方法2：先清除再登录
python clear_login.py  # 清除旧登录信息
python cli_main.py     # 登录新账号
```

### 查看登录状态
```bash
python check_login.py
```

### API配置错误
```bash
# 重新测试API配置
python test_api.py
```

### 登录失败
```bash
# 删除缓存的登录信息
python clear_login.py
# 或手动删除
rm -rf ~/.bili-hardcore/auth.json
# 重新运行程序
python cli_main.py
```

### 二维码显示异常
- 程序会提供一个链接
- 访问 https://cli.im/
- 粘贴链接生成二维码
- 使用APP扫描

## 进阶配置

### 使用其他兼容OpenAI API的服务

编辑 `cli_main.py`，修改配置：

**火山引擎示例：**
```python
DEEPSEEK_API_KEY = "your-volcengine-api-key"
DEEPSEEK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEEPSEEK_MODEL = "your-model-endpoint-id"
```

**硅基流动示例：**
```python
DEEPSEEK_API_KEY = "your-siliconflow-api-key"
DEEPSEEK_BASE_URL = "https://api.siliconflow.cn/v1"
DEEPSEEK_MODEL = "deepseek-ai/DeepSeek-V2.5"
```

## 文件说明

| 文件 | 说明 |
|------|------|
| `cli_main.py` | 主程序（需要配置API密钥） |
| `test_api.py` | API配置测试工具 |
| `start_cli.sh` | 快速启动脚本（macOS/Linux） |
| `requirements-cli.txt` | 命令行版本依赖 |
| `CLI_README.md` | 详细使用文档 |
| `QUICKSTART.md` | 本文件 |

## 获取帮助

如果遇到问题：
1. 查看 `CLI_README.md` 详细文档
2. 运行 `python test_api.py` 测试配置
3. 检查 `~/.bili-hardcore/` 目录下的日志文件
