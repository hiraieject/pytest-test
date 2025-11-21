"""
計算機能のテストモジュール
基本的な算術演算のテストケース
"""
import pytest


def add(a, b):
    """加算"""
    return a + b


def subtract(a, b):
    """減算"""
    return a - b


def multiply(a, b):
    """乗算"""
    return a * b


def divide(a, b):
    """除算"""
    if b == 0:
        raise ValueError("ゼロで除算することはできません")
    return a / b


@pytest.mark.category("Calculation")
class TestBasicCalculation:
    """基本計算のテストクラス"""
    
    def test_add_positive_numbers(self):
        """正の数の加算テスト"""
        assert add(2, 3) == 5
        assert add(10, 20) == 30
    
    def test_add_negative_numbers(self):
        """負の数の加算テスト"""
        assert add(-5, -3) == -8
        assert add(-10, 5) == -5
    
    def test_subtract_positive_numbers(self):
        """正の数の減算テスト"""
        assert subtract(10, 3) == 7
        assert subtract(20, 5) == 15
    
    def test_subtract_negative_numbers(self):
        """負の数の減算テスト"""
        assert subtract(-5, -3) == -2
        assert subtract(5, -3) == 8
    
    def test_multiply_numbers(self):
        """乗算テスト"""
        assert multiply(3, 4) == 12
        assert multiply(-2, 5) == -10
        assert multiply(0, 100) == 0
    
    def test_divide_numbers(self):
        """除算テスト"""
        assert divide(10, 2) == 5
        assert divide(15, 3) == 5
        assert divide(7, 2) == 3.5
    
    def test_divide_by_zero(self):
        """ゼロ除算のテスト"""
        with pytest.raises(ValueError, match="ゼロで除算することはできません"):
            divide(10, 0)
    
    def test_complex_calculation(self):
        """複合計算のテスト"""
        result = add(multiply(3, 4), divide(10, 2))
        assert result == 17


@pytest.mark.category("Calculation")
class TestAdvancedCalculation:
    """高度な計算のテストクラス"""
    
    def test_large_numbers(self):
        """大きな数値の計算テスト"""
        assert add(1000000, 2000000) == 3000000
        assert multiply(1000, 1000) == 1000000
    
    def test_floating_point_precision(self):
        """浮動小数点の精度テスト"""
        result = add(0.1, 0.2)
        assert abs(result - 0.3) < 0.0001
    
    def test_edge_cases(self):
        """エッジケースのテスト"""
        assert add(0, 0) == 0
        assert multiply(1, 999999) == 999999
