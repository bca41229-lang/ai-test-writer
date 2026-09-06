"""AI 单元测试生成器：调用 DeepSeek API 为源码生成 pytest 测试。

用法（本地开发 / mock 模式，不需要 API Key）：
    python scripts/write_tests.py --source src/calculator.py --dry-run

用法（真实调用，需要 DEEPSEEK_API_KEY 环境变量）：
    python scripts/write_tests.py --source src/calculator.py

GitHub Actions 中由 workflow 自动调用，从变更文件列表生成测试。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

# DeepSeek API 兼容 OpenAI 格式
API_URL = "https://api.deepseek.com/chat/completions"
MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

SYSTEM_PROMPT = """你是一位资深的 Python 测试工程师。根据用户提供的源码文件，
编写高质量的 pytest 单元测试。要求：
1. 只输出合法的 Python 代码，放在 ```python 代码块中，不要输出任何解释文字。
2. 覆盖正常路径、边界条件和异常路径。
3. 使用 pytest 风格（普通 assert + pytest.raises），不要依赖 unittest。
4. 测试函数以 test_ 开头。
5. 通过 from src.xxx import ... 或 from xxx import ... 导入被测模块（保持与源码相同的包路径）。
6. 不要 mock 掉被测函数本身，测试要真实执行逻辑。"""


def read_source(path: Path) -> str:
    if not path.exists():
        sys.exit(f"Error: source file not found: {path}")
    return path.read_text(encoding="utf-8")


def infer_test_path(source_path: Path) -> Path:
    """src/foo/bar.py -> tests/test_bar.py"""
    name = source_path.stem
    return Path("tests") / f"test_{name}.py"


def extract_python(text: str) -> str:
    """从模型回复中提取第一个 ```python 代码块；没有代码块则返回原文。"""
    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    return match.group(1).strip() if match else text.strip()


def call_deepseek(source_code: str, api_key: str) -> str:
    """调用 DeepSeek API 生成测试代码。"""
    import urllib.request

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"源码文件内容如下：\n\n```python\n{source_code}\n```"},
        ],
        "temperature": 0.2,
        "max_tokens": 4096,
        "stream": False,
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]


def main() -> int:
    parser = argparse.ArgumentParser(description="AI 单元测试生成器")
    parser.add_argument("--source", required=True, help="源码文件路径，如 src/calculator.py")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="不调用 API，输出 mock 测试（用于本地无 Key 验证流程）",
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    source_code = read_source(source_path)
    test_path = infer_test_path(source_path)

    if args.dry_run:
        print(f"[dry-run] 将为 {source_path} 生成测试 -> {test_path}")
        print("[dry-run] 请配置 DEEPSEEK_API_KEY 后去掉 --dry-run 真实运行")
        return 0

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        sys.exit(
            "Error: 环境变量 DEEPSEEK_API_KEY 未设置。"
            "本地运行请先 export/set DEEPSEEK_API_KEY=sk-xxx，"
            "GitHub Actions 中会自动从 Secrets 注入。"
        )

    print(f"[ai-test-writer] 正在让 {MODEL} 分析 {source_path} ...")
    reply = call_deepseek(source_code, api_key)
    generated = extract_python(reply)

    test_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.write_text(generated + "\n", encoding="utf-8")
    print(f"[ai-test-writer] ✅ 测试已写入 {test_path} ({len(generated)} 字符)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
