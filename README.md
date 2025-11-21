# pytest サンプルプロジェクト

このプロジェクトは、pytestを使用したテストの実装例と、テスト結果をExcelファイルに出力する機能を提供します。

## 機能

- ✅ pytestを使用した複数のテストケース
- 📊 テスト結果の自動Excel出力
- 📝 実行ログの記録
- 🏷️ カテゴリ別のテスト結果管理

## プロジェクト構成

```
pytest-test/
├── tests/                      # テストファイル格納フォルダ
│   ├── test_calculation.py     # 計算機能のテスト
│   ├── test_string_processing.py  # 文字列処理のテスト
│   ├── test_list_operations.py    # リスト操作のテスト
│   └── test_data_validation.py    # データ検証のテスト
├── output/                     # 出力フォルダ（Excel、ログ）
│   ├── test_results_*.xlsx     # テスト結果Excelファイル
│   └── test_execution_*.log    # 実行ログファイル
├── conftest.py                 # pytest設定ファイル
├── excel_reporter.py           # Excelレポート生成モジュール
├── logger_config.py            # ロギング設定モジュール
├── requirements.txt            # 依存パッケージ
└── README.md                   # このファイル
```

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. テストの実行

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

### Excelファイル（output/test_results_*.xlsx）

テスト実行後、`output`フォルダに以下の構成でExcelファイルが生成されます:

1. **Summaryシート**: テスト実行の統計情報
   - 総テスト数
   - 成功/失敗/スキップの件数と割合
   - 実行日時

2. **カテゴリ別シート**: 各カテゴリごとの詳細結果
   - Calculation（計算機能）
   - String Processing（文字列処理）
   - List Operations（リスト操作）
   - Data Validation（データ検証）

3. **All Testsシート**: 全テストの詳細結果
   - テスト名
   - カテゴリ
   - 結果（成功/失敗/スキップ）
   - 実行時間
   - エラーメッセージ

### ログファイル（output/test_execution_*.log）

テスト実行の詳細ログが記録されます:
- 各テストの開始/終了
- 成功/失敗の情報
- エラー詳細
- 実行時刻

## テストのカテゴリ

テストにカテゴリを設定するには、`@pytest.mark.category()`デコレータを使用します:

```python
import pytest

@pytest.mark.category("Custom Category")
class TestExample:
    def test_something(self):
        assert True
```

カテゴリを指定しない場合、ファイル名から自動的に推測されます。

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
