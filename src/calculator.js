// 示例业务模块：计算器工具集（JavaScript 版）
// 这是多语言 AI 测试机器人的演示源码。

function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) throw new Error("division by zero");
  return a / b;
}

function isEven(n) {
  return n % 2 === 0;
}

function factorial(n) {
  if (n < 0) throw new Error("factorial of negative number");
  let result = 1;
  for (let i = 2; i <= n; i++) result *= i;
  return result;
}

module.exports = { add, subtract, multiply, divide, isEven, factorial };
