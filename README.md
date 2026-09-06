# 🤖 AI Test Writer

用 **DeepSeek API + GitHub Actions** 搭建的"自动给代码写单元测试"免费机器人（练手项目）。

当你在 `src/` 下修改 Python 代码并推送到 GitHub 时，机器人会自动：
1. 找出变更的源码文件
2. 调用 DeepSeek API 分析代码
3. 生成 pytest 单元测试，写入 `tests/`
4. 自动提交并推回仓库（提交信息带 `[skip ci]` 防止无限循环）

## ✨ 特性

- **免费运行**：GitHub Actions 公开仓库免费额度 + DeepSeek API 极低成本
- **防自触发**：机器人提交带 `[skip ci]`，不会递归触发自己
- **按变更触发**：只有 `src/**` 变更才运行，不浪费 token
- **零第三方 SDK**：核心脚本仅用 Python 标准库（urllib），无需安装 openai 包

## 📁 目录结构

```
.
├── .github/workflows/ai-test-writer.yml   # GitHub Actions 工作流
├── scripts/write_tests.py                 # 核心：调用 DeepSeek 生成测试
├── src/                                   # 业务源码（放这里才会被扫描）
│   └── calculator.py                      # 示例模块
└── tests/                                 # AI 生成的测试落这里
```

## 🚀 快速开始

### 1. 申请 DeepSeek API Key

到 [platform.deepseek.com](https://platform.deepseek.com) 注册并创建 API Key（形如 `sk-...`）。

### 2. 配置 GitHub Secrets

仓库 Settings → Secrets and variables → Actions → New repository secret：

| 名称 | 值 |
|---|---|
| `DEEPSEEK_API_KEY` | 你的 `sk-...` |
| `DEEPSEEK_MODEL` | （可选）默认 `deepseek-chat` |

### 3. 体验机器人

修改 `src/calculator.py`（加个函数或改逻辑）→ commit → push → 打开仓库 Actions 页
观察工作流运行，完成后 `tests/` 下会出现 AI 生成的 `test_calculator.py`。

## 🧪 本地运行

```bash
# dry-run（无 Key，验证流程）
python scripts/write_tests.py --source src/calculator.py --dry-run

# 真实调用（需先设置环境变量）
set DEEPSEEK_API_KEY=sk-xxx        # Windows
export DEEPSEEK_API_KEY=sk-xxx     # macOS / Linux
python scripts/write_tests.py --source src/calculator.py

# 运行生成的测试
python -m pytest tests -v
```

## ⚠️ 已知限制与改进方向（面试可聊）

- **测试质量需人工把关**：workflow 中运行测试用了 `|| true`，失败不会让 CI 红掉。
  生产化时建议：机器人把测试提交到独立分支并发 PR，由人工 review 后合入。
- **生成失败重试**：可加 1~2 次重试逻辑处理 API 偶发错误。
- **只测 Python**：目前按 `.py` 文件触发，可扩展支持 JS/Java 等。
- **上下文裁剪**：超大文件可只传 diff 而非全文，节省 token。

## 🛡️ 安全说明

- API Key 只存在 GitHub Secrets，绝不写入代码或提交历史
- 机器人提交使用 `GITHUB_TOKEN`（最小权限 `contents: write`）
