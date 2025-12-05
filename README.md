# pytest テスト自動化プロジェクト

このプロジェクトは、pytest を使用したテストの実装例と、テスト結果を Excel ファイルに出力する機能を提供します。

## 機能

- ✅ pytest を使用した複数のテストケース
- 📋 テンプレートベースのテスト仕様書兼結果ファイル
- 📊 テスト結果の自動 Excel 出力（2種類のレポート）
- 📝 実行ログの記録
- 🏷️ カテゴリ別のテスト結果管理
- ⚙️ YAML 形式の設定ファイル

## プロジェクト構成

```
pytest-test/
├── template/                   # テンプレートファイル格納フォルダ
│   └── test_template.xlsx      # テスト仕様書兼結果ファイルの雛形
├── conf/                       # 設定ファイル格納フォルダ
│   └── config.yaml             # テスト実行設定（ROMバージョン、実施者名など）
├── tests/                      # テストファイル格納フォルダ
│   ├── test_calculation.py     # 計算機能のテスト
│   ├── test_string_processing.py  # 文字列処理のテスト
│   ├── test_list_operations.py    # リスト操作のテスト
│   └── test_data_validation.py    # データ検証のテスト
├── testlib/                    # テスト実行サポートライブラリ
│   ├── __init__.py
│   ├── config_manager.py       # 設定管理モジュール
│   └── excel_manager.py        # テンプレートベースExcel管理モジュール
├── output/                     # 出力フォルダ（Excel、ログ）
│   ├── test_results.xlsx       # テンプレートベースの結果ファイル
│   ├── test_results_*.xlsx     # 詳細レポート（実行ごとに生成）
│   └── test_execution_*.log    # 実行ログファイル
├── docs/                       # ドキュメント
│   ├── test_implementer_guide.md  # テストスクリプト実装者向けガイド
│   └── test_operator_guide.md     # テスト実施者向けガイド
├── conftest.py                 # pytest 設定ファイル
├── excel_reporter.py           # Excel レポート生成モジュール
├── logger_config.py            # ロギング設定モジュール
├── pytest.ini                  # pytest マーカー定義
├── requirements.txt            # 依存パッケージ
└── README.md                   # このファイル
```

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. 設定ファイルの編集

テスト実施前に `conf/config.yaml` を編集して必要な情報を入力します:

```yaml
# テンプレートファイル設定
template_file: "test_template.xlsx"

# 出力ファイル設定
output_file: "test_results.xlsx"
output_sheet: "テスト結果"

# テスト情報
rom_version: "v0.0"  # ターゲットROMバージョン（必ず変更してください）
tester_name: ""  # テスト実施者氏名（任意）
```

### 3. テストの実行

全てのテストを実行する場合:

```bash
pytest
```

特定のテストファイルを実行する場合:

```bash
pytest tests/test_calculation.py
```

詳細な出力で実行する場合:

```bash
pytest -v
```

## 出力ファイル

テスト実行後、`output` フォルダに以下のファイルが生成されます:

### 1. テンプレートベースの結果ファイル（output/test_results.xlsx）

テンプレートファイルに基づいて作成される、メインの結果ファイルです。

**構成:**
- **1行目**: ターゲットROMバージョン（設定ファイルから自動記入）
- **3行目**: ヘッダー行
  - テスト番号、テスト分類１、テスト分類２、テスト手順、期待値、テスト実施日付、テスト結果、テスト結果補足
- **4行目以降**: テストケースと結果
  - テスト実施日付: テスト実行日（月/日形式）が自動記入
  - テスト結果: OK/NG/SKIP が自動記入
  - テスト結果補足: NG の場合、エラー詳細が自動記入

**特徴:**
- 初回実行時にテンプレートファイルからコピーされて作成
- 2回目以降は既存ファイルを更新（上書き）
- `@pytest.mark.test_id()` が設定されたテストのみが記録される

### 2. 詳細レポート（output/test_results_YYYYMMDD_HHMMSS.xlsx）

実行ごとに生成される詳細なレポートファイルです。

1. **Summary シート**: テスト実行の統計情報
   - 総テスト数
   - 成功/失敗/スキップの件数と割合
   - 実行日時

2. **カテゴリ別シート**: 各カテゴリごとの詳細結果
   - Calculation（計算機能）
   - String Processing（文字列処理）
   - List Operations（リスト操作）
   - Data Validation（データ検証）

3. **All Tests シート**: 全テストの詳細結果
   - テスト名
   - カテゴリ
   - 結果（成功/失敗/スキップ）
   - 実行時間
   - エラーメッセージ

### 3. ログファイル（output/test_execution_*.log）

テスト実行の詳細ログが記録されます:
- 各テストの開始/終了
- 成功/失敗の情報
- エラー詳細
- 実行時刻

## テストの記述方法

### カテゴリの設定

テストにカテゴリを設定するには、`@pytest.mark.category()` デコレータを使用します:

```python
import pytest

@pytest.mark.category("Custom Category")
class TestExample:
    def test_something(self):
        assert True
```

カテゴリを指定しない場合、ファイル名から自動的に推測されます。

### テスト番号の設定

テンプレートファイルのテスト番号と対応させるには、`@pytest.mark.test_id()` デコレータを使用します:

```python
import pytest

@pytest.mark.category("Calculation")
class TestCalculation:
    
    @pytest.mark.test_id("TC001")
    def test_add(self):
        """加算テスト"""
        assert 2 + 3 == 5
    
    @pytest.mark.test_id("TC002")
    def test_subtract(self):
        """減算テスト"""
        assert 10 - 3 == 7
```

**重要:**
- `test_id` に指定する値は、テンプレートファイルの「テスト番号」列の値と完全に一致させる必要があります
- `test_id` を指定しないテストは、詳細レポートにのみ記録されます

## ドキュメント

詳細なガイドは `docs/` フォルダを参照してください:

- **[テストスクリプト実装者向けガイド](docs/test_implementer_guide.md)**
  - テストスクリプトの書き方
  - テスト番号の指定方法
  - テンプレートファイルとの対応

- **[テスト実施者向けガイド](docs/test_operator_guide.md)**
  - テスト実施手順
  - VS Code での実行方法
  - 結果ファイルの確認方法

## サンプルテスト

### 1. 計算機能テスト（test_calculation.py）
- 加算、減算、乗算、除算の基本演算
- ゼロ除算のエラーハンドリング
- 複合計算
- 大きな数値や浮動小数点の精度

### 2. 文字列処理テスト（test_string_processing.py）
- 文字列の反転
- 単語の大文字化
- 母音のカウント
- 回文チェック

### 3. リスト操作テスト（test_list_operations.py）
- 最大値/最小値の検索
- 平均値の計算
- 重複の削除
- ソート処理

### 4. データ検証テスト（test_data_validation.py）
- メールアドレスの検証
- 電話番号の検証
- 年齢の妥当性チェック
- パスワード強度の評価

## カスタマイズ

### 新しいテストの追加

1. `tests/`フォルダに新しいテストファイルを作成（ファイル名は`test_`で始める）
2. テストクラスやテスト関数を実装
3. 必要に応じて`@pytest.mark.category()`でカテゴリを設定

### Excel出力のカスタマイズ

`excel_reporter.py`を編集することで、以下をカスタマイズできます:
- シートの構成
- カラムの追加/削除
- スタイル（色、フォントなど）
- 統計情報の追加

### ログ出力のカスタマイズ

`logger_config.py`を編集することで、以下をカスタマイズできます:
- ログレベル
- ログフォーマット
- 出力先（ファイル、コンソール）

## ライセンス

このプロジェクトはサンプルコードです。自由に使用、改変してください。

## トラブルシューティング

### Excelファイルが生成されない

- `output/`フォルダの書き込み権限を確認してください
- pytestが正常に実行されているか確認してください

### ログが出力されない

- `output/`フォルダが存在するか確認してください
- ファイルシステムの書き込み権限を確認してください

### テストが見つからない

- テストファイル名が`test_`で始まっているか確認してください
- テスト関数名が`test_`で始まっているか確認してください
- テストクラス名が`Test`で始まっているか確認してください
