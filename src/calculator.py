"""示例业务模块：计算器工具集。

这是 AI 测试机器人要分析的示例源码。真实使用时请把你的业务代码
放在 src/ 下，workflow 会自动为变更的文件生成测试。
"""


def add(a: float, b: float) -> float:
    """返回两个数的和。"""
    return a + b


def subtract(a: float, b: float) -> float:
    """返回 a - b。"""
    return a - b


def multiply(a: float, b: float) -> float:
    """返回两个数的积。"""
    return a * b


def divide(a: float, b: float) -> float:
    """返回 a / b；除数为零时抛出 ValueError。"""
    if b == 0:
        raise ValueError("division by zero")
    return a / b


def is_even(n: int) -> bool:
    """判断整数 n 是否为偶数。"""
    return n % 2 == 0


def factorial(n: int) -> int:
    """计算非负整数 n 的阶乘。"""
    if n < 0:
        raise ValueError("factorial of negative number")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def power(base: float, exponent: int) -> float:
    """计算 base 的 exponent 次幂（exponent 为非负整数）。"""
    if exponent < 0:
        raise ValueError("negative exponent not supported")
    return base ** exponent

# v0.1.1: 触发 AI 测试机器人（修复 DEEPSEEK_MODEL 回退）
