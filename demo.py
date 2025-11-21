#!/usr/bin/env python3
"""
pytestサンプルプロジェクトのデモスクリプト
テスト実行とレポート生成の例を示します
"""
import subprocess
import sys
import os
from datetime import datetime


def print_banner(text):
    """バナーを表示"""
    print("\n" + "=" * 80)
    print(f" {text}")
    print("=" * 80 + "\n")


def run_tests():
    """テストを実行"""
    print_banner("pytestテストを実行中...")
    
    # テストの実行
    result = subprocess.run(
        ["python3", "-m", "pytest", "-v"],
        cwd=os.path.dirname(os.path.abspath(__file__)),
        capture_output=False
    )
    
    return result.returncode == 0


def show_output_files():
    """生成されたファイルを表示"""
    print_banner("生成されたファイル")
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    
    if os.path.exists(output_dir):
        files = sorted(os.listdir(output_dir))
        
        # Excelファイル
        excel_files = [f for f in files if f.endswith('.xlsx')]
        if excel_files:
            print("📊 Excelファイル:")
            for f in excel_files:
                file_path = os.path.join(output_dir, f)
                size = os.path.getsize(file_path)
                print(f"  - {f} ({size:,} bytes)")
        
        # ログファイル
        log_files = [f for f in files if f.endswith('.log')]
        if log_files:
            print("\n📝 ログファイル:")
            for f in log_files:
                file_path = os.path.join(output_dir, f)
                size = os.path.getsize(file_path)
                print(f"  - {f} ({size:,} bytes)")
        
        # 最新のファイルを表示
        if excel_files:
            latest_excel = sorted(excel_files)[-1]
            print(f"\n💡 最新のExcelレポート: output/{latest_excel}")
        
        if log_files:
            latest_log = sorted(log_files)[-1]
            print(f"💡 最新のログファイル: output/{latest_log}")
    else:
        print("❌ outputフォルダが見つかりません")


def show_test_categories():
    """テストカテゴリを表示"""
    print_banner("テストカテゴリ")
    
    categories = {
        "Calculation": "計算機能のテスト（加算、減算、乗算、除算など）",
        "String Processing": "文字列処理のテスト（反転、大文字化、回文チェックなど）",
        "List Operations": "リスト操作のテスト（最大値、最小値、ソートなど）",
        "Data Validation": "データ検証のテスト（メール、電話番号、パスワード強度など）"
    }
    
    for category, description in categories.items():
        print(f"📁 {category}")
        print(f"   {description}\n")


def main():
    """メイン関数"""
    print_banner("pytest サンプルプロジェクト デモ")
    
    print("このスクリプトは以下を実行します:")
    print("1. テストカテゴリの表示")
    print("2. pytestの実行")
    print("3. 生成されたファイルの表示\n")
    
    # テストカテゴリの表示
    show_test_categories()
    
    # テストの実行
    success = run_tests()
    
    # 生成されたファイルの表示
    show_output_files()
    
    # まとめ
    print_banner("完了")
    if success:
        print("✅ すべてのテストが正常に実行されました")
        print("\n次のステップ:")
        print("1. output/フォルダ内のExcelファイルを開いてテスト結果を確認")
        print("2. output/フォルダ内のログファイルでテスト実行の詳細を確認")
        print("3. tests/フォルダ内のPythonファイルでテストコードを確認")
    else:
        print("⚠️  一部のテストが失敗しました")
        print("詳細はログファイルを確認してください")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
