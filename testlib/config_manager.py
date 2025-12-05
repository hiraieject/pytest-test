"""
設定ファイル管理モジュール
conf/config.yaml からテスト実行設定を読み込む
"""
import os
import yaml
from typing import Dict, Any


class ConfigManager:
    """設定ファイル管理クラス"""
    
    def __init__(self, config_path: str = "conf/config.yaml"):
        """
        初期化
        
        Args:
            config_path: 設定ファイルのパス
        """
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self):
        """設定ファイルの読み込み"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"設定ファイルが見つかりません: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        # デフォルト値の設定
        self.config.setdefault('rom_version', 'v0.0')
        self.config.setdefault('tester_name', '')
    
    def get(self, key: str, default=None):
        """
        設定値の取得
        
        Args:
            key: 設定キー
            default: デフォルト値
            
        Returns:
            設定値
        """
        return self.config.get(key, default)
    
    @property
    def template_file(self) -> str:
        """テンプレートファイル名"""
        return self.config.get('template_file', 'test_template.xlsx')
    
    @property
    def template_path(self) -> str:
        """テンプレートファイルのフルパス"""
        return os.path.join('template', self.template_file)
    
    @property
    def output_file(self) -> str:
        """出力ファイル名"""
        return self.config.get('output_file', 'test_results.xlsx')
    
    @property
    def output_path(self) -> str:
        """出力ファイルのフルパス"""
        return os.path.join('output', self.output_file)
    
    @property
    def output_sheet(self) -> str:
        """出力シート名"""
        return self.config.get('output_sheet', 'テスト結果')
    
    @property
    def rom_version(self) -> str:
        """ターゲットROMバージョン"""
        return self.config.get('rom_version', 'v0.0')
    
    @property
    def tester_name(self) -> str:
        """テスト実施者氏名"""
        return self.config.get('tester_name', '')
