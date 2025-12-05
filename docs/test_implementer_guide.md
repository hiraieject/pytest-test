# テストスクリプト実装者向けドキュメント

## 概要

このドキュメントは、pytest を使用したテストスクリプトを実装する開発者向けの説明書です。

## テストスクリプトの作成方法

### 1. 基本構造

テストスクリプトは `tests/` フォルダに配置します。ファイル名は `test_` で始める必要があります。

```python
"""
テストモジュールの説明
"""
import pytest

# テスト対象の関数を実装
def target_function(x, y):
    return x + y

# テストクラスを定義（クラス名は Test で始める）
@pytest.mark.category("カテゴリ名")
class TestExample:
    """テストクラスの説明"""
    
    @pytest.mark.test_id("TC001")
    def test_example_case(self):
        """テストケースの説明"""
        assert target_function(1, 2) == 3
```

### 2. テスト番号の指定

テンプレートファイル（`template/test_template.xlsx`）のテスト番号と対応させるために、`@pytest.mark.test_id()` デコレータを使用します。

```python
@pytest.mark.test_id("TC001")
def test_add_positive_numbers(self):
    """正の数の加算テスト"""
    assert add(2, 3) == 5
```

**重要事項:**
- `test_id` に指定する値は、テンプレートファイルの「テスト番号」列の値と完全に一致させてください
- `test_id` を指定しないテストは、テンプレートファイルに記録されません（詳細レポートのみに記録されます）
- **複数のテストで同じ `test_id` を使用可能**: 関連するテストケースを1つのテスト仕様にまとめる場合に便利です
  - 例: TC002に加算と減算の両方をマッピングする場合、どちらかが失敗すればNG、両方成功すればOKとなります
  - 最後に実行されたテストの結果が記録されます

### 3. カテゴリの指定

テスト結果を分類するために、`@pytest.mark.category()` デコレータを使用します。

```python
@pytest.mark.category("Calculation")
class TestCalculation:
    """計算機能のテストクラス"""
    pass
```

カテゴリを指定しない場合は、ファイル名から自動的に推測されます。

### 4. テンプレートファイルへの対応

#### 4.1 テンプレートファイルの編集

1. `template/test_template.xlsx` を開く
2. 3行目がヘッダー行（変更不可）
3. 4行目以降にテストケースを追加:
   - **テスト番号**: TC001, TC002, ... のような一意の識別子
   - **テスト分類１**: 大分類（例: 計算、文字列、リスト）
   - **テスト分類２**: 小分類（例: 加算、減算、乗算）
   - **テスト手順**: テストで実行する操作の説明
   - **期待値**: 期待される結果の説明
   - **テスト実施日付**: 空欄（自動記入）
   - **テスト結果**: 空欄（自動記入）
   - **テスト結果補足**: 空欄（自動記入）

#### 4.2 テストスクリプトの実装

テンプレートファイルのテスト番号に対応するテストを実装します:

```python
import pytest

@pytest.mark.category("計算")
class TestCalculation:
    
    @pytest.mark.test_id("TC001")  # テンプレートのTC001に対応
    def test_add(self):
        """加算テスト"""
        assert 2 + 3 == 5
    
    @pytest.mark.test_id("TC002")  # テンプレートのTC002に対応
    def test_subtract(self):
        """減算テスト"""
        assert 10 - 3 == 7
```

### 5. テスト失敗時の情報

テストが失敗した場合、エラーの詳細情報が自動的にテンプレートファイルの「テスト結果補足」列に記録されます。

デバッグしやすいように、適切なアサーションメッセージを記述することを推奨します:

```python
def test_example(self):
    result = calculate(10, 5)
    assert result == 15, f"期待値15だが実際は{result}でした"
```

### 6. 複数のアサーションを持つテスト

1つのテストケースで複数の条件を検証する場合、すべてのアサーションが成功すればOK、1つでも失敗すればNGとして記録されます。

```python
@pytest.mark.test_id("TC001")
def test_multiple_conditions(self):
    """複数条件のテスト"""
    assert add(2, 3) == 5
    assert add(10, 20) == 30
    assert add(-5, -3) == -8
```

### 7. 例外を期待するテスト

エラーが発生することを期待するテストの場合、`pytest.raises()` を使用します:

```python
@pytest.mark.test_id("TC005")
def test_divide_by_zero(self):
    """ゼロ除算のテスト"""
    with pytest.raises(ValueError, match="ゼロで除算することはできません"):
        divide(10, 0)
```

このテストは、指定した例外が発生すればOK（passed）となります。

### 8. テストのスキップ

特定の条件下でテストをスキップする場合:

```python
@pytest.mark.skip(reason="機能実装予定")
def test_future_feature(self):
    """未実装機能のテスト"""
    pass
```

スキップされたテストは、テンプレートファイルに「SKIP」として記録されます。

## 設定ファイル

`conf/config.yaml` でテスト実行の設定を変更できます:

```yaml
# テンプレートファイル設定
template_file: "test_template.xlsx"  # template/ フォルダ内のファイル名

# 出力ファイル設定
output_file: "test_results.xlsx"  # output/ フォルダ内のファイル名
output_sheet: "テスト結果"  # 出力シート名

# テスト情報
rom_version: "v0.0"  # ターゲットROMバージョン
tester_name: ""  # テスト実施者氏名
```

## ディレクトリ構造

```
pytest-test/
├── template/               # テンプレートファイル格納フォルダ
│   └── test_template.xlsx  # テスト仕様書兼結果ファイルの雛形
├── conf/                   # 設定ファイル格納フォルダ
│   └── config.yaml         # テスト実行設定
├── tests/                  # テストスクリプト格納フォルダ
│   ├── test_*.py           # テストスクリプト
├── testlib/                # テスト実行サポートライブラリ
│   ├── config_manager.py   # 設定管理
│   └── excel_manager.py    # Excel操作
├── output/                 # 出力フォルダ
│   ├── test_results.xlsx   # テンプレートベースの結果ファイル
│   ├── test_results_*.xlsx # 詳細レポート
│   └── test_execution_*.log # 実行ログ
├── conftest.py             # pytest設定
└── pytest.ini              # pytestマーカー定義
```

## トラブルシューティング

### テスト番号が見つからない

```
テスト番号 'TC999' がテンプレートに見つかりません。スキップします。
```

→ テンプレートファイルの「テスト番号」列に該当するテスト番号が存在するか確認してください。

### 設定ファイルが見つからない

```
設定ファイルが見つかりません: conf/config.yaml
```

→ `conf/config.yaml` が存在するか確認してください。

### テンプレートファイルが見つからない

```
テンプレートファイルが見つかりません: template/test_template.xlsx
```

→ `template/` フォルダにテンプレートファイルが存在するか、`conf/config.yaml` の設定が正しいか確認してください。

## ベストプラクティス

1. **テスト番号の一意性**: 各テストには一意のテスト番号を割り当てる
2. **わかりやすいテスト名**: テスト関数名は何をテストしているか明確に
3. **適切なカテゴリ分類**: 関連するテストは同じカテゴリにまとめる
4. **詳細なエラーメッセージ**: デバッグしやすいアサーションメッセージを記述
5. **独立したテスト**: 各テストは他のテストに依存しないように実装

## 参考情報

- pytest公式ドキュメント: https://docs.pytest.org/
- Python公式ドキュメント: https://docs.python.org/ja/3/
