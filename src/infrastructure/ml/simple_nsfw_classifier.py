import os
import uuid
from datetime import datetime
from typing import Dict, Tuple
import numpy as np
from PIL import Image as PILImage

from domain.entities.image import Image
from domain.entities.image_classification import ImageClassification
from domain.services.image_classification_service import ImageClassificationService

class SimpleNSFWClassifier(ImageClassificationService):
    """シンプルな画像特性を使ったNSFW分類器の実装
    外部ライブラリに依存しない簡易実装
    """
    
    def __init__(self):
        self.loaded = True  # 常にロード済み
    
    def classify_is_nsfw(self, image: Image, classifier_type: str = "simple") -> ImageClassification:
        """画像を分類する（シンプルなヒューリスティックを使用）"""
        try:
            # 画像を読み込み
            pil_image = PILImage.open(image.path)
            
            # RGB形式に変換
            pil_image = pil_image.convert('RGB')
            
            # 画像を小さなサイズにリサイズ（処理を高速化）
            pil_image = pil_image.resize((100, 100))
            
            # NumPy配列に変換
            img_array = np.array(pil_image)
            
            # シンプルなヒューリスティック: 肌色の割合を計算
            # 肌色のRGB範囲を定義（かなり大まかな近似）
            r_range = (60, 255)
            g_range = (40, 200)
            b_range = (20, 180)
            
            # 肌色のピクセル数をカウント
            skin_pixels = np.logical_and.reduce([
                img_array[:, :, 0] >= r_range[0],
                img_array[:, :, 0] <= r_range[1],
                img_array[:, :, 1] >= g_range[0],
                img_array[:, :, 1] <= g_range[1],
                img_array[:, :, 2] >= b_range[0],
                img_array[:, :, 2] <= b_range[1]
            ])
            
            # 肌色の比率を計算
            skin_ratio = np.sum(skin_pixels) / (100 * 100)
            
            # NSFWスコアを設定（0.3~0.8の間に調整）
            # 完全にランダムではなく、肌色の比率を考慮するが、あくまでデモ用
            nsfw_score = min(0.3 + skin_ratio * 0.5, 0.8)
            
            # ファイル名にNSFWを示す単語が含まれているか確認（デモ用）
            filename_lower = image.filename.lower()
            if any(word in filename_lower for word in ['nsfw', 'adult', 'xxx', '18']):
                nsfw_score = max(nsfw_score, 0.7)  # ファイル名に基づいてスコアを上げる
            
            # NSFWかどうかの判断
            is_nsfw = nsfw_score > 0.5
            
            # 分類結果を作成
            classification = ImageClassification(
                id=str(uuid.uuid4()),
                image_id=image.id,
                is_nsfw=is_nsfw,
                nsfw_score=float(nsfw_score),
                classification_method="SimpleHeuristic",
                classified_at=datetime.now()
            )
            
            return classification
        
        except Exception as e:
            print(f"Error classifying image: {e}")
            # エラーが発生した場合は、ダミーの結果を返す
            return ImageClassification(
                id=str(uuid.uuid4()),
                image_id=image.id,
                is_nsfw=False,
                nsfw_score=0.0,
                classification_method="error",
                classified_at=datetime.now()
            )
