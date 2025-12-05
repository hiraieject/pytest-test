# テスト実施者向けドキュメント

## 概要

このドキュメントは、pytest を使用してテストを実施するオペレーター向けの説明書です。

## 事前準備

### 1. 環境構築

#### 1.1 Python のインストール

Python 3.8 以上がインストールされていることを確認してください。

```bash
python --version
```

#### 1.2 依存パッケージのインストール

プロジェクトのルートディレクトリで以下のコマンドを実行します:

```bash
pip install -r requirements.txt
```

### 2. VS Code のセットアップ（推奨）

#### 2.1 VS Code のインストール

Visual Studio Code を以下からダウンロードしてインストールします:
https://code.visualstudio.com/

#### 2.2 Python 拡張機能のインストール

1. VS Code を起動
2. 左側の拡張機能アイコンをクリック
3. "Python" を検索してインストール

#### 2.3 プロジェクトを開く

1. VS Code で「ファイル」→「フォルダーを開く」
2. このプロジェクトのルートフォルダを選択

## テスト実施手順

### ステップ1: 設定ファイルの編集

テスト実施前に、`conf/config.yaml` を編集して必要な情報を入力します。

```yaml
# テンプレートファイル設定
template_file: "test_template.xlsx"  # 使用するテンプレートファイル名

# 出力ファイル設定
output_file: "test_results.xlsx"  # 結果ファイル名
output_sheet: "テスト結果"  # シート名

# テスト情報
rom_version: "v1.0"  # ターゲットROMバージョン（必ず入力してください）
tester_name: "山田太郎"  # テスト実施者氏名（任意）
```

**重要:** `rom_version` は必ず実施するROMのバージョンに変更してください。

### ステップ2: テンプレートファイルの確認

初回実施時のみ、`template/test_template.xlsx` の内容を確認してください。
このファイルがテスト仕様書兼結果ファイルの雛形となります。

- 3行目: ヘッダー行（変更しないでください）
- 4行目以降: テストケース一覧

### ステップ3: テストの実行

#### 方法A: VS Code の UI から実行（推奨）

1. VS Code の左側のアクティビティバーで「テスト」アイコンをクリック
2. テストエクスプローラーが表示されます
3. テスト一覧が表示されるので、実行したいテストを選択
4. テストの横にある「▶」ボタンをクリックして実行

**メリット:**
- 視覚的にテスト一覧を確認できる
- 個別のテストを選択して実行できる
- テスト結果がリアルタイムで表示される
- 失敗したテストを簡単に再実行できる

#### 方法B: ターミナルから実行

VS Code 内でターミナルを開いて実行します:

1. VS Code で「ターミナル」→「新しいターミナル」
2. 以下のコマンドを実行

**全テストを実行:**
```bash
pytest
```

**詳細な出力で実行:**
```bash
pytest -v
```

**特定のテストファイルのみ実行:**
```bash
pytest tests/test_calculation.py
```

**特定のテストクラスのみ実行:**
```bash
pytest tests/test_calculation.py::TestBasicCalculation
```

**特定のテストケースのみ実行:**
```bash
pytest tests/test_calculation.py::TestBasicCalculation::test_add_positive_numbers
```

### ステップ4: 結果の確認

テスト実行後、以下のファイルが生成されます:

#### 1. テスト結果ファイル（テンプレートベース）

**場所:** `output/test_results.xlsx`

このファイルがメインの結果ファイルです。テンプレートファイルに基づいて作成され、以下の情報が自動的に記録されます:

- **1行目**: ターゲットROMバージョン
- **F列（テスト実施日付）**: テスト実施日（月/日形式）
- **G列（テスト結果）**: OK/NG/SKIP
- **H列（テスト結果補足）**: NG の場合、エラーの詳細情報

**注意:**
- このファイルは初回実行時にテンプレートからコピーされます
- 2回目以降の実行では既存のファイルが更新されます（上書き）
- テスト結果は上書きされるため、過去の結果を保存したい場合は別名でコピーしてください

#### 2. 詳細レポート

**場所:** `output/test_results_YYYYMMDD_HHMMSS.xlsx`

実行ごとに生成される詳細なレポートファイルです。

- **Summaryシート**: 実行統計
- **カテゴリ別シート**: カテゴリごとの結果
- **All Testsシート**: 全テストの詳細

#### 3. 実行ログ

**場所:** `output/test_execution_YYYYMMDD_HHMMSS.log`

テスト実行の詳細ログが記録されます。

### ステップ5: 結果の評価

#### 正常終了の場合

```
============ 41 passed in 0.16s ============
```

- すべてのテストが成功（passed）
- `output/test_results.xlsx` のG列がすべて「OK」

#### 一部失敗の場合

```
============ 38 passed, 3 failed in 0.20s ============
```

- 一部のテストが失敗（failed）
- `output/test_results.xlsx` で「NG」となっている行を確認
- H列（テスト結果補足）にエラーの詳細が記録されています

#### スキップがある場合

```
============ 40 passed, 1 skipped in 0.18s ============
```

- 一部のテストがスキップされました
- スキップされたテストは未実装または条件により実行されませんでした

## テスト再実行

### 全テストの再実行

設定ファイルやテンプレートファイルを変更せずに、再度全テストを実行する場合:

```bash
pytest
```

既存の `output/test_results.xlsx` が上書きされます。

### 失敗したテストのみ再実行

前回失敗したテストのみを再実行する場合:

```bash
pytest --lf
```

### 新しい結果ファイルで実行

新しい結果ファイルを作成したい場合は、以下の手順で実施します:

1. `conf/config.yaml` の `output_file` を変更
   ```yaml
   output_file: "test_results_v1.1.xlsx"
   ```

2. テストを実行
   ```bash
   pytest
   ```

## よくある質問（FAQ）

### Q1: テスト結果ファイルが見つからない

**A:** `output/` フォルダを確認してください。初回実行時にテンプレートファイルからコピーされて作成されます。

### Q2: 一部のテストしか結果に記録されない

**A:** テストスクリプトに `@pytest.mark.test_id()` が設定されているテストのみが、テンプレートベースの結果ファイルに記録されます。詳細レポートには全テストが記録されています。

### Q3: エラーメッセージが文字化けする

**A:** Excel でファイルを開く際、文字エンコーディングが正しく認識されていない可能性があります。VS Code などのテキストエディタでログファイルを確認してください。

### Q4: 前回の結果を保存したい

**A:** テスト実行前に `output/test_results.xlsx` を別名でコピーしてください。または、`conf/config.yaml` の `output_file` を変更して新しいファイル名で実行してください。

### Q5: ROMバージョンを変更し忘れた

**A:** `conf/config.yaml` の `rom_version` を修正して、テストを再実行してください。

## トラブルシューティング

### エラー: "設定ファイルが見つかりません"

```
FileNotFoundError: 設定ファイルが見つかりません: conf/config.yaml
```

**対処法:**
- `conf/config.yaml` が存在するか確認
- プロジェクトのルートディレクトリで pytest を実行しているか確認

### エラー: "テンプレートファイルが見つかりません"

```
FileNotFoundError: テンプレートファイルが見つかりません: template/test_template.xlsx
```

**対処法:**
- `template/` フォルダにテンプレートファイルが存在するか確認
- `conf/config.yaml` の `template_file` の設定が正しいか確認

### エラー: "ModuleNotFoundError"

```
ModuleNotFoundError: No module named 'pytest'
```

**対処法:**
```bash
pip install -r requirements.txt
```

### VS Code でテストが表示されない

**対処法:**
1. VS Code でPython インタープリターが正しく設定されているか確認
2. コマンドパレット（Ctrl+Shift+P / Cmd+Shift+P）を開く
3. "Python: Select Interpreter" を選択
4. プロジェクトで使用する Python を選択

## 結果ファイルの提出

テスト完了後、以下のファイルを提出してください:

1. **必須:** `output/test_results.xlsx` - テンプレートベースの結果ファイル
2. **推奨:** `output/test_results_YYYYMMDD_HHMMSS.xlsx` - 詳細レポート（最新のもの）
3. **推奨:** `output/test_execution_YYYYMMDD_HHMMSS.log` - 実行ログ（最新のもの）

## 問い合わせ

テスト実施中に不明点や問題が発生した場合は、開発チームに問い合わせてください。
