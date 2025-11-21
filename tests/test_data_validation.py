"""
データ検証のテストモジュール
入力データの検証機能のテストケース
"""
import pytest
import re


def validate_email(email: str) -> bool:
    """メールアドレスの形式を検証"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """電話番号の形式を検証（日本の形式）"""
    # 固定電話: 0X-XXXX-XXXX または 0XX-XXX-XXXX
    # 携帯電話: 090-XXXX-XXXX, 080-XXXX-XXXX, 070-XXXX-XXXX
    import re
    # ハイフン区切りまたはハイフンなし
    pattern = r'^(0\d{1,4}-\d{1,4}-\d{4}|0\d{9,10})$'
    if not re.match(pattern, phone):
        return False
    # 数字のみの場合は10桁または11桁
    digits_only = phone.replace('-', '')
    return len(digits_only) in [10, 11]


def validate_age(age: int) -> bool:
    """年齢の妥当性を検証"""
    return 0 <= age <= 150


def validate_password_strength(password: str) -> str:
    """パスワードの強度を評価"""
    if len(password) < 6:
        return "弱い"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    strength_score = sum([has_upper, has_lower, has_digit, has_special])
    
    # 強い: 4種類全て含み、10文字以上
    if strength_score >= 4 and len(password) >= 10:
        return "強い"
    # 強い: 3種類以上含み、12文字以上
    elif strength_score >= 3 and len(password) >= 12:
        return "強い"
    # 普通: 3種類以上含む
    elif strength_score >= 3:
        return "普通"
    # 普通: 2種類以上含み、8文字以上
    elif strength_score >= 2 and len(password) >= 8:
        return "普通"
    else:
        return "弱い"


@pytest.mark.category("Data Validation")
class TestEmailValidation:
    """メール検証のテストクラス"""
    
    def test_valid_emails(self):
        """有効なメールアドレスのテスト"""
        assert validate_email("test@example.com") == True
        assert validate_email("user.name@domain.co.jp") == True
        assert validate_email("admin+tag@test-domain.com") == True
    
    def test_invalid_emails(self):
        """無効なメールアドレスのテスト"""
        assert validate_email("invalid.email") == False
        assert validate_email("@example.com") == False
        assert validate_email("user@") == False
        assert validate_email("user @example.com") == False


@pytest.mark.category("Data Validation")
class TestPhoneValidation:
    """電話番号検証のテストクラス"""
    
    def test_valid_phones(self):
        """有効な電話番号のテスト"""
        assert validate_phone("090-1234-5678") == True
        assert validate_phone("09012345678") == True
        assert validate_phone("03-1234-5678") == True
    
    def test_invalid_phones(self):
        """無効な電話番号のテスト"""
        assert validate_phone("123-4567") == False
        assert validate_phone("abc-defg-hijk") == False


@pytest.mark.category("Data Validation")
class TestAgeValidation:
    """年齢検証のテストクラス"""
    
    def test_valid_ages(self):
        """有効な年齢のテスト"""
        assert validate_age(0) == True
        assert validate_age(25) == True
        assert validate_age(100) == True
        assert validate_age(150) == True
    
    def test_invalid_ages(self):
        """無効な年齢のテスト"""
        assert validate_age(-1) == False
        assert validate_age(151) == False
        assert validate_age(999) == False


@pytest.mark.category("Data Validation")
class TestPasswordStrength:
    """パスワード強度のテストクラス"""
    
    def test_weak_passwords(self):
        """弱いパスワードのテスト"""
        assert validate_password_strength("123") == "弱い"
        assert validate_password_strength("abc") == "弱い"
        assert validate_password_strength("simple") == "弱い"
    
    def test_medium_passwords(self):
        """普通のパスワードのテスト"""
        assert validate_password_strength("Password123") == "普通"
        assert validate_password_strength("test1234") == "普通"
    
    def test_strong_passwords(self):
        """強いパスワードのテスト"""
        assert validate_password_strength("StrongP@ss123") == "強い"
        assert validate_password_strength("MyP@ssw0rd!2024") == "強い"
    
    @pytest.mark.skip(reason="機能実装予定")
    def test_future_validation(self):
        """将来実装予定の検証テスト"""
        # このテストは実装予定のためスキップ
        pass
