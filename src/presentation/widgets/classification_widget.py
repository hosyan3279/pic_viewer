from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor

from domain.entities.image_classification import ImageClassification

class ClassificationWidget(QWidget):
    """分類結果を表示するウィジェット"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # レイアウトの設定
        self.layout = QVBoxLayout(self)
        
        # 分類結果を表示するパネル
        self.result_layout = QHBoxLayout()
        
        # NSFWラベル
        self.nsfw_label = QLabel("NSFW判定: ")
        self.result_layout.addWidget(self.nsfw_label)
        
        # 結果ラベル
        self.result_value = QLabel("未分類")
        self.result_layout.addWidget(self.result_value)
        
        # スコアラベル
        self.score_label = QLabel("スコア: ")
        self.result_layout.addWidget(self.score_label)
        
        # スコア値
        self.score_value = QLabel("-")
        self.result_layout.addWidget(self.score_value)
        
        # 分類日時
        self.date_label = QLabel("分類日時: ")
        self.result_layout.addWidget(self.date_label)
        
        # 日時値
        self.date_value = QLabel("-")
        self.result_layout.addWidget(self.date_value)
        
        self.layout.addLayout(self.result_layout)
        
        # 現在の分類結果
        self.current_classification = None
    
    def set_classification(self, classification: ImageClassification):
        """分類結果を設定する"""
        self.current_classification = classification
        
        # NSFWフラグの表示
        is_nsfw = classification.is_nsfw
        self.result_value.setText("はい" if is_nsfw else "いいえ")
        self.result_value.setStyleSheet(
            f"color: {'red' if is_nsfw else 'green'}; font-weight: bold;"
        )
        
        # スコアの表示
        nsfw_score = classification.nsfw_score
        self.score_value.setText(f"{nsfw_score:.2f}")
        
        # 分類日時の表示
        self.date_value.setText(classification.classified_at.strftime("%Y-%m-%d %H:%M:%S"))
