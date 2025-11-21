"""
pytest設定ファイル
テスト実行時のフックを定義し、Excel出力とロギングを統合
"""
import pytest
import logging
from datetime import datetime
from logger_config import setup_logger
from excel_reporter import ExcelReporter

# グローバル変数
excel_reporter = None
logger = None


def pytest_configure(config):
    """pytest開始時の設定"""
    global excel_reporter, logger
    
    # ロガーのセットアップ
    logger = setup_logger()
    logger.info("=" * 80)
    logger.info("pytestテスト実行を開始します")
    logger.info("=" * 80)
    
    # Excelレポーターの初期化
    excel_reporter = ExcelReporter()
    excel_reporter.initialize_workbook()


def pytest_runtest_setup(item):
    """各テスト実行前の処理"""
    logger.info(f"テスト開始: {item.nodeid}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """テスト実行レポートの作成"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        # テスト名の取得
        test_name = item.nodeid
        
        # カテゴリの取得
        category = "General"
        if hasattr(item, "own_markers"):
            for marker in item.own_markers:
                if marker.name == "category":
                    category = marker.args[0] if marker.args else "General"
                    break
        
        # カテゴリが設定されていない場合、ファイル名から推測
        if category == "General" and "::" in test_name:
            file_part = test_name.split("::")[0]
            if "test_" in file_part:
                category = file_part.split("test_")[-1].replace(".py", "").replace("_", " ").title()
        
        # 結果の取得
        status = rep.outcome  # passed, failed, skipped
        duration = rep.duration
        error_message = ""
        
        if status == "failed" and rep.longrepr:
            error_message = str(rep.longrepr)
        elif status == "skipped" and rep.longrepr:
            error_message = str(rep.longrepr)
        
        # レポートに追加
        excel_reporter.add_test_result(
            test_name=test_name,
            status=status,
            duration=duration,
            error_message=error_message,
            category=category
        )
        
        # ログ出力
        if status == "passed":
            logger.info(f"✓ テスト成功: {test_name} ({duration:.3f}秒)")
        elif status == "failed":
            logger.error(f"✗ テスト失敗: {test_name} ({duration:.3f}秒)")
            logger.error(f"  エラー: {error_message}")
        elif status == "skipped":
            logger.warning(f"⊘ テストスキップ: {test_name}")


def pytest_sessionfinish(session, exitstatus):
    """テストセッション終了時の処理"""
    global excel_reporter, logger
    
    logger.info("=" * 80)
    logger.info("pytestテスト実行が完了しました")
    logger.info("=" * 80)
    
    # Excelファイルの保存
    if excel_reporter:
        excel_file = excel_reporter.save()
        logger.info(f"テスト結果をExcelファイルに出力しました: {excel_file}")
