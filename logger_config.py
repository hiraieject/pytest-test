"""
ロギング設定モジュール
テスト実行のログを適切に記録するための設定を提供
"""
import logging
import os
from datetime import datetime


def setup_logger(name: str = "pytest_logger", log_dir: str = "output") -> logging.Logger:
    """
    ロガーのセットアップ
    
    Args:
        name: ロガーの名前
        log_dir: ログファイルを保存するディレクトリ
    
    Returns:
        設定されたロガーインスタンス
    """
    # ログディレクトリの作成
    os.makedirs(log_dir, exist_ok=True)
    
    # ロガーの作成
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # 既存のハンドラをクリア（重複を防ぐ）
    if logger.handlers:
        logger.handlers.clear()
    
    # ファイルハンドラの設定
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"test_execution_{timestamp}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    
    # コンソールハンドラの設定
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # フォーマッタの設定
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # ハンドラの追加
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"ロガーを初期化しました: {log_file}")
    
    return logger
