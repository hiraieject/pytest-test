"""
文字列処理のテストモジュール
文字列操作機能のテストケース
"""
import pytest


def reverse_string(s: str) -> str:
    """文字列を反転"""
    return s[::-1]


def capitalize_words(s: str) -> str:
    """各単語の先頭を大文字に"""
    return s.title()


def count_vowels(s: str) -> int:
    """母音の数をカウント"""
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)


def is_palindrome(s: str) -> bool:
    """回文かどうかをチェック"""
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


@pytest.mark.category("String Processing")
class TestStringOperations:
    """文字列操作のテストクラス"""
    
    def test_reverse_string(self):
        """文字列反転のテスト"""
        assert reverse_string("hello") == "olleh"
        assert reverse_string("Python") == "nohtyP"
        assert reverse_string("") == ""
    
    def test_capitalize_words(self):
        """単語の大文字化テスト"""
        assert capitalize_words("hello world") == "Hello World"
        assert capitalize_words("python programming") == "Python Programming"
    
    def test_count_vowels(self):
        """母音カウントのテスト"""
        assert count_vowels("hello") == 2
        assert count_vowels("AEIOU") == 5
        assert count_vowels("xyz") == 0
        assert count_vowels("beautiful") == 5
    
    def test_palindrome_simple(self):
        """単純な回文テスト"""
        assert is_palindrome("racecar") == True
        assert is_palindrome("hello") == False
        assert is_palindrome("A") == True
    
    def test_palindrome_with_spaces(self):
        """スペース含む回文テスト"""
        assert is_palindrome("A man a plan a canal Panama") == True
        assert is_palindrome("race a car") == False
    
    def test_empty_string(self):
        """空文字列のテスト"""
        assert reverse_string("") == ""
        assert count_vowels("") == 0
        assert is_palindrome("") == True


@pytest.mark.category("String Processing")
class TestStringValidation:
    """文字列検証のテストクラス"""
    
    def test_string_length(self):
        """文字列の長さテスト"""
        text = "Hello, World!"
        assert len(text) == 13
    
    def test_string_contains(self):
        """文字列の包含テスト"""
        text = "Python is awesome"
        assert "Python" in text
        assert "Java" not in text
    
    def test_string_startswith(self):
        """文字列の開始テスト"""
        text = "Hello World"
        assert text.startswith("Hello")
        assert not text.startswith("World")
