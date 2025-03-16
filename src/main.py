import sys
import os
from pathlib import Path

# ソースディレクトリをPythonパスに追加
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from PyQt6.QtWidgets import QApplication

from infrastructure.di.container import DIContainer

def main():
    """アプリケーションのエントリーポイント"""
    app = QApplication(sys.argv)
    
    # アプリケーション情報の設定
    app.setApplicationName("画像ビューワー")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("PicViewer")
    
    # スタイルシートの適用
    app.setStyle("Fusion")
    
    # 依存性注入コンテナの設定
    container = DIContainer()
    container.setup()
    
    # メインウィンドウの作成と表示
    main_window = container.create_main_window()
    main_window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
