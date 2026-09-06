# 🤖 AI Test Writer

用 **DeepSeek API + GitHub Actions** 搭建的"自动给代码写单元测试"免费机器人（练手项目）。

当你在 `src/` 下修改源码并推送到 GitHub 时，机器人会自动：
1. 找出变更的源码文件（**自动识别语言**）
2. 调用 DeepSeek API 分析代码
3. 按语言生成对应框架的单元测试，写入 `tests/`
4. 自动提交并推回仓库（提交信息带 `[skip ci]` 防止无限循环）

## ✨ 特性

- **🌍 多语言支持**：自动按文件扩展名选择测试框架
- **免费运行**：GitHub Actions 公开仓库免费额度 + DeepSeek API 极低成本
- **防自触发**：机器人提交带 `[skip ci]`，不会递归触发自己
- **按变更触发**：只有 `src/**` 源码变更才运行，不浪费 token
- **零第三方 SDK**：核心脚本仅用 Python 标准库（urllib），无需安装 openai 包

## 🌐 支持的语言

| 扩展名 | 语言 | 测试框架 |
|---|---|---|
| `.py` | Python | pytest |
| `.js` | JavaScript | Jest |
| `.ts` | TypeScript | Jest + ts-jest |
| `.java` | Java | JUnit 5 |
| `.go` | Go | Go testing |
| `.rs` | Rust | cargo test |
| `.c` / `.cpp` / `.hpp` | C / C++ | 轻量断言 / GoogleTest |

> 把任意受支持语言的源码放进 `src/`，机器人就会为它写对应框架的测试。
> 生成测试的文件命名遵循各语言惯例（如 `tests/test_x.py`、`tests/x.test.js`、`tests/TestX.java`）。

## 📁 目录结构

```
.
├── .github/workflows/ai-test-writer.yml   # GitHub Actions 工作流（多语言触发）
├── scripts/write_tests.py                 # 核心：语言识别 + 调用 DeepSeek 生成测试
├── src/                                   # 业务源码（放这里才会被扫描）
│   ├── calculator.py                      # 示例：Python 模块
│   └── calculator.js                      # 示例：JavaScript 模块
├── tests/                                 # AI 生成的测试落这里
└── package.json                           # JS 测试运行配置
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

## 📖 日常使用手册（无需 AI 协助，自助操作）

> 核心一句话：**把代码放进 `src/` → push 到 GitHub → 机器人自动干活**。

### 日常使用流程（每次就 4 步）

**① 打开项目文件夹**

```powershell
cd "D:\新建文件夹 (2)\Desktop\deepseek harness\ai-test-writer"
```

**② 把你的代码放进 `src/` 文件夹**

支持：`.py` `.js` `.ts` `.java` `.go` `.rs` `.c` `.cpp`

> ⚠️ **重要**：机器人只分析 `src/` 下**新增或改过**的文件。代码在别处的话，复制进 `src/` 即可。

**③ 提交推送（Git 三连）**

```powershell
git add .
git commit -m "添加了我的 XX 功能"
git push
```

**④ 等约 1 分钟，看结果**

打开浏览器 → `https://github.com/bca41229-lang/ai-test-writer/actions`
- 绿色 ✓ = 机器人成功生成测试并提交
- 红色 ✗ = 失败了，点进运行记录看日志（多为 API 偶发错误，重试一次即可）
- 点进具体运行记录可查看每个步骤日志

### 查看机器人生成的测试

**网页方式**：打开 `https://github.com/bca41229-lang/ai-test-writer/tree/main/tests`

**本地方式**：push 后执行 `git pull`，测试会出现在本地 `tests/` 文件夹：

```powershell
git pull
dir tests     # Windows 查看目录
```

### 运行测试，确认代码正确

```powershell
# Python 测试
python -m pytest tests -v

# JavaScript 测试
npx jest tests
```

- **全绿 ✅** = 你的代码行为符合预期
- **有红 ❌** = 测试帮你发现了潜在 Bug（看报错信息定位并修复）

### 你的日常工作循环

```
写/改代码 → git add . → git commit → git push
    ↑                                    ↓
发现问题、修复                   机器人自动写测试
    ↑                                    ↓
跑测试看红绿 ←—————— 拉取测试 (git pull)
```

### 常见问题自查

| 现象 | 原因与解决 |
|---|---|
| push 后 Actions 没跑 | 只改了 `src/` 之外的文件（如 README）→ 机器人不触发，属正常 |
| Actions 红色失败 | 看日志；多为 API 偶发错误，重新 push 一次即可 |
| 想测新代码但旧测试还在 | 正常，机器人只**新增/更新变更文件的测试** |
| 忘了改过什么 | 运行 `git status` 查看 |

### 小贴士

- 示例代码（`calculator.py` / `calculator.js`）随时可以删掉，换成你自己的
- 机器人生成的测试**仅供参考**，AI 偶尔会写错，重要项目请人工 review
- 本地跑测试前确认工具已装：Python 需 `pip install pytest`，JS 需 `npm install jest`

## 🧪 本地运行

```bash
# 查看支持的语言
python scripts/write_tests.py --list-langs

# dry-run（无 Key，验证流程）
python scripts/write_tests.py --source src/calculator.py --dry-run
python scripts/write_tests.py --source src/calculator.js --dry-run

# 真实调用（需先设置环境变量）
set DEEPSEEK_API_KEY=sk-xxx        # Windows
export DEEPSEEK_API_KEY=sk-xxx     # macOS / Linux
python scripts/write_tests.py --source src/calculator.py
python scripts/write_tests.py --source src/calculator.js

# 运行生成的测试
python -m pytest tests -v                          # Python
npx jest tests                                     # JavaScript (需 npm install jest)
```

## ⚠️ 已知限制与改进方向（面试可聊）

- **测试质量需人工把关**：workflow 中运行测试用了 `|| true`，失败不会让 CI 红掉。
  生产化时建议：机器人把测试提交到独立分支并发 PR，由人工 review 后合入。
- **生成失败重试**：可加 1~2 次重试逻辑处理 API 偶发错误。
- **JS 测试需 package.json**：工作流运行 Jest 测试要求仓库有 `package.json`。
- **上下文裁剪**：超大文件可只传 diff 而非全文，节省 token。

## 🛡️ 安全说明

- API Key 只存在 GitHub Secrets，绝不写入代码或提交历史
- 机器人提交使用 `GITHUB_TOKEN`（最小权限 `contents: write`）
