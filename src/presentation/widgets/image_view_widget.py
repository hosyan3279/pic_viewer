from PyQt6.QtWidgets import QScrollArea, QLabel, QSizePolicy, QWidget, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QTransform

from domain.entities.image import Image
from presentation.widgets.video_player_widget import VideoPlayerWidget

class ImageViewWidget(QScrollArea):
    """画像を表示するウィジェット"""
    
    def __init__(self):
        super().__init__()
        
        self.setWidgetResizable(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # コンテナウィジェット
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        
        # スタックウィジェット（画像と動画の切り替え用）
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        # 画像表示用ラベル
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.stack.addWidget(self.image_label)
        
        # 動画プレーヤー
        self.video_player = VideoPlayerWidget()
        self.stack.addWidget(self.video_player)
        
        self.setWidget(self.container)
        
        # 画像データ
        self.current_pixmap = None
        self.zoom_level = 1.0
        self.rotation = 0
        self.current_image = None
    
    def set_image(self, image: Image):
        """画像を設定する"""
        self.current_image = image
        
        # 動画か画像か判定
        if image.is_video:
            # 動画の場合
            self.stack.setCurrentWidget(self.video_player)
            self.video_player.set_video(image.path)
            return
        
        # 画像の場合
        self.stack.setCurrentWidget(self.image_label)
        pixmap = QPixmap(image.path)
        if pixmap.isNull():
            self.image_label.setText("画像を読み込めませんでした")
            return
        
        self.current_pixmap = pixmap
        self._update_display()
    
    def set_zoom(self, zoom_level: float):
        """ズームレベルを設定する"""
        self.zoom_level = zoom_level
        self._update_display()
    
    def set_rotation(self, rotation: int):
        """回転角度を設定する"""
        self.rotation = rotation
        self._update_display()
    
    def _update_display(self):
        """表示を更新する"""
        if self.current_pixmap is None:
            return
        
        # 回転
        transform = QTransform().rotate(self.rotation)
        rotated_pixmap = self.current_pixmap.transformed(transform)
        
        # ズーム
        w = int(rotated_pixmap.width() * self.zoom_level)
        h = int(rotated_pixmap.height() * self.zoom_level)
        
        # 表示
        self.image_label.setPixmap(
            rotated_pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        )
        
        # ラベルのサイズを調整
        self.image_label.resize(w, h)
