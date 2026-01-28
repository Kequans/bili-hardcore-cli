# B站硬核会员答题助手 - 命令行版本

基于AI的B站硬核会员自动答题工具，使用DeepSeek API进行智能答题。

## 特点

- ✅ 纯命令行界面，无需GUI
- ✅ AI自动分析题目并答题
- ✅ 支持登录信息管理和账号切换
- ✅ 详细的日志输出
- ✅ 完整的测试工具

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

### 3. 测试配置（推荐）

```bash
python test_api.py
```

### 4. 运行程序

```bash
python cli_main.py
```

## 主要功能

### 自动答题
- 扫码登录B站账号
- 选择答题分类
- AI自动分析并提交答案
- 实时显示答题过程

### 登录管理
- 自动保存登录信息（7天有效）
- 查看登录状态：`python check_login.py`
- 清除登录信息：`python clear_login.py`
- 支持快速切换账号

### 测试工具
- API配置测试：`python test_api.py`
- AI功能测试：`python test_ai_answer.py`
- API调用监控：`python monitor_api.py`

## 使用流程

### 首次使用
```bash
python cli_main.py
# 1. 扫码登录
# 2. 输入分类ID和验证码
# 3. 开始自动答题
```

### 继续使用
```bash
python cli_main.py
# 检测到已保存的登录信息
# 选择 y 使用已保存的登录信息
# 直接开始答题
```

### 切换账号
```bash
python cli_main.py
# 选择 n 清除旧登录信息
# 扫码登录新账号
# 开始答题
```

或使用清除工具：
```bash
python clear_login.py  # 清除旧登录信息
python cli_main.py     # 登录新账号
```

## 工具说明

| 工具 | 命令 | 功能 |
|------|------|------|
| 主程序 | `python cli_main.py` | 自动答题 |
| API测试 | `python test_api.py` | 测试API配置 |
| AI测试 | `python test_ai_answer.py` | 测试AI功能 |
| API监控 | `python monitor_api.py` | 监控API调用 |
| 查看登录 | `python check_login.py` | 查看登录状态 |
| 清除登录 | `python clear_login.py` | 清除登录信息 |
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

### Q: 如何切换账号？
A: 运行 `python clear_login.py` 或在主程序中选择 n

### Q: 如何验证AI是否在工作？
A: 运行 `python test_ai_answer.py` 或 `python monitor_api.py`

### Q: 登录信息保存在哪里？
A: `~/.bili-hardcore/auth.json`（有效期7天）

### Q: 二维码显示异常怎么办？
A: 程序会提供链接，访问 https://cli.im/ 手动生成二维码

### Q: API调用失败怎么办？
A:
1. 检查API密钥是否正确
2. 运行 `python test_api.py` 测试
3. 检查网络连接

### Q: 如何查看登录状态？
A: 运行 `python check_login.py`

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
├── test_api.py              # API配置测试
├── test_ai_answer.py        # AI答题测试
├── monitor_api.py           # API调用监控
├── check_login.py           # 查看登录状态
├── clear_login.py           # 清除登录信息
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

- **Python 3.8+**
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

**立即开始**: `python cli_main.py` 🚀
