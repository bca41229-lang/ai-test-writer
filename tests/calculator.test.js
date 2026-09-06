// 本测试由 AI Test Writer 自动生成 (Jest)

const {
  add,
  subtract,
  multiply,
  divide,
  isEven,
  factorial,
  power
} = require('../src/calculator.js');

describe('Calculator Utility Functions', () => {
  // ========== add() tests ==========
  describe('add()', () => {
    it('should correctly add two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('should correctly add positive and negative numbers', () => {
      expect(add(5, -3)).toBe(2);
    });

    it('should correctly add two negative numbers', () => {
      expect(add(-2, -3)).toBe(-5);
    });

    it('should correctly add floating point numbers', () => {
      expect(add(0.1, 0.2)).toBeCloseTo(0.3);
    });

    it('should correctly add zero', () => {
      expect(add(0, 0)).toBe(0);
      expect(add(5, 0)).toBe(5);
    });

    it('should handle large numbers', () => {
      expect(add(Number.MAX_SAFE_INTEGER, 1)).toBe(Number.MAX_SAFE_INTEGER + 1);
    });
  });

  // ========== subtract() tests ==========
  describe('subtract()', () => {
    it('should correctly subtract two positive numbers', () => {
      expect(subtract(5, 3)).toBe(2);
    });

    it('should correctly subtract resulting in negative', () => {
      expect(subtract(3, 5)).toBe(-2);
    });

    it('should correctly subtract negative numbers', () => {
      expect(subtract(-5, -3)).toBe(-2);
    });

    it('should correctly subtract floating point numbers', () => {
      expect(subtract(0.3, 0.1)).toBeCloseTo(0.2);
    });

    it('should correctly subtract zero', () => {
      expect(subtract(5, 0)).toBe(5);
      expect(subtract(0, 5)).toBe(-5);
    });
  });

  // ========== multiply() tests ==========
  describe('multiply()', () => {
    it('should correctly multiply two positive numbers', () => {
      expect(multiply(4, 3)).toBe(12);
    });

    it('should correctly multiply positive and negative numbers', () => {
      expect(multiply(4, -3)).toBe(-12);
    });

    it('should correctly multiply two negative numbers', () => {
      expect(multiply(-4, -3)).toBe(12);
    });

    it('should correctly multiply by zero', () => {
      expect(multiply(5, 0)).toBe(0);
      expect(multiply(0, 5)).toBe(0);
    });

    it('should correctly multiply floating point numbers', () => {
      expect(multiply(0.5, 0.5)).toBeCloseTo(0.25);
    });

    it('should handle large numbers', () => {
      expect(multiply(1000000, 1000000)).toBe(1000000000000);
    });
  });

  // ========== divide() tests ==========
  describe('divide()', () => {
    it('should correctly divide two positive numbers', () => {
      expect(divide(10, 2)).toBe(5);
    });

    it('should correctly divide positive by negative', () => {
      expect(divide(10, -2)).toBe(-5);
    });

    it('should correctly divide negative by negative', () => {
      expect(divide(-10, -2)).toBe(5);
    });

    it('should correctly divide floating point numbers', () => {
      expect(divide(1, 3)).toBeCloseTo(0.3333333333);
    });

    it('should correctly divide resulting in decimal', () => {
      expect(divide(7, 2)).toBe(3.5);
    });

    it('should throw error when dividing by zero', () => {
      expect(() => divide(10, 0)).toThrow('division by zero');
    });

    it('should throw error when dividing zero by zero', () => {
      expect(() => divide(0, 0)).toThrow('division by zero');
    });

    it('should correctly divide zero by non-zero number', () => {
      expect(divide(0, 5)).toBe(0);
    });

    it('should handle division of negative zero', () => {
      expect(divide(-0, 5)).toBe(-0);
    });
  });

  // ========== isEven() tests ==========
  describe('isEven()', () => {
    it('should return true for even positive numbers', () => {
      expect(isEven(2)).toBe(true);
      expect(isEven(4)).toBe(true);
      expect(isEven(100)).toBe(true);
    });

    it('should return false for odd positive numbers', () => {
      expect(isEven(1)).toBe(false);
      expect(isEven(3)).toBe(false);
      expect(isEven(99)).toBe(false);
    });

    it('should return true for even negative numbers', () => {
      expect(isEven(-2)).toBe(true);
      expect(isEven(-4)).toBe(true);
    });

    it('should return false for odd negative numbers', () => {
      expect(isEven(-1)).toBe(false);
      expect(isEven(-3)).toBe(false);
    });

    it('should return true for zero', () => {
      expect(isEven(0)).toBe(true);
    });

    it('should handle large even numbers', () => {
      expect(isEven(1000000)).toBe(true);
    });

    it('should handle large odd numbers', () => {
      expect(isEven(1000001)).toBe(false);
    });
  });

  // ========== factorial() tests ==========
  describe('factorial()', () => {
    it('should return 1 for factorial of 0', () => {
      expect(factorial(0)).toBe(1);
    });

    it('should return 1 for factorial of 1', () => {
      expect(factorial(1)).toBe(1);
    });

    it('should correctly calculate factorial of positive numbers', () => {
      expect(factorial(2)).toBe(2);
      expect(factorial(3)).toBe(6);
      expect(factorial(4)).toBe(24);
      expect(factorial(5)).toBe(120);
    });

    it('should correctly calculate factorial of 10', () => {
      expect(factorial(10)).toBe(3628800);
    });

    it('should throw error for negative numbers', () => {
      expect(() => factorial(-1)).toThrow('factorial of negative number');
      expect(() => factorial(-100)).toThrow('factorial of negative number');
    });

    it('should handle factorial of 20 (large number)', () => {
      expect(factorial(20)).toBe(2432902008176640000);
    });
  });

  // ========== power() tests ==========
  describe('power()', () => {
    it('should correctly calculate power with positive exponent', () => {
      expect(power(2, 3)).toBe(8);
      expect(power(3, 2)).toBe(9);
      expect(power(5, 0)).toBe(1);
    });

    it('should return 1 for exponent 0', () => {
      expect(power(10, 0)).toBe(1);
      expect(power(0, 0)).toBe(1);
    });

    it('should correctly calculate power with base 0', () => {
      expect(power(0, 5)).toBe(0);
    });

    it('should correctly calculate power with negative base', () => {
      expect(power(-2, 3)).toBe(-8);
      expect(power(-2, 2)).toBe(4);
    });

    it('should correctly calculate power with floating point base', () => {
      expect(power(0.5, 2)).toBeCloseTo(0.25);
    });

    it('should throw error for negative exponent', () => {
      expect(() => power(2, -1)).toThrow('negative exponent not supported');
      expect(() => power(2, -3)).toThrow('negative exponent not supported');
    });

    it('should handle large numbers', () => {
      expect(power(10, 10)).toBe(10000000000);
    });

    it('should handle exponent 1', () => {
      expect(power(7, 1)).toBe(7);
    });
  });
});
