# B站硬核会员答题助手 - 命令行版本

基于AI的B站硬核会员自动答题工具，使用DeepSeek API进行智能答题。

## 特点

- ✅ 纯命令行界面，无需GUI
- ✅ AI自动分析题目并答题
- ✅ 支持登录信息管理和账号切换
- ✅ 自动下载并显示验证码图片
- ✅ 详细的日志输出

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements-cli.txt
```

### 2. 配置API密钥

编辑 `cli_main.py` 文件，设置你的DeepSeek API密钥：

```python
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # 替换为你的API Key
```

获取API密钥：https://platform.deepseek.com/api_keys

### 3. 运行程序

```bash
./start_cli.sh
# 或
python cli_main.py
```

## 主要功能

### 自动答题
- 扫码登录B站账号
- 选择答题分类
- 自动下载并显示验证码图片
- AI自动分析并提交答案
- 实时显示答题过程

### 登录管理
- 自动保存登录信息（7天有效）
- 支持快速切换账号
- 登录信息加密存储

## 使用流程

### 首次使用
```bash
./start_cli.sh
# 或 python cli_main.py

# 1. 扫码登录
# 2. 输入分类ID（例如：1 或 1,2,3）
# 3. 程序自动下载验证码图片并打开
# 4. 输入验证码
# 5. 开始自动答题
```

### 继续使用
```bash
./start_cli.sh
# 检测到已保存的登录信息
# 选择 y 使用已保存的登录信息
# 直接开始答题
```

### 切换账号
```bash
./start_cli.sh
# 选择 n 清除旧登录信息
# 扫码登录新账号
# 开始答题
```

## 工具说明

| 工具 | 命令 | 功能 |
|------|------|------|
| 主程序 | `python cli_main.py` | 自动答题 |
| 快速启动 | `./start_cli.sh` | 一键启动（macOS/Linux） |

## 配置说明

### API配置
在 `cli_main.py` 中配置：

```python
# DeepSeek API配置
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"
```

### 支持其他API服务

**火山引擎：**
```python
DEEPSEEK_API_KEY = "your-volcengine-api-key"
DEEPSEEK_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DEEPSEEK_MODEL = "your-model-endpoint-id"
```

**硅基流动：**
```python
DEEPSEEK_API_KEY = "your-siliconflow-api-key"
DEEPSEEK_BASE_URL = "https://api.siliconflow.cn/v1"
DEEPSEEK_MODEL = "deepseek-ai/DeepSeek-V2.5"
```

## 常见问题

### Q: 验证码如何输入？
A: 程序会自动下载验证码图片并尝试打开。如果无法自动打开，请手动打开当前目录下的 `captcha.jpg` 文件。

### Q: 如何切换账号？
A: 运行程序时选择 n 清除旧登录信息，然后扫码登录新账号。

### Q: 登录信息保存在哪里？
A: `~/.bili-hardcore/auth.json`（有效期7天）

### Q: 二维码显示异常怎么办？
A: 程序会提供链接，访问 https://cli.im/ 手动生成二维码

### Q: API调用失败怎么办？
A:
1. 检查API密钥是否正确
2. 检查网络连接
3. 确认API服务是否正常

## 注意事项

1. **API密钥安全**
   - 不要将包含真实API密钥的代码提交到公共仓库
   - 已添加到 `.gitignore`

2. **登录信息**
   - 登录信息保存在 `~/.bili-hardcore/auth.json`
   - 有效期7天，过期需重新登录
   - 如遇问题可删除该文件重新登录

3. **答题建议**
   - 推荐选择历史分区，准确率较高
   - 避免使用思考模型，防止超时
   - 如AI卡住，可去B站APP手动答题

4. **费用说明**
   - DeepSeek API费用：输入 ¥1/百万tokens，输出 ¥2/百万tokens
   - 每道题约 ¥0.0005（约0.05分）
   - 答100道题约 ¥0.05（5分钱）

## 文件结构

```
bilibili-AIHardcore/
├── cli_main.py              # 主程序（需配置API密钥）
├── start_cli.sh             # 快速启动脚本
├── requirements-cli.txt     # 依赖列表
├── README.md                # 本文件
├── QUICKSTART.md            # 快速开始指南
├── 更新日志.md              # 更新日志
└── bilibili-AIHardcore/     # 核心功能模块
    ├── client/              # B站API客户端
    ├── config/              # 配置管理
    ├── scripts/             # 登录和答题脚本
    └── tools/               # 工具模块（LLM、日志等）
```

## 技术栈

- **Python 3.10+**
- **DeepSeek API** - AI模型
- **requests** - HTTP请求
- **qrcode** - 二维码生成

## 更新日志

查看 [更新日志.md](更新日志.md) 了解详细的更新内容。

## 许可证

本项目基于原仓库修改，仅供学习交流使用。

## 致谢

- 原项目：bilibili-AIHardcore
- AI模型：DeepSeek

---

**立即开始**: `./start_cli.sh` 🚀
