"""AI 单元测试生成器（多语言版）：调用 DeepSeek API 为源码生成单元测试。

自动按文件扩展名识别语言并选择测试框架：

    .py    -> pytest                .js    -> Jest
    .ts    -> Jest (ts-jest)        .java  -> JUnit 5
    .go    -> Go testing            .rs    -> cargo test
    .c/.cpp/.hpp -> GoogleTest

用法（本地开发 / mock 模式，不需要 API Key）：
    python scripts/write_tests.py --source src/calculator.js --dry-run

用法（真实调用，需要 DEEPSEEK_API_KEY 环境变量）：
    python scripts/write_tests.py --source src/calculator.js

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
MODEL = os.environ.get("DEEPSEEK_MODEL") or "deepseek-chat"

# ---------------------------------------------------------------- 语言配置表
# 每项：文件名模板（{stem}=模块名）、提示词要求、测试文件顶部附加注释
LANG_CONFIGS = {
    ".py": {
        "lang": "Python",
        "framework": "pytest",
        "file": "test_{stem}.py",
        "hint": (
            "使用 pytest 风格（普通 assert + pytest.raises），测试函数以 test_ 开头。"
            "通过 from src.模块名 import ... 导入被测模块。不要 mock 被测函数本身。"
        ),
        "header": "# 本测试由 AI Test Writer 自动生成 (pytest)",
    },
    ".js": {
        "lang": "JavaScript",
        "framework": "Jest",
        "file": "{stem}.test.js",
        "hint": (
            "使用 Jest 风格（describe/it/expect）。通过 require() 或 import 导入被测模块"
            "（路径相对测试文件所在目录）。覆盖正常、边界与异常路径。"
        ),
        "header": "// 本测试由 AI Test Writer 自动生成 (Jest)",
    },
    ".ts": {
        "lang": "TypeScript",
        "framework": "Jest + ts-jest",
        "file": "{stem}.test.ts",
        "hint": (
            "使用 Jest + ts-jest 风格（describe/it/expect + 类型标注）。"
            "通过 import 导入被测模块。覆盖正常、边界与异常路径。"
        ),
        "header": "// 本测试由 AI Test Writer 自动生成 (Jest + ts-jest)",
    },
    ".java": {
        "lang": "Java",
        "framework": "JUnit 5",
        "file": "Test{Stem}.java",
        "hint": (
            "使用 JUnit 5（@Test、org.junit.jupiter.api）。类名以 Test 结尾，"
            "方法以 test 开头。通过 import 导入被测类。不要用 main 方法。"
        ),
        "header": "// 本测试由 AI Test Writer 自动生成 (JUnit 5)",
    },
    ".go": {
        "lang": "Go",
        "framework": "Go testing",
        "file": "{stem}_test.go",
        "hint": (
            "使用 Go 标准 testing 包（func TestXxx(t *testing.T)）。"
            "测试文件需与源码同目录或同包，用包名 + . 导入被测函数。"
        ),
        "header": "// 本测试由 AI Test Writer 自动生成 (Go testing)",
    },
    ".rs": {
        "lang": "Rust",
        "framework": "cargo test (#[cfg(test)])",
        "file": "{stem}_test.rs",
        "hint": (
            "在被测模块文件内或 tests/ 下使用 #[cfg(test)] mod tests { ... }，"
            "用 assert_eq!/assert!。保持与源码相同的 crate 路径。"
        ),
        "header": "// 本测试由 AI Test Writer 自动生成 (cargo test)",
    },
    ".c": {
        "lang": "C",
        "framework": "GoogleTest (C++) 风格断言",
        "file": "test_{stem}.c",
        "hint": (
            "为 C 源码编写测试：包含被测头文件，编写一个 main 中运行的断言集"
            "（简单 assert 风格即可），不要引入复杂框架。"
        ),
        "header": "/* 本测试由 AI Test Writer 自动生成 */",
    },
    ".cpp": {
        "lang": "C++",
        "framework": "GoogleTest 或轻量断言",
        "file": "test_{stem}.cpp",
        "hint": (
            "为 C++ 源码编写测试：包含被测头文件，编写断言。"
            "若代码简单可用 assert，否则用 GoogleTest 的 TEST() 宏。"
        ),
        "header": "// 本测试由 AI Test Writer 自动生成 (C++)",
    },
    ".hpp": {
        "lang": "C++ header",
        "framework": "GoogleTest 或轻量断言",
        "file": "test_{stem}.cpp",
        "hint": (
            "为 C++ 头文件声明编写测试，include 该头文件后编写断言。"
        ),
        "header": "// 本测试由 AI Test Writer 自动生成 (C++)",
    },
}

SYSTEM_PROMPT_TEMPLATE = """你是一位资深的测试工程师。根据用户提供的 {lang} 源码文件，
编写高质量的单元测试。要求：
1. 只输出合法的 {lang} 代码，放在 ```{ext} 代码块中（或对应语言代码块），不要输出任何解释文字。
2. {hint}
3. 覆盖正常路径、边界条件和异常路径。
4. 不要在测试中修改被测源码。"""


def detect_config(path: Path) -> dict:
    """根据文件扩展名返回语言配置；不支持时报错退出。"""
    cfg = LANG_CONFIGS.get(path.suffix.lower())
    if cfg is None:
        supported = ", ".join(sorted(LANG_CONFIGS.keys()))
        sys.exit(f"Error: 不支持的文件类型 {path.suffix}（支持: {supported}）")
    return cfg


def read_source(path: Path) -> str:
    if not path.exists():
        sys.exit(f"Error: source file not found: {path}")
    return path.read_text(encoding="utf-8", errors="replace")


def infer_test_path(source_path: Path, cfg: dict) -> Path:
    """按语言模板生成测试路径：src/foo/bar.js -> tests/bar.test.js"""
    stem = source_path.stem
    # Java 类名首字母大写
    stem_cap = stem[:1].upper() + stem[1:]
    filename = cfg["file"].format(stem=stem, Stem=stem_cap)
    return Path("tests") / filename


def extract_code(text: str, cfg: dict) -> str:
    """从模型回复提取代码块；无代码块则返回原文（按语言去掉可能的围栏）。"""
    fence_langs = ["python", "javascript", "js", "typescript", "ts", "java", "go", "rust", "c", "cpp", "c++"]
    pattern = r"```(?:[a-zA-Z+]*)\s*\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # 兜底：若回复不含代码块，去掉 ``` 围栏
    cleaned = re.sub(r"```[a-zA-Z+]*", "", text)
    cleaned = re.sub(r"```", "", cleaned)
    return cleaned.strip()


def call_deepseek(source_code: str, api_key: str, cfg: dict, import_hint: str = "") -> str:
    """调用 DeepSeek API 生成测试代码。"""
    import urllib.request

    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        lang=cfg["lang"], ext=cfg["lang"].lower(), hint=cfg["hint"]
    )
    location_note = ""
    if import_hint:
        location_note = (
            f"\n\n[重要] 被测源码位于 {import_hint['source']}，生成的测试文件将写入 "
            f"{import_hint['test']}。请使用正确的相对导入路径引用被测模块"
            f"（如 JS/TS 的 require/import、Python 的 from ... import 等），"
            f"确保测试能真实运行。不要假设被测文件与测试文件在同一目录。"
        )
    user_msg = (
        f"源码文件内容如下：\n\n```\n{source_code}\n```{location_note}"
    )
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
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
    parser = argparse.ArgumentParser(description="AI 单元测试生成器（多语言版）")
    parser.add_argument("--source", help="源码文件路径，如 src/calculator.js")
    parser.add_argument("--list-langs", action="store_true", help="列出支持的语言并退出")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="不调用 API，仅输出将生成的目标（用于本地无 Key 验证流程）",
    )
    args = parser.parse_args()

    if args.list_langs:
        for ext, cfg in LANG_CONFIGS.items():
            print(f"{ext:<8} -> {cfg['lang']:<18} ({cfg['framework']})")
        return 0

    if not args.source:
        parser.error("--source 是必需的（或用 --list-langs 查看支持的语言）")

    source_path = Path(args.source)
    cfg = detect_config(source_path)
    source_code = read_source(source_path)
    test_path = infer_test_path(source_path, cfg)

    if args.dry_run:
        print(f"[dry-run] {source_path} ({cfg['lang']}) -> {test_path} [{cfg['framework']}]")
        print("[dry-run] 请配置 DEEPSEEK_API_KEY 后去掉 --dry-run 真实运行")
        return 0

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        sys.exit(
            "Error: 环境变量 DEEPSEEK_API_KEY 未设置。"
            "本地运行请先设置 DEEPSEEK_API_KEY=sk-xxx，"
            "GitHub Actions 中会自动从 Secrets 注入。"
        )

    print(f"[ai-test-writer] 正在让 {MODEL} 分析 {source_path} ({cfg['lang']}) ...")
    import_hint = {
        "source": str(source_path),
        "test": str(test_path),
    }
    reply = call_deepseek(source_code, api_key, cfg, import_hint=import_hint)
    generated = extract_code(reply, cfg)

    test_path.parent.mkdir(parents=True, exist_ok=True)
    body = f"{cfg['header']}\n\n{generated}\n"
    test_path.write_text(body, encoding="utf-8")
    print(f"[ai-test-writer] ✅ 测试已写入 {test_path} ({len(generated)} 字符)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
