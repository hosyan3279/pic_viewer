from PyQt6.QtWidgets import QListWidget, QListView, QListWidgetItem
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from typing import List

from domain.entities.image import Image

class ImageListWidget(QListWidget):
    """画像のサムネイルリストを表示するウィジェット"""
    
    image_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setIconSize(QSize(120, 120))
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setWrapping(True)
        self.setSpacing(10)
        
        # シグナルの接続
        self.itemClicked.connect(self._on_item_clicked)
    
    def set_images(self, images: List[Image]):
        """画像リストを設定する"""
        self.clear()
        
        for image in images:
            item = QListWidgetItem()
            item.setText(image.filename)
            item.setData(Qt.ItemDataRole.UserRole, image.id)
            
            # サムネイルの設定（実際には非同期で行うべき）
            pixmap = QPixmap(image.path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                item.setIcon(QIcon(pixmap))
            else:
                # 画像が読み込めない場合のデフォルトアイコン
                item.setIcon(QIcon.fromTheme("image-x-generic"))
            
            self.addItem(item)
    
    def _on_item_clicked(self, item: QListWidgetItem):
        """アイテムがクリックされたときの処理"""
        image_id = item.data(Qt.ItemDataRole.UserRole)
        self.image_selected.emit(image_id)
