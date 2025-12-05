"""
リスト操作のテストモジュール
リストに関する機能のテストケース
"""
import pytest


def find_max(numbers: list):
    """リストの最大値を取得"""
    if not numbers:
        raise ValueError("空のリストです")
    return max(numbers)


def find_min(numbers: list):
    """リストの最小値を取得"""
    if not numbers:
        raise ValueError("空のリストです")
    return min(numbers)


def calculate_average(numbers: list) -> float:
    """リストの平均値を計算"""
    if not numbers:
        raise ValueError("空のリストです")
    return sum(numbers) / len(numbers)


def remove_duplicates(items: list) -> list:
    """重複を削除"""
    return list(dict.fromkeys(items))


def sort_list(items: list, reverse: bool = False) -> list:
    """リストをソート"""
    return sorted(items, reverse=reverse)


@pytest.mark.category("List Operations")
class TestListBasics:
    """リスト基本操作のテストクラス"""
    
    @pytest.mark.test_id("TC010")
    def test_find_max(self):
        """最大値検索のテスト"""
        assert find_max([1, 5, 3, 9, 2]) == 9
        assert find_max([10]) == 10
        assert find_max([-5, -1, -10]) == -1
    
    @pytest.mark.test_id("TC011")
    def test_find_min(self):
        """最小値検索のテスト"""
        assert find_min([1, 5, 3, 9, 2]) == 1
        assert find_min([10]) == 10
        assert find_min([-5, -1, -10]) == -10
    
    @pytest.mark.test_id("TC012")
    def test_calculate_average(self):
        """平均値計算のテスト"""
        assert calculate_average([1, 2, 3, 4, 5]) == 3.0
        assert calculate_average([10, 20, 30]) == 20.0
        assert calculate_average([100]) == 100.0
    
    def test_empty_list_max(self):
        """空リストの最大値テスト"""
        with pytest.raises(ValueError, match="空のリストです"):
            find_max([])
    
    def test_empty_list_average(self):
        """空リストの平均値テスト"""
        with pytest.raises(ValueError, match="空のリストです"):
            calculate_average([])


@pytest.mark.category("List Operations")
class TestListManipulation:
    """リスト操作のテストクラス"""
    
    @pytest.mark.test_id("TC013")
    def test_remove_duplicates(self):
        """重複削除のテスト"""
        assert remove_duplicates([1, 2, 2, 3, 3, 3]) == [1, 2, 3]
        assert remove_duplicates([1, 1, 1, 1]) == [1]
        assert remove_duplicates([1, 2, 3]) == [1, 2, 3]
    
    def test_sort_ascending(self):
        """昇順ソートのテスト"""
        assert sort_list([3, 1, 4, 1, 5, 9]) == [1, 1, 3, 4, 5, 9]
        assert sort_list([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    
    def test_sort_descending(self):
        """降順ソートのテスト"""
        assert sort_list([3, 1, 4, 1, 5, 9], reverse=True) == [9, 5, 4, 3, 1, 1]
    
    def test_list_comprehension(self):
        """リスト内包表記のテスト"""
        numbers = [1, 2, 3, 4, 5]
        squared = [x**2 for x in numbers]
        assert squared == [1, 4, 9, 16, 25]
    
    def test_list_filtering(self):
        """リストフィルタリングのテスト"""
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        even_numbers = [x for x in numbers if x % 2 == 0]
        assert even_numbers == [2, 4, 6, 8, 10]


@pytest.mark.category("List Operations")
class TestListEdgeCases:
    """リストのエッジケーステストクラス"""
    
    def test_single_element_list(self):
        """単一要素リストのテスト"""
        assert find_max([42]) == 42
        assert find_min([42]) == 42
        assert calculate_average([42]) == 42.0
    
    def test_negative_numbers(self):
        """負の数のリストテスト"""
        assert find_max([-1, -5, -3]) == -1
        assert calculate_average([-2, -4, -6]) == -4.0
