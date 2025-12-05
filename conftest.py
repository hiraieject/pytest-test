"""
pytest設定ファイル
テスト実行時のフックを定義し、Excel出力とロギングを統合
"""
import pytest
import logging
from datetime import datetime
from logger_config import setup_logger
from excel_reporter import ExcelReporter
from testlib.config_manager import ConfigManager
from testlib.excel_manager import ExcelManager

# グローバル変数
excel_reporter = None
excel_manager = None
config_manager = None
logger = None


def pytest_configure(config):
    """pytest開始時の設定"""
    global excel_reporter, excel_manager, config_manager, logger
    
    # ロガーのセットアップ
    logger = setup_logger()
    logger.info("=" * 80)
    logger.info("pytestテスト実行を開始します")
    logger.info("=" * 80)
    
    # 設定ファイルの読み込み
    try:
        config_manager = ConfigManager()
        logger.info(f"設定ファイルを読み込みました: {config_manager.config_path}")
        logger.info(f"  テンプレートファイル: {config_manager.template_file}")
        logger.info(f"  出力ファイル: {config_manager.output_file}")
        logger.info(f"  出力シート: {config_manager.output_sheet}")
        logger.info(f"  ROMバージョン: {config_manager.rom_version}")
        logger.info(f"  テスト実施者: {config_manager.tester_name}")
        
        # テンプレートベースのExcelマネージャーの初期化
        excel_manager = ExcelManager(
            template_path=config_manager.template_path,
            output_path=config_manager.output_path,
            sheet_name=config_manager.output_sheet,
            rom_version=config_manager.rom_version,
            tester_name=config_manager.tester_name
        )
        
        # 出力ファイルの準備（テンプレートのコピー）
        excel_manager.prepare_output_file()
        
        # ワークブックを開く
        excel_manager.open_workbook()
        
        # テスト諸情報の書き込み
        excel_manager.write_test_info()
        
    except Exception as e:
        logger.error(f"テンプレートベースの初期化に失敗しました: {e}")
        logger.info("フォールバック: 従来の方式でExcelレポーターを初期化します")
        excel_manager = None
    
    # 従来のExcelレポーターも初期化（両方のレポートを生成）
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
        
        # テスト番号の取得（test_idマーカーから）
        test_id = None
        if hasattr(item, "own_markers"):
            for marker in item.own_markers:
                if marker.name == "test_id":
                    test_id = marker.args[0] if marker.args else None
                    break
        
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
        
        # テンプレートベースのExcelに結果を記録
        if excel_manager and test_id:
            try:
                # エラー情報の抽出（より詳細な情報）
                error_info = ""
                if status == "failed" and rep.longrepr:
                    # アサーションエラーの詳細を抽出
                    longrepr_str = str(rep.longrepr)
                    # 最後の行にエラー詳細がある場合が多い
                    lines = longrepr_str.split('\n')
                    for line in reversed(lines):
                        if line.strip() and ('assert' in line.lower() or 'error' in line.lower()):
                            error_info = line.strip()
                            break
                    if not error_info and lines:
                        # アサーションが見つからない場合は最後の非空行を使用
                        for line in reversed(lines):
                            if line.strip():
                                error_info = line.strip()
                                break
                
                excel_manager.write_test_result(test_id, status, error_info)
            except Exception as e:
                logger.error(f"テンプレートベースのExcel記録に失敗しました: {e}")
        
        # 従来のレポートにも追加
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
    global excel_reporter, excel_manager, logger
    
    logger.info("=" * 80)
    logger.info("pytestテスト実行が完了しました")
    logger.info("=" * 80)
    
    # テンプレートベースのExcelを保存
    if excel_manager:
        try:
            excel_manager.save()
            excel_manager.close()
            logger.info(f"テンプレートベースの結果ファイルを保存しました: {excel_manager.output_path}")
        except Exception as e:
            logger.error(f"テンプレートベースのExcel保存に失敗しました: {e}")
    
    # 従来のExcelファイルの保存
    if excel_reporter:
        excel_file = excel_reporter.save()
        logger.info(f"詳細レポートをExcelファイルに出力しました: {excel_file}")
