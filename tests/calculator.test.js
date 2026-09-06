// 本测试由 AI Test Writer 自动生成 (Jest)

const { add, subtract, multiply, divide, isEven, factorial } = require('./calculator');

describe('Calculator utility functions', () => {
  describe('add', () => {
    it('should correctly add two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    it('should correctly add negative numbers', () => {
      expect(add(-2, -3)).toBe(-5);
    });

    it('should handle decimal numbers', () => {
      expect(add(0.1, 0.2)).toBeCloseTo(0.3);
    });

    it('should handle zero', () => {
      expect(add(0, 5)).toBe(5);
      expect(add(0, 0)).toBe(0);
    });

    it('should handle large numbers', () => {
      expect(add(Number.MAX_SAFE_INTEGER, 1)).toBe(Number.MAX_SAFE_INTEGER + 1);
    });
  });

  describe('subtract', () => {
    it('should correctly subtract two positive numbers', () => {
      expect(subtract(5, 3)).toBe(2);
    });

    it('should handle negative results', () => {
      expect(subtract(3, 5)).toBe(-2);
    });

    it('should handle negative numbers', () => {
      expect(subtract(-5, -3)).toBe(-2);
    });

    it('should handle decimal numbers', () => {
      expect(subtract(0.3, 0.1)).toBeCloseTo(0.2);
    });

    it('should handle zero', () => {
      expect(subtract(5, 0)).toBe(5);
      expect(subtract(0, 5)).toBe(-5);
    });
  });

  describe('multiply', () => {
    it('should correctly multiply two positive numbers', () => {
      expect(multiply(4, 3)).toBe(12);
    });

    it('should handle negative numbers', () => {
      expect(multiply(-4, 3)).toBe(-12);
      expect(multiply(-4, -3)).toBe(12);
    });

    it('should handle decimal numbers', () => {
      expect(multiply(0.5, 0.5)).toBeCloseTo(0.25);
    });

    it('should handle zero', () => {
      expect(multiply(5, 0)).toBe(0);
      expect(multiply(0, 0)).toBe(0);
    });

    it('should handle large numbers', () => {
      expect(multiply(1000000, 1000000)).toBe(1000000000000);
    });
  });

  describe('divide', () => {
    it('should correctly divide two positive numbers', () => {
      expect(divide(10, 2)).toBe(5);
    });

    it('should handle negative numbers', () => {
      expect(divide(-10, 2)).toBe(-5);
      expect(divide(10, -2)).toBe(-5);
      expect(divide(-10, -2)).toBe(5);
    });

    it('should handle decimal results', () => {
      expect(divide(1, 3)).toBeCloseTo(0.3333);
    });

    it('should handle division by decimal', () => {
      expect(divide(1, 0.5)).toBe(2);
    });

    it('should throw error when dividing by zero', () => {
      expect(() => divide(10, 0)).toThrow('division by zero');
    });

    it('should handle zero divided by number', () => {
      expect(divide(0, 5)).toBe(0);
    });
  });

  describe('isEven', () => {
    it('should return true for even numbers', () => {
      expect(isEven(2)).toBe(true);
      expect(isEven(0)).toBe(true);
      expect(isEven(-4)).toBe(true);
    });

    it('should return false for odd numbers', () => {
      expect(isEven(3)).toBe(false);
      expect(isEven(-3)).toBe(false);
    });

    it('should handle large even numbers', () => {
      expect(isEven(1000000)).toBe(true);
    });

    it('should handle large odd numbers', () => {
      expect(isEven(1000001)).toBe(false);
    });
  });

  describe('factorial', () => {
    it('should return 1 for factorial of 0', () => {
      expect(factorial(0)).toBe(1);
    });

    it('should return 1 for factorial of 1', () => {
      expect(factorial(1)).toBe(1);
    });

    it('should correctly calculate factorial of positive numbers', () => {
      expect(factorial(5)).toBe(120);
      expect(factorial(10)).toBe(3628800);
    });

    it('should throw error for negative numbers', () => {
      expect(() => factorial(-1)).toThrow('factorial of negative number');
      expect(() => factorial(-10)).toThrow('factorial of negative number');
    });

    it('should handle large factorial values', () => {
      expect(factorial(20)).toBe(2432902008176640000);
    });

    it('should handle decimal input by truncating', () => {
      // Note: JavaScript will truncate decimal to integer in the loop
      expect(factorial(5.5)).toBe(120);
    });
  });
});
